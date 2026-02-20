"""
RepoMap class for generating repository maps.
"""

import os
import sys
from pathlib import Path
from collections import namedtuple, defaultdict
from typing import List, Dict, Set, Optional, Tuple, Callable, Any
import shutil
import sqlite3
from utils import Tag

try:
    import networkx as nx
except ImportError:
    print("Error: networkx is required. Install with: pip install networkx")
    sys.exit(1)

try:
    import diskcache
except ImportError:
    print("Error: diskcache is required. Install with: pip install diskcache")
    sys.exit(1)

try:
    from grep_ast import TreeContext
except ImportError:
    print("Error: grep-ast is required. Install with: pip install grep-ast")
    sys.exit(1)

from utils import count_tokens, read_text, Tag
from scm import get_scm_fname
from importance import filter_important_files

# Constants
CACHE_VERSION = 1
TAGS_CACHE_DIRNAME = f".repomap.tags.cache.v{CACHE_VERSION}"
SQLITE_ERRORS = (sqlite3.OperationalError, sqlite3.DatabaseError)

# Tag namedtuple for storing parsed code definitions and references
Tag = namedtuple("Tag", "rel_fname fname line name kind".split())


class RepoMap:
    """Main class for generating repository maps."""
    
    def __init__(
        self,
        map_tokens: int = 1024,
        root: str = None,
        token_counter_func: Callable[[str], int] = count_tokens,
        file_reader_func: Callable[[str], Optional[str]] = read_text,
        output_handler_funcs: Dict[str, Callable] = None,
        repo_content_prefix: Optional[str] = None,
        verbose: bool = False,
        max_context_window: Optional[int] = None,
        map_mul_no_files: int = 8,
        refresh: str = "auto",
        exclude_unranked: bool = False
    ):
        """Initialize RepoMap instance."""
        self.map_tokens = map_tokens
        self.max_map_tokens = map_tokens
        self.root = Path(root or os.getcwd()).resolve()
        self.token_count_func_internal = token_counter_func
        self.read_text_func_internal = file_reader_func
        self.repo_content_prefix = repo_content_prefix
        self.verbose = verbose
        self.max_context_window = max_context_window
        self.map_mul_no_files = map_mul_no_files
        self.refresh = refresh
        self.exclude_unranked = exclude_unranked
        
        # Set up output handlers
        if output_handler_funcs is None:
            output_handler_funcs = {
                'info': print,
                'warning': print,
                'error': print
            }
        self.output_handlers = output_handler_funcs
        
        # Initialize caches
        self.tree_cache = {}
        self.tree_context_cache = {}
        self.map_cache = {}
        self.ranked_file_count = 0
        
        # Load persistent tags cache
        self.load_tags_cache()
    
    def load_tags_cache(self):
        """Load the persistent tags cache."""
        cache_dir = self.root / TAGS_CACHE_DIRNAME
        try:
            self.TAGS_CACHE = diskcache.Cache(str(cache_dir))
        except Exception as e:
            self.output_handlers['warning'](f"Failed to load tags cache: {e}")
            self.TAGS_CACHE = {}
    
    def save_tags_cache(self):
        """Save the tags cache (no-op as diskcache handles persistence)."""
        pass
    
    def tags_cache_error(self):
        """Handle tags cache errors."""
        try:
            cache_dir = self.root / TAGS_CACHE_DIRNAME
            if cache_dir.exists():
                shutil.rmtree(cache_dir)
            self.load_tags_cache()
        except Exception:
            self.output_handlers['warning']("Failed to recreate tags cache, using in-memory cache")
            self.TAGS_CACHE = {}
    
    def token_count(self, text: str) -> int:
        """Count tokens in text with sampling optimization for long texts."""
        if not text:
            return 0
        
        len_text = len(text)
        if len_text < 200:
            return self.token_count_func_internal(text)
        
        # Sample for longer texts
        lines = text.splitlines(keepends=True)
        num_lines = len(lines)
        
        step = max(1, num_lines // 100)
        sampled_lines = lines[::step]
        sample_text = "".join(sampled_lines)
        
        if not sample_text:
            return self.token_count_func_internal(text)
        
        sample_tokens = self.token_count_func_internal(sample_text)
        
        if len(sample_text) == 0:
            return self.token_count_func_internal(text)
        
        est_tokens = (sample_tokens / len(sample_text)) * len_text
        return int(est_tokens)
    
    def get_rel_fname(self, fname: str) -> str:
        """Get relative filename from absolute path."""
        try:
            return str(Path(fname).relative_to(self.root))
        except ValueError:
            return fname
    
    def get_mtime(self, fname: str) -> Optional[float]:
        """Get file modification time."""
        try:
            return os.path.getmtime(fname)
        except FileNotFoundError:
            self.output_handlers['warning'](f"File not found: {fname}")
            return None
    
    def get_tags(self, fname: str, rel_fname: str) -> List[Tag]:
        """Get tags for a file, using cache when possible."""
        file_mtime = self.get_mtime(fname)
        if file_mtime is None:
            return []
        
        try:
            cached_entry = self.TAGS_CACHE.get(fname)
            if cached_entry and cached_entry.get("mtime") == file_mtime:
                return cached_entry["data"]
        except SQLITE_ERRORS:
            self.tags_cache_error()
        
        # Cache miss or file changed
        tags = self.get_tags_raw(fname, rel_fname)
        
        try:
            self.TAGS_CACHE[fname] = {"mtime": file_mtime, "data": tags}
        except SQLITE_ERRORS:
            self.tags_cache_error()
        
        return tags
    
    def get_tags_raw(self, fname: str, rel_fname: str) -> List[Tag]:
        """Parse file to extract tags using Tree-sitter."""
        try:
            from grep_ast import filename_to_lang
            from grep_ast.tsl import get_language, get_parser
        except ImportError:
            print("Error: grep-ast is required. Install with: pip install grep-ast")
            sys.exit(1)
            
        lang = filename_to_lang(fname)
        if not lang:
            return []
        
        try:
            language = get_language(lang)
            parser = get_parser(lang)
        except Exception as err:
            self.output_handlers['error'](f"Skipping file {fname}: {err}")
            return []
        
        scm_fname = get_scm_fname(lang)
        if not scm_fname:
            return []
        
        code = self.read_text_func_internal(fname)
        if not code:
            return []
        
        try:
            tree = parser.parse(bytes(code, "utf-8"))
            
            # Load query from SCM file
            query_text = read_text(scm_fname, silent=True)
            if not query_text:
                return []
            
            query = language.query(query_text)

            # tree-sitter 0.25+ moved captures to QueryCursor
            try:
                captures = query.captures(tree.root_node)
            except AttributeError:
                import tree_sitter
                cursor = tree_sitter.QueryCursor(query)
                captures = cursor.captures(tree.root_node)

            tags = []
            for capture_name, nodes in captures.items():
                for node in nodes:
                    if capture_name.startswith("name.definition"):
                        kind = "def"
                    elif capture_name.startswith("name.reference"):
                        kind = "ref"
                    else:
                        continue

                    line_num = node.start_point[0] + 1
                    name = node.text.decode('utf-8')

                    tags.append(Tag(
                        rel_fname=rel_fname,
                        fname=fname,
                        line=line_num,
                        name=name,
                        kind=kind
                    ))
            
            return tags
            
        except Exception as e:
            self.output_handlers['error'](f"Error parsing {fname}: {e}")
            return []
    
    @staticmethod
    def _pagerank(G, alpha=0.85, max_iter=100, tol=1e-6, personalization=None):
        """Pure-Python PageRank (no scipy/numpy needed)."""
        nodes = list(G.nodes())
        if not nodes:
            return {}
        n = len(nodes)
        idx = {node: i for i, node in enumerate(nodes)}

        # Initial scores
        if personalization:
            total = sum(personalization.get(nd, 0.0) for nd in nodes)
            scores = [(personalization.get(nd, 0.0) / total if total else 1.0 / n) for nd in nodes]
        else:
            scores = [1.0 / n] * n

        # Precompute out-edges per node
        out_edges = [[] for _ in range(n)]
        for u, v in G.edges():
            out_edges[idx[u]].append(idx[v])

        out_degree = [len(out_edges[i]) for i in range(n)]
        teleport = scores[:]  # reuse initial as teleport distribution

        for _ in range(max_iter):
            new_scores = [0.0] * n
            dangling_sum = sum(scores[i] for i in range(n) if out_degree[i] == 0)

            for i in range(n):
                if out_degree[i] > 0:
                    share = scores[i] / out_degree[i]
                    for j in out_edges[i]:
                        new_scores[j] += share

            for i in range(n):
                new_scores[i] = alpha * (new_scores[i] + dangling_sum * teleport[i]) + (1 - alpha) * teleport[i]

            # Check convergence
            diff = sum(abs(new_scores[i] - scores[i]) for i in range(n))
            scores = new_scores
            if diff < tol:
                break

        # Scale to readable values (max=100)
        max_score = max(scores) if scores else 1.0
        scale = 100.0 / max_score if max_score > 0 else 1.0
        return {nodes[i]: scores[i] * scale for i in range(n)}

    def get_ranked_tags(
        self,
        focus_fnames: List[str],
        context_fnames: List[str],
        mentioned_fnames: Optional[Set[str]] = None,
        mentioned_idents: Optional[Set[str]] = None
    ) -> List[Tuple[float, Tag]]:
        """Get ranked tags using PageRank algorithm."""
        if mentioned_fnames is None:
            mentioned_fnames = set()
        if mentioned_idents is None:
            mentioned_idents = set()
        
        # Collect all tags
        defines = defaultdict(set)
        references = defaultdict(set)
        definitions = defaultdict(set)
        
        personalization = {}
        focus_rel_fnames = set(self.get_rel_fname(f) for f in focus_fnames)
        
        all_fnames = list(set(focus_fnames + context_fnames))
        
        for fname in all_fnames:
            rel_fname = self.get_rel_fname(fname)
            
            if not os.path.exists(fname):
                self.output_handlers['warning'](f"Repo-map can't include {fname}")
                continue
            
            tags = self.get_tags(fname, rel_fname)
            
            for tag in tags:
                if tag.kind == "def":
                    defines[tag.name].add(rel_fname)
                    definitions[rel_fname].add(tag.name)
                elif tag.kind == "ref":
                    references[tag.name].add(rel_fname)
            
            # Set personalization for chat files
            if fname in focus_fnames:
                personalization[rel_fname] = 100.0
        
        # Build graph
        G = nx.MultiDiGraph()
        
        # Add nodes
        for fname in all_fnames:
            rel_fname = self.get_rel_fname(fname)
            G.add_node(rel_fname)
        
        # Add edges based on references
        for name, ref_fnames in references.items():
            def_fnames = defines.get(name, set())
            for ref_fname in ref_fnames:
                for def_fname in def_fnames:
                    if ref_fname != def_fname:
                        G.add_edge(ref_fname, def_fname, name=name)
        
        if not G.nodes():
            return []
        
        # Run PageRank (pure-Python to avoid scipy dependency)
        ranks = self._pagerank(G, personalization=personalization or None)
        
        # Collect and rank tags
        ranked_tags = []
        ranked_files = set()

        for fname in all_fnames:
            rel_fname = self.get_rel_fname(fname)
            if not os.path.exists(fname):
                continue
            
            tags = self.get_tags(fname, rel_fname)
            file_rank = ranks.get(rel_fname, 0.0)

            # Exclude files with Page Rank 0 if exclude_unranked is True
            if self.exclude_unranked and file_rank == 0.0:
                continue
            
            for tag in tags:
                if tag.kind == "def":
                    boost = 1.0
                    if tag.name in mentioned_idents:
                        boost *= 10.0
                    if rel_fname in mentioned_fnames:
                        boost *= 5.0
                    if rel_fname in focus_rel_fnames:
                        boost *= 20.0

                    final_rank = file_rank * boost
                    ranked_tags.append((final_rank, tag))
                    ranked_files.add(rel_fname)

        ranked_tags.sort(key=lambda x: x[0], reverse=True)
        self.ranked_file_count = len(ranked_files)
        return ranked_tags
    
    def render_tree(self, abs_fname: str, rel_fname: str, lois: List[int]) -> str:
        """Render a code snippet with specific lines of interest."""
        code = self.read_text_func_internal(abs_fname)
        if not code:
            return ""
        
        # Use TreeContext for rendering
        try:
            if rel_fname not in self.tree_context_cache:
                self.tree_context_cache[rel_fname] = TreeContext(
                    rel_fname,
                    code,
                    color=False
                )
            
            tree_context = self.tree_context_cache[rel_fname]
            return tree_context.format(lois)
        except Exception:
            # Fallback to simple line extraction
            lines = code.splitlines()
            result_lines = [f"{rel_fname}:"]
            
            for loi in sorted(set(lois)):
                if 1 <= loi <= len(lines):
                    result_lines.append(f"{loi:4d}: {lines[loi-1]}")
            
            return "\n".join(result_lines)
    
    def to_tree(self, tags: List[Tuple[float, Tag]], focus_rel_fnames: Set[str]) -> str:
        """Convert ranked tags to formatted tree output."""
        if not tags:
            return ""
        
        # Group tags by file
        file_tags = defaultdict(list)
        for rank, tag in tags:
            file_tags[tag.rel_fname].append((rank, tag))
        
        # Sort files by importance (max rank of their tags)
        sorted_files = sorted(
            file_tags.items(),
            key=lambda x: max(rank for rank, tag in x[1]),
            reverse=True
        )
        
        tree_parts = []
        
        for rel_fname, file_tag_list in sorted_files:
            # Get lines of interest
            lois = [tag.line for rank, tag in file_tag_list]
            
            # Find absolute filename
            abs_fname = str(self.root / rel_fname)
            
            # Get the max rank for the file
            max_rank = max(rank for rank, tag in file_tag_list)
            
            # Render the tree for this file
            rendered = self.render_tree(abs_fname, rel_fname, lois)
            if rendered:
                # Add rank value to the output
                rendered_lines = rendered.splitlines()
                first_line = rendered_lines[0]
                code_lines = rendered_lines[1:]
                
                tree_parts.append(
                    f"{first_line}\n"
                    f"(Rank value: {max_rank:.4f})\n\n" # Added an extra newline here
                    + "\n".join(code_lines)
                )
        
        return "\n\n".join(tree_parts)
    
    def get_ranked_tags_map(
        self,
        focus_fnames: List[str],
        context_fnames: List[str],
        max_map_tokens: int,
        mentioned_fnames: Optional[Set[str]] = None,
        mentioned_idents: Optional[Set[str]] = None,
        force_refresh: bool = False
    ) -> Optional[str]:
        """Get the ranked tags map with caching."""
        cache_key = (
            tuple(sorted(focus_fnames)),
            tuple(sorted(context_fnames)),
            max_map_tokens,
            tuple(sorted(mentioned_fnames or [])),
            tuple(sorted(mentioned_idents or [])),
        )
        
        if not force_refresh and cache_key in self.map_cache:
            return self.map_cache[cache_key]
        
        result = self.get_ranked_tags_map_uncached(
            focus_fnames, context_fnames, max_map_tokens,
            mentioned_fnames, mentioned_idents
        )
        
        self.map_cache[cache_key] = result
        return result
    
    def get_ranked_tags_map_uncached(
        self,
        focus_fnames: List[str],
        context_fnames: List[str],
        max_map_tokens: int,
        mentioned_fnames: Optional[Set[str]] = None,
        mentioned_idents: Optional[Set[str]] = None
    ) -> Optional[str]:
        """Generate the ranked tags map without caching."""
        ranked_tags = self.get_ranked_tags(
            focus_fnames, context_fnames, mentioned_fnames, mentioned_idents
        )
        
        if not ranked_tags:
            return None
        
        # Filter important files
        important_files = filter_important_files(
            [self.get_rel_fname(f) for f in context_fnames]
        )
        
        # Binary search to find the right number of tags
        focus_rel_fnames = set(self.get_rel_fname(f) for f in focus_fnames)
        
        def try_tags(num_tags: int) -> Tuple[Optional[str], int]:
            if num_tags <= 0:
                return None, 0
            
            selected_tags = ranked_tags[:num_tags]
            tree_output = self.to_tree(selected_tags, focus_rel_fnames)
            
            if not tree_output:
                return None, 0
            
            tokens = self.token_count(tree_output)
            return tree_output, tokens
        
        # Binary search for optimal number of tags
        left, right = 0, len(ranked_tags)
        best_tree = None
        
        while left <= right:
            mid = (left + right) // 2
            tree_output, tokens = try_tags(mid)
            
            if tree_output and tokens <= max_map_tokens:
                best_tree = tree_output
                left = mid + 1
            else:
                right = mid - 1
        
        return best_tree
    
    def get_repo_map(
        self,
        focus_files: List[str] = None,
        context_files: List[str] = None,
        mentioned_fnames: Optional[Set[str]] = None,
        mentioned_idents: Optional[Set[str]] = None,
        force_refresh: bool = False
    ) -> Optional[str]:
        """Generate the repository map."""
        if focus_files is None:
            focus_files = []
        if context_files is None:
            context_files = []
        
        if self.max_map_tokens <= 0 or not context_files:
            return None
        
        # Adjust max_map_tokens if no chat files
        max_map_tokens = self.max_map_tokens
        if not focus_files and self.max_context_window:
            padding = 1024
            available = self.max_context_window - padding
            max_map_tokens = min(
                max_map_tokens * self.map_mul_no_files,
                available
            )
        
        try:
            files_listing = self.get_ranked_tags_map(
                focus_files, context_files, max_map_tokens,
                mentioned_fnames, mentioned_idents, force_refresh
            )
        except RecursionError:
            self.output_handlers['error']("Disabling repo map, git repo too large?")
            self.max_map_tokens = 0
            return None
        
        if not files_listing:
            print("files_listing is None")
            return None
        
        if self.verbose:
            tokens = self.token_count(files_listing)
            self.output_handlers['info'](f"Repo-map: {tokens / 1024:.1f} k-tokens")
        
        # Format final output
        other = "context " if focus_files else ""
        
        if self.repo_content_prefix:
            repo_content = self.repo_content_prefix.format(other=other)
        else:
            repo_content = ""
        
        repo_content += files_listing
        
        return repo_content
