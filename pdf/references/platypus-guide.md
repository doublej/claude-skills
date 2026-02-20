# Platypus Guide

High-level document layout with ReportLab Platypus.

Platypus = "Page Layout and Typography Using Scripts"

## Core Concepts

| Component | Purpose |
|-----------|---------|
| **Flowables** | Content blocks (paragraphs, tables, images) |
| **Frames** | Rectangular areas that hold flowables |
| **PageTemplates** | Define frame layouts for pages |
| **DocTemplate** | Manages document structure |

## Simple Document

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

## Flowables Reference

```python
from reportlab.platypus import (
    Paragraph,      # Formatted text
    Spacer,         # Vertical space
    Table,          # Data tables
    TableStyle,     # Table formatting
    Image,          # Images
    PageBreak,      # Force new page
    KeepTogether,   # Prevent page breaks within
    ListFlowable,   # Bullet/numbered lists
    HRFlowable,     # Horizontal rule
)
```

## Paragraph Styles

```python
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY

styles = getSampleStyleSheet()

# Built-in styles
styles['Normal']
styles['Heading1']
styles['Heading2']
styles['Title']
styles['BodyText']
styles['Code']

# Custom style
custom = ParagraphStyle(
    'CustomStyle',
    parent=styles['Normal'],
    fontSize=11,
    leading=14,           # Line height
    textColor=HexColor('#333333'),
    alignment=TA_JUSTIFY,
    spaceAfter=12,
    spaceBefore=6,
    leftIndent=20,
    rightIndent=20,
    firstLineIndent=20,
    fontName='Helvetica',
)
```

## Paragraph HTML-like Tags

```python
text = """
<b>Bold</b> and <i>italic</i> and <u>underline</u><br/>
<font size="14" color="red">Colored text</font><br/>
<a href="https://example.com">Link</a><br/>
<sub>subscript</sub> and <super>superscript</super>
"""
story.append(Paragraph(text, styles['Normal']))
```

## Tables

### Basic Table

```python
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

data = [
    ['Name', 'Age', 'City'],
    ['Alice', '30', 'New York'],
    ['Bob', '25', 'Los Angeles'],
]

table = Table(data)
story.append(table)
```

### Table Styling

```python
data = [
    ['Product', 'Qty', 'Price', 'Total'],
    ['Widget A', '10', '$5.00', '$50.00'],
    ['Widget B', '5', '$8.00', '$40.00'],
    ['', '', 'Total:', '$90.00'],
]

table = Table(data, colWidths=[200, 60, 80, 80])

style = TableStyle([
    # Header row
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

    # Body rows
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),

    # Alternating row colors
    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#D6DCE5')),

    # Grid
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

    # Padding
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
])

table.setStyle(style)
```

### TableStyle Commands

| Command | Description |
|---------|-------------|
| `BACKGROUND` | Cell background |
| `TEXTCOLOR` | Text color |
| `FONTNAME` | Font family |
| `FONTSIZE` | Font size in points |
| `ALIGN` | LEFT/CENTER/RIGHT |
| `VALIGN` | TOP/MIDDLE/BOTTOM |
| `GRID` | Full grid |
| `BOX` | Outer border |
| `INNERGRID` | Inner lines only |
| `LINEABOVE/BELOW` | Top/bottom border |
| `LINEBEFORE/AFTER` | Left/right border |
| `TOPPADDING` | Top cell padding |
| `BOTTOMPADDING` | Bottom cell padding |
| `SPAN` | Merge cells |

### Cell Coordinates

```
(0, 0) = top-left cell
(-1, 0) = top-right cell
(0, -1) = bottom-left cell
(-1, -1) = bottom-right cell
```

### Spanning Cells

```python
table.setStyle(TableStyle([
    ('SPAN', (0, 0), (3, 0)),  # Span first row across all columns
]))
```

### Nested Content in Tables

```python
data = [
    ['Description', 'Image'],
    [
        Paragraph('This is <b>formatted</b> text', styles['Normal']),
        Image('photo.jpg', width=100, height=75)
    ],
]
table = Table(data, colWidths=[300, 120])
```

## Headers and Footers

```python
from reportlab.lib.pagesizes import A4

def header_footer(canvas, doc):
    canvas.saveState()

    # Header
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(72, A4[1] - 50, "Company Name")
    canvas.drawRightString(A4[0] - 72, A4[1] - 50, "Report Title")

    # Footer
    canvas.setFont('Helvetica', 9)
    canvas.drawCentredString(A4[0] / 2, 40, f"Page {doc.page}")

    canvas.restoreState()

doc = SimpleDocTemplate(
    "output.pdf",
    pagesize=A4,
    topMargin=80,
    bottomMargin=70,
)

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
```

## Multi-Column Layout

```python
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

doc = BaseDocTemplate("multicolumn.pdf", pagesize=A4)

frame_left = Frame(72, 72, 240, 700, id='left')
frame_right = Frame(330, 72, 240, 700, id='right')

template = PageTemplate(
    id='TwoColumn',
    frames=[frame_left, frame_right],
    onPage=header_footer
)

doc.addPageTemplates([template])
doc.build(story)
```
