# Python Color Workflows for PDFs

## Batch Color Conversion with Ghostscript

### Convert Directory of PDFs to CMYK

```python
import subprocess
from pathlib import Path

def convert_to_cmyk(
    input_dir: Path,
    output_dir: Path,
    icc_profile: str = "ISOcoated_v2_300_eci.icc",
):
    output_dir.mkdir(parents=True, exist_ok=True)
    for pdf in input_dir.glob("*.pdf"):
        out = output_dir / pdf.name
        subprocess.run([
            "gs", "-dBATCH", "-dNOPAUSE", "-dQUIET",
            "-sDEVICE=pdfwrite",
            "-sColorConversionStrategy=CMYK",
            "-dProcessColorModel=/DeviceCMYK",
            "-dOverrideICC=true",
            f"-sOutputICCProfile={icc_profile}",
            "-dRenderIntent=1",
            "-dDeviceGrayToK=true",
            f"-sOutputFile={out}",
            str(pdf),
        ], check=True)
        print(f"Converted: {pdf.name}")
```

### Batch Ink Coverage Report

```python
import subprocess
import re
from pathlib import Path

def ink_coverage_report(pdf_path: Path) -> list[dict]:
    result = subprocess.run(
        ["gs", "-dBATCH", "-dNOPAUSE", "-dQUIET", "-sDEVICE=inkcov", str(pdf_path)],
        capture_output=True, text=True,
    )
    pages = []
    for line in result.stdout.splitlines():
        match = re.match(r"\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+CMYK OK", line)
        if match:
            c, m, y, k = (float(v) for v in match.groups())
            pages.append({"C": c, "M": m, "Y": y, "K": k, "total": c + m + y + k})
    return pages

# Flag pages exceeding ink limit
for page_num, ink in enumerate(ink_coverage_report(Path("input.pdf")), 1):
    if ink["total"] > 3.0:  # 300%
        print(f"Page {page_num}: total ink {ink['total']:.1%} exceeds 300%")
```

## pikepdf Advanced Usage

### Extract All ICC Profiles from a PDF

```python
import pikepdf

def extract_all_icc_profiles(pdf_path: str, output_dir: str = "."):
    pdf = pikepdf.open(pdf_path)
    count = 0

    # Output intent profiles
    for intent in pdf.Root.get("/OutputIntents", []):
        profile = intent.get("/DestOutputProfile")
        if profile:
            data = bytes(profile.read_bytes())
            path = f"{output_dir}/output_intent_{count}.icc"
            with open(path, "wb") as f:
                f.write(data)
            count += 1

    # Per-page color space profiles
    for page_num, page in enumerate(pdf.pages):
        resources = page.get("/Resources", {})
        color_spaces = resources.get("/ColorSpace", {})
        for name, cs in dict(color_spaces).items():
            if isinstance(cs, pikepdf.Array) and len(cs) >= 2:
                if str(cs[0]) == "/ICCBased":
                    profile_stream = cs[1]
                    data = bytes(profile_stream.read_bytes())
                    path = f"{output_dir}/page{page_num}_{name}_{count}.icc"
                    with open(path, "wb") as f:
                        f.write(data)
                    count += 1

    return count
```

### Audit Color Spaces in a PDF

```python
import pikepdf

def audit_color_spaces(pdf_path: str) -> dict:
    pdf = pikepdf.open(pdf_path)
    report = {"output_intents": [], "pages": []}

    # Output intents
    for intent in pdf.Root.get("/OutputIntents", []):
        info = {
            "subtype": str(intent.get("/S", "")),
            "condition_id": str(intent.get("/OutputConditionIdentifier", "")),
            "has_profile": "/DestOutputProfile" in intent,
        }
        if info["has_profile"]:
            profile = intent["/DestOutputProfile"]
            info["num_components"] = int(profile.get("/N", 0))
        report["output_intents"].append(info)

    # Per-page analysis
    for i, page in enumerate(pdf.pages):
        page_info = {"page": i + 1, "color_spaces": set()}
        resources = page.get("/Resources", {})

        # Named color spaces
        for name, cs in dict(resources.get("/ColorSpace", {})).items():
            if isinstance(cs, pikepdf.Name):
                page_info["color_spaces"].add(str(cs))
            elif isinstance(cs, pikepdf.Array) and len(cs) > 0:
                page_info["color_spaces"].add(str(cs[0]))

        # Image color spaces
        for name, xobj in dict(resources.get("/XObject", {})).items():
            if xobj.get("/Subtype") == "/Image":
                cs = xobj.get("/ColorSpace")
                if isinstance(cs, pikepdf.Name):
                    page_info["color_spaces"].add(str(cs))
                elif isinstance(cs, pikepdf.Array) and len(cs) > 0:
                    page_info["color_spaces"].add(str(cs[0]))

        page_info["color_spaces"] = sorted(page_info["color_spaces"])
        report["pages"].append(page_info)

    return report
```

### Replace Output Intent Profile

```python
import pikepdf

def replace_output_intent(
    pdf_path: str,
    new_profile_path: str,
    output_path: str,
    condition_id: str = "Custom",
    subtype: str = "/GTS_PDFA1",
):
    pdf = pikepdf.open(pdf_path)

    with open(new_profile_path, "rb") as f:
        icc_data = f.read()

    icc_stream = pdf.make_stream(icc_data)
    # Detect N from profile header (byte 16-19 = color space)
    color_space = icc_data[16:20].decode("ascii").strip()
    n_map = {"RGB": 3, "CMYK": 4, "GRAY": 1}
    icc_stream["/N"] = n_map.get(color_space, 3)

    intent = pikepdf.Dictionary({
        "/Type": pikepdf.Name("/OutputIntent"),
        "/S": pikepdf.Name(subtype),
        "/OutputConditionIdentifier": condition_id,
        "/DestOutputProfile": icc_stream,
    })

    pdf.Root["/OutputIntents"] = pikepdf.Array([intent])
    pdf.save(output_path)
```

## img2pdf Integration

### Create PDF from Images with ICC Profile

```python
import img2pdf
from pathlib import Path

def images_to_pdf(
    image_paths: list[Path],
    output_path: str,
    icc_profile_path: str | None = None,
):
    """Convert images to PDF, optionally embedding an ICC profile."""
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert([str(p) for p in image_paths]))

    # img2pdf doesn't embed ICC output intents;
    # use pikepdf to add one after creation
    if icc_profile_path:
        import pikepdf
        pdf = pikepdf.open(output_path, allow_overwriting_input=True)

        with open(icc_profile_path, "rb") as pf:
            icc_data = pf.read()

        icc_stream = pdf.make_stream(icc_data)
        color_space = icc_data[16:20].decode("ascii").strip()
        n_map = {"RGB": 3, "CMYK": 4, "GRAY": 1}
        icc_stream["/N"] = n_map.get(color_space, 3)

        intent = pikepdf.Dictionary({
            "/Type": pikepdf.Name("/OutputIntent"),
            "/S": pikepdf.Name("/GTS_PDFA1"),
            "/OutputConditionIdentifier": color_space,
            "/DestOutputProfile": icc_stream,
        })
        pdf.Root["/OutputIntents"] = pikepdf.Array([intent])
        pdf.save(output_path)
```

## PDF/A Compliance with Python

### Check and Fix Output Intent for PDF/A

```python
import pikepdf
from pathlib import Path

def ensure_pdfa_output_intent(
    pdf_path: str,
    output_path: str,
    srgb_profile_path: str = "sRGB.icc",
):
    """Add sRGB output intent if missing (required for PDF/A)."""
    pdf = pikepdf.open(pdf_path)

    intents = pdf.Root.get("/OutputIntents", pikepdf.Array())
    if len(intents) > 0:
        print("Output intent already present")
        pdf.save(output_path)
        return

    with open(srgb_profile_path, "rb") as f:
        icc_data = f.read()

    icc_stream = pdf.make_stream(icc_data)
    icc_stream["/N"] = 3

    intent = pikepdf.Dictionary({
        "/Type": pikepdf.Name("/OutputIntent"),
        "/S": pikepdf.Name("/GTS_PDFA1"),
        "/OutputConditionIdentifier": "sRGB IEC61966-2.1",
        "/DestOutputProfile": icc_stream,
    })

    pdf.Root["/OutputIntents"] = pikepdf.Array([intent])
    pdf.save(output_path)
    print(f"Added sRGB output intent to {output_path}")
```

### Validate with veraPDF (subprocess)

```python
import subprocess
import json

def validate_pdfa(pdf_path: str, flavour: str = "2b") -> dict:
    result = subprocess.run(
        ["verapdf", "--format", "json", f"--flavour", flavour, pdf_path],
        capture_output=True, text=True,
    )
    return json.loads(result.stdout) if result.stdout else {"error": result.stderr}
```

## Pillow/pyCMS Batch Workflow

### Batch Convert Images RGB to CMYK

```python
from pathlib import Path
from PIL import Image, ImageCms

def batch_rgb_to_cmyk(
    input_dir: Path,
    output_dir: Path,
    cmyk_profile_path: str,
    intent: int = ImageCms.Intent.RELATIVE_COLORIMETRIC,
):
    output_dir.mkdir(parents=True, exist_ok=True)
    srgb = ImageCms.createProfile("sRGB")
    cmyk = ImageCms.getOpenProfile(cmyk_profile_path)
    transform = ImageCms.buildTransform(srgb, cmyk, "RGB", "CMYK", intent)

    for img_path in input_dir.glob("*"):
        if img_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".tiff", ".tif"}:
            continue
        img = Image.open(img_path).convert("RGB")
        cmyk_img = ImageCms.applyTransform(img, transform)
        out = output_dir / f"{img_path.stem}_cmyk.tiff"
        cmyk_img.save(out)
        print(f"Converted: {img_path.name} -> {out.name}")
```

### Inspect ICC Profile Metadata

```python
from PIL import ImageCms

def profile_info(icc_path: str) -> dict:
    profile = ImageCms.getOpenProfile(icc_path)
    return {
        "description": ImageCms.getProfileDescription(profile),
        "color_space": profile.profile.xcolor_space,
        "pcs": profile.profile.connection_space,
        "manufacturer": ImageCms.getProfileManufacturer(profile),
        "model": ImageCms.getProfileModel(profile),
        "copyright": ImageCms.getProfileCopyright(profile),
        "version": profile.profile.version,
        "device_class": profile.profile.device_class,
    }
```
