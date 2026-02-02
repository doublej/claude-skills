---
name: reportlab-pdf
description: Comprehensive guide to ReportLab PDF generation in Python. Covers Canvas API, Platypus layouts, tables, graphics, fonts, and images. Use when creating PDFs programmatically, building reports, generating documents with tables/charts, or working with complex page layouts.
---

# ReportLab PDF Skill

Generate PDFs with ReportLab 4.x in Python.

## When to Use

- Creating PDFs programmatically from Python
- Building reports with tables, charts, and formatted text
- Generating invoices, certificates, or data-driven documents
- Drawing vector graphics and shapes
- Complex multi-page layouts with headers/footers

## Version & Installation

```bash
uv add reportlab
# or
pip install reportlab
```

- Latest: ReportLab 4.4.5
- Python: 3.9 - 3.13

## Architecture Overview

| API | Level | Use Case |
|-----|-------|----------|
| **Canvas** | Low-level | Direct PDF drawing, absolute positioning |
| **Platypus** | High-level | Document templates, flowable content |

**Rule of thumb:** Use Platypus for documents, Canvas for custom graphics.

## Canvas Quick Start

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf", pagesize=A4)
width, height = A4  # 595.27, 841.89 points

c.setFont("Helvetica", 12)
c.drawString(100, 750, "Hello, ReportLab!")

c.showPage()
c.save()
```

## Platypus Quick Start

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("output.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("This is a heading", styles['Heading1']))
story.append(Spacer(1, 12))
story.append(Paragraph("This is body text. " * 50, styles['Normal']))

doc.build(story)
```

## Basic Table

```python
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

data = [
    ['Name', 'Age', 'City'],
    ['Alice', '30', 'New York'],
    ['Bob', '25', 'Los Angeles'],
]

table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(table)
```

## Quick Reference

| Task | Method |
|------|--------|
| Create PDF | `canvas.Canvas("file.pdf")` |
| Draw text | `c.drawString(x, y, "text")` |
| Draw line | `c.line(x1, y1, x2, y2)` |
| Draw rectangle | `c.rect(x, y, w, h)` |
| Set font | `c.setFont("Helvetica", 12)` |
| Set color | `c.setFillColor(colors.red)` |
| New page | `c.showPage()` |
| Save PDF | `c.save()` |
| Simple doc | `SimpleDocTemplate("file.pdf")` |
| Add paragraph | `story.append(Paragraph(text, style))` |
| Add table | `story.append(Table(data))` |
| Build doc | `doc.build(story)` |

## Reference Files

- [Canvas API](references/canvas-api.md) - Text, shapes, colors, images, state management
- [Platypus Guide](references/platypus-guide.md) - Flowables, styles, tables, page templates
- [Charts & Patterns](references/charts-patterns.md) - Graphics, charts, invoice template

## Documentation

- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Official Documentation](https://docs.reportlab.com/)
- [PyPI Package](https://pypi.org/project/reportlab/)
