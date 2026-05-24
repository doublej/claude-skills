#!/usr/bin/env python3
"""Audit a FastAPI project for docs-upgrade opportunities.

Outputs JSON to stdout. Usage:
    python3 audit_fastapi.py [project_root]

Identifies:
- The FastAPI(...) instantiation file and its kwargs
- All APIRouter definitions (prefix, tags)
- Route decorators with their currently-set metadata kwargs
- Pydantic models and field/example coverage
- Whether scalar/rapidoc/elements are already mounted
- Whether a custom_openapi hook is wired

Read-only. Pure AST — no imports of project code. Skips venvs, build dirs, node_modules.
"""

from __future__ import annotations

import ast
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROUTE_DECORATORS = {"get", "post", "put", "patch", "delete", "head", "options", "trace", "api_route"}
ROUTE_METADATA_KWARGS = {
    "summary", "description", "response_description", "responses",
    "tags", "operation_id", "deprecated", "openapi_extra",
    "response_model", "response_model_exclude_unset", "status_code",
    "name", "include_in_schema",
}
APP_METADATA_KWARGS = {
    "title", "summary", "description", "version", "openapi_url",
    "docs_url", "redoc_url", "terms_of_service", "contact", "license_info",
    "openapi_tags", "servers", "swagger_ui_parameters",
}
SKIP_DIRS = {
    ".venv", "venv", "env", ".env", "node_modules", "dist", "build",
    "__pycache__", ".git", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".tox", "site-packages", "target", ".next", ".nuxt",
}


@dataclass
class RouteHit:
    file: str
    line: int
    method: str
    path: str
    decorator_target: str  # "app" or router var name
    set_kwargs: list[str]
    missing_kwargs: list[str]
    has_docstring: bool


@dataclass
class RouterHit:
    file: str
    line: int
    var: str
    prefix: str | None
    tags: list[str]


@dataclass
class AppHit:
    file: str
    line: int
    var: str
    set_kwargs: list[str]
    missing_kwargs: list[str]


@dataclass
class ModelHit:
    file: str
    line: int
    name: str
    fields_total: int
    fields_with_description: int
    fields_with_examples: int
    has_model_config_examples: bool


@dataclass
class UIStatus:
    has_scalar_mount: bool = False
    has_rapidoc_mount: bool = False
    has_elements_mount: bool = False
    has_custom_openapi_hook: bool = False
    swagger_ui_parameters_set: bool = False
    openapi_tags_set: bool = False


@dataclass
class Audit:
    project_root: str
    python_files_scanned: int
    apps: list[AppHit] = field(default_factory=list)
    routers: list[RouterHit] = field(default_factory=list)
    routes: list[RouteHit] = field(default_factory=list)
    models: list[ModelHit] = field(default_factory=list)
    ui_status: UIStatus = field(default_factory=UIStatus)
    package_manager: str = "unknown"  # uv | pip | poetry | unknown


def discover_python_files(root: Path) -> list[Path]:
    files = []
    for p in root.rglob("*.py"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        files.append(p)
    return files


def detect_package_manager(root: Path) -> str:
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text(encoding="utf-8", errors="ignore")
        if "[tool.uv]" in text or "[tool.uv." in text:
            return "uv"
        if "[tool.poetry]" in text:
            return "poetry"
        if "[project]" in text:
            return "uv"  # PEP 621; uv works, prefer it
    if (root / "uv.lock").exists():
        return "uv"
    if (root / "poetry.lock").exists():
        return "poetry"
    if (root / "requirements.txt").exists():
        return "pip"
    return "unknown"


def get_kw_names(call: ast.Call) -> set[str]:
    return {kw.arg for kw in call.keywords if kw.arg}


def call_is(call: ast.Call, name: str) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id == name:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == name:
        return True
    return False


def is_attr_call(node: ast.AST, attr: str) -> tuple[str, str] | None:
    """If node is `something.attr(...)`, return (something_repr, attr). Else None."""
    if not isinstance(node, ast.Call):
        return None
    if not isinstance(node.func, ast.Attribute):
        return None
    if node.func.attr != attr:
        return None
    target = node.func.value
    if isinstance(target, ast.Name):
        return (target.id, attr)
    return (ast.unparse(target), attr)


def first_str_arg(call: ast.Call) -> str:
    if call.args and isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str):
        return call.args[0].value
    return ""


def kwarg_str(call: ast.Call, name: str) -> str | None:
    for kw in call.keywords:
        if kw.arg == name and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
            return kw.value.value
    return None


def kwarg_str_list(call: ast.Call, name: str) -> list[str]:
    for kw in call.keywords:
        if kw.arg == name and isinstance(kw.value, (ast.List, ast.Tuple)):
            return [e.value for e in kw.value.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
    return []


def analyze_file(path: Path, root: Path, audit: Audit) -> None:
    try:
        src = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return
    try:
        tree = ast.parse(src, filename=str(path))
    except SyntaxError:
        return

    rel = str(path.relative_to(root))

    # Detect alt UI mounts and openapi hook by string search on source — cheaper than AST walking
    if "get_scalar_api_reference" in src or "scalar_fastapi" in src:
        audit.ui_status.has_scalar_mount = True
    if "rapidoc" in src.lower() and "rapi-doc" in src.lower():
        audit.ui_status.has_rapidoc_mount = True
    if "elements-api" in src or "@stoplight/elements" in src:
        audit.ui_status.has_elements_mount = True

    # Track router var names for route detection
    router_vars: set[str] = set()
    app_vars: set[str] = set()

    for node in ast.walk(tree):
        # App / Router instantiation: var = FastAPI(...) / var = APIRouter(...)
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            call = node.value
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                if call_is(call, "FastAPI"):
                    set_kw = get_kw_names(call)
                    audit.apps.append(AppHit(
                        file=rel, line=node.lineno, var=target.id,
                        set_kwargs=sorted(set_kw),
                        missing_kwargs=sorted(APP_METADATA_KWARGS - set_kw),
                    ))
                    app_vars.add(target.id)
                    if "swagger_ui_parameters" in set_kw:
                        audit.ui_status.swagger_ui_parameters_set = True
                    if "openapi_tags" in set_kw:
                        audit.ui_status.openapi_tags_set = True
                elif call_is(call, "APIRouter"):
                    prefix = kwarg_str(call, "prefix")
                    tags = kwarg_str_list(call, "tags")
                    audit.routers.append(RouterHit(
                        file=rel, line=node.lineno, var=target.id, prefix=prefix, tags=tags,
                    ))
                    router_vars.add(target.id)

        # custom_openapi hook detection: app.openapi = something
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (isinstance(target, ast.Attribute) and target.attr == "openapi"
                        and isinstance(target.value, ast.Name)):
                    audit.ui_status.has_custom_openapi_hook = True

        # Pydantic models: class X(BaseModel)
        if isinstance(node, ast.ClassDef):
            is_pydantic = any(
                (isinstance(b, ast.Name) and b.id == "BaseModel")
                or (isinstance(b, ast.Attribute) and b.attr == "BaseModel")
                for b in node.bases
            )
            if is_pydantic:
                fields_total = 0
                fields_with_desc = 0
                fields_with_ex = 0
                has_examples_cfg = False
                for sub in node.body:
                    if isinstance(sub, ast.AnnAssign) and isinstance(sub.target, ast.Name):
                        fields_total += 1
                        if isinstance(sub.value, ast.Call) and call_is(sub.value, "Field"):
                            kws = get_kw_names(sub.value)
                            if "description" in kws:
                                fields_with_desc += 1
                            if "examples" in kws or "example" in kws:
                                fields_with_ex += 1
                    if isinstance(sub, ast.Assign) and any(
                        isinstance(t, ast.Name) and t.id == "model_config" for t in sub.targets
                    ):
                        # crude: check if json_schema_extra mentioned
                        cfg_src = ast.unparse(sub.value)
                        if "json_schema_extra" in cfg_src and "example" in cfg_src:
                            has_examples_cfg = True
                audit.models.append(ModelHit(
                    file=rel, line=node.lineno, name=node.name,
                    fields_total=fields_total,
                    fields_with_description=fields_with_desc,
                    fields_with_examples=fields_with_ex,
                    has_model_config_examples=has_examples_cfg,
                ))

    # Second pass: route decorators (need router_vars+app_vars known)
    targets_of_interest = app_vars | router_vars | {"app", "router"}  # fallback names
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        has_doc = bool(ast.get_docstring(node))
        for dec in node.decorator_list:
            hit = None
            for method in ROUTE_DECORATORS:
                got = is_attr_call(dec, method)
                if got and got[0] in targets_of_interest:
                    hit = (got[0], method, dec)
                    break
            if not hit:
                continue
            target_var, method, dec_call = hit
            path_str = first_str_arg(dec_call)
            set_kw = get_kw_names(dec_call)
            audit.routes.append(RouteHit(
                file=rel, line=node.lineno, method=method, path=path_str,
                decorator_target=target_var,
                set_kwargs=sorted(set_kw),
                missing_kwargs=sorted(ROUTE_METADATA_KWARGS - set_kw),
                has_docstring=has_doc,
            ))


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.is_dir():
        print(json.dumps({"error": f"not a directory: {root}"}), file=sys.stderr)
        return 2

    files = discover_python_files(root)
    audit = Audit(
        project_root=str(root),
        python_files_scanned=len(files),
        package_manager=detect_package_manager(root),
    )
    for f in files:
        analyze_file(f, root, audit)

    payload = asdict(audit)
    # Coverage summary
    total_routes = len(audit.routes)
    routes_missing_summary = sum(1 for r in audit.routes if "summary" in r.missing_kwargs)
    routes_missing_responses = sum(1 for r in audit.routes if "responses" in r.missing_kwargs)
    routes_no_docstring = sum(1 for r in audit.routes if not r.has_docstring)
    models_missing_examples = sum(
        1 for m in audit.models
        if m.fields_total > 0
        and m.fields_with_examples == 0
        and not m.has_model_config_examples
    )
    payload["summary"] = {
        "apps_found": len(audit.apps),
        "routers_found": len(audit.routers),
        "routes_found": total_routes,
        "models_found": len(audit.models),
        "routes_missing_summary": routes_missing_summary,
        "routes_missing_responses": routes_missing_responses,
        "routes_without_docstring": routes_no_docstring,
        "models_without_any_examples": models_missing_examples,
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
