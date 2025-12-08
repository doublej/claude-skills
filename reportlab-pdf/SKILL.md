---
name: reportlab-pdf
description: Comprehensive guide to ReportLab PDF generation in Python. Covers Canvas API, Platypus layouts, tables, graphics, fonts, and images. Use when creating PDFs programmatically, building reports, generating documents with tables/charts, or working with complex page layouts.
---

# ReportLab PDF Skill

Comprehensive guide for generating PDFs with ReportLab 4.x in Python.

## When to Use

- Creating PDFs programmatically from Python
- Building reports with tables, charts, and formatted text
- Generating invoices, certificates, or data-driven documents
- Drawing vector graphics and shapes
- Complex multi-page layouts with headers/footers

## Current Version

- **Latest Stable**: ReportLab 4.4.5
- **Python Support**: 3.9 - 3.13
- **License**: BSD

## Installation

```bash
uv add reportlab
# or
pip install reportlab
```

## Architecture Overview

ReportLab has two main APIs:

| API | Level | Use Case |
|-----|-------|----------|
| **Canvas** | Low-level | Direct PDF drawing, absolute positioning |
| **Platypus** | High-level | Document templates, flowable content |

**Rule of thumb:** Use Platypus for documents, Canvas for custom graphics.

## Canvas API (Low-Level)

The Canvas is a graphics state machine for direct PDF generation.

### Basic Canvas Usage

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Create PDF
c = canvas.Canvas("output.pdf", pagesize=A4)
width, height = A4  # 595.27, 841.89 points (1 point = 1/72 inch)

# Draw text
c.drawString(100, 750, "Hello, ReportLab!")

# Save page and finish
c.showPage()
c.save()
```

### Coordinate System

- Origin (0, 0) is **bottom-left**
- Y increases upward
- Units are points (1/72 inch)
- A4 = 595.27 x 841.89 points
- Letter = 612 x 792 points

```python
from reportlab.lib.units import inch, cm, mm

# Use units for clarity
c.drawString(1*inch, 10*inch, "One inch from left, 10 inches up")
c.drawString(2.5*cm, 20*cm, "Using centimeters")
```

### Text Operations

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas("text.pdf", pagesize=A4)

# Set font (must call before drawing text)
c.setFont("Helvetica", 12)
c.drawString(100, 700, "Regular text")

c.setFont("Helvetica-Bold", 14)
c.drawString(100, 680, "Bold text")

c.setFont("Helvetica-Oblique", 12)
c.drawString(100, 660, "Italic text")

# Text alignment
c.drawString(100, 640, "Left aligned (default)")
c.drawRightString(500, 620, "Right aligned")
c.drawCentredString(300, 600, "Centered")

# Rotated text
c.saveState()
c.translate(100, 500)
c.rotate(45)
c.drawString(0, 0, "Rotated 45 degrees")
c.restoreState()

c.showPage()
c.save()
```

### Built-in Fonts

Always available (no embedding needed):

```
Helvetica, Helvetica-Bold, Helvetica-Oblique, Helvetica-BoldOblique
Times-Roman, Times-Bold, Times-Italic, Times-BoldItalic
Courier, Courier-Bold, Courier-Oblique, Courier-BoldOblique
Symbol, ZapfDingbats
```

### Custom Fonts (TTF)

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register font
pdfmetrics.registerFont(TTFont('MyFont', '/path/to/font.ttf'))

# Use it
c.setFont('MyFont', 12)
c.drawString(100, 700, "Custom font text")
```

### Colors

```python
from reportlab.lib.colors import red, blue, black, HexColor, Color

# Named colors
c.setFillColor(red)
c.setStrokeColor(blue)

# Hex colors
c.setFillColor(HexColor('#FF5733'))

# RGB (0-1 range)
c.setFillColor(Color(0.2, 0.4, 0.6))

# CMYK
from reportlab.lib.colors import CMYKColor
c.setFillColor(CMYKColor(0.1, 0.2, 0.3, 0.1))
```

### Drawing Shapes

```python
# Lines
c.setStrokeColor(black)
c.setLineWidth(1)
c.line(100, 700, 400, 700)  # x1, y1, x2, y2

# Rectangles
c.rect(100, 600, 200, 80)  # x, y, width, height (stroke only)
c.rect(100, 500, 200, 80, fill=1)  # filled

# Rounded rectangles
c.roundRect(100, 400, 200, 80, 10)  # radius=10

# Circles and ellipses
c.circle(200, 350, 40)  # x_center, y_center, radius
c.ellipse(100, 250, 300, 300)  # x1, y1, x2, y2 (bounding box)

# Wedge (pie slice)
c.wedge(100, 150, 200, 250, 0, 90, fill=1)  # x1,y1,x2,y2, startAngle, extent
```

### Paths (Complex Shapes)

```python
from reportlab.graphics.shapes import Path

p = c.beginPath()
p.moveTo(100, 100)
p.lineTo(200, 200)
p.lineTo(150, 250)
p.curveTo(100, 300, 50, 250, 100, 200)  # Bezier curve
p.close()

c.drawPath(p, fill=1, stroke=1)
```

### Images

```python
# Draw image at position
c.drawImage("photo.jpg", 100, 500, width=200, height=150)

# Preserve aspect ratio
c.drawImage("photo.jpg", 100, 300, width=200, preserveAspectRatio=True)

# With mask (transparency)
c.drawImage("logo.png", 100, 100, mask='auto')
```

### State Management

```python
# Save state before transformations
c.saveState()

c.translate(100, 100)  # Move origin
c.rotate(45)           # Rotate
c.scale(2, 2)          # Scale

c.drawString(0, 0, "Transformed text")

# Restore original state
c.restoreState()
```

## Platypus (High-Level API)

Platypus = "Page Layout and Typography Using Scripts"

### Core Concepts

| Component | Purpose |
|-----------|---------|
| **Flowables** | Content blocks (paragraphs, tables, images) |
| **Frames** | Rectangular areas that hold flowables |
| **PageTemplates** | Define frame layouts for pages |
| **DocTemplate** | Manages document structure |

### Simple Document

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("output.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = []

# Add content
story.append(Paragraph("This is a heading", styles['Heading1']))
story.append(Spacer(1, 12))
story.append(Paragraph("This is body text. " * 50, styles['Normal']))

# Build PDF
doc.build(story)
```

### Flowables Reference

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

### Paragraph Styles

```python
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY

styles = getSampleStyleSheet()

# Use built-in styles
styles['Normal']
styles['Heading1']
styles['Heading2']
styles['Title']
styles['BodyText']
styles['Code']

# Create custom style
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

story.append(Paragraph("Custom styled text", custom))
```

### Paragraph HTML-like Tags

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

Tables are the most powerful Platypus feature.

### Basic Table

```python
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

data = [
    ['Name', 'Age', 'City'],
    ['Alice', '30', 'New York'],
    ['Bob', '25', 'Los Angeles'],
    ['Charlie', '35', 'Chicago'],
]

table = Table(data)
story.append(table)
```

### Table Styling

```python
from reportlab.lib import colors

data = [
    ['Product', 'Qty', 'Price', 'Total'],
    ['Widget A', '10', '$5.00', '$50.00'],
    ['Widget B', '5', '$8.00', '$40.00'],
    ['Widget C', '20', '$2.50', '$50.00'],
    ['', '', 'Total:', '$140.00'],
]

table = Table(data, colWidths=[200, 60, 80, 80])

style = TableStyle([
    # Header row
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

    # Body rows
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),  # Right-align numbers

    # Alternating row colors
    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#D6DCE5')),
    ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#D6DCE5')),

    # Grid
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

    # Total row bold
    ('FONTNAME', (2, -1), (-1, -1), 'Helvetica-Bold'),

    # Padding
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
])

table.setStyle(style)
story.append(table)
```

### TableStyle Commands

| Command | Parameters | Description |
|---------|------------|-------------|
| `BACKGROUND` | color | Cell background |
| `TEXTCOLOR` | color | Text color |
| `FONTNAME` | font name | Font family |
| `FONTSIZE` | size | Font size in points |
| `ALIGN` | LEFT/CENTER/RIGHT | Horizontal alignment |
| `VALIGN` | TOP/MIDDLE/BOTTOM | Vertical alignment |
| `GRID` | width, color | Full grid |
| `BOX` | width, color | Outer border |
| `INNERGRID` | width, color | Inner lines only |
| `LINEABOVE` | width, color | Top border |
| `LINEBELOW` | width, color | Bottom border |
| `LINEBEFORE` | width, color | Left border |
| `LINEAFTER` | width, color | Right border |
| `TOPPADDING` | points | Top cell padding |
| `BOTTOMPADDING` | points | Bottom cell padding |
| `LEFTPADDING` | points | Left cell padding |
| `RIGHTPADDING` | points | Right cell padding |
| `SPAN` | (col, row) | Merge cells |

### Cell Coordinates

```
(0, 0) = top-left cell
(-1, 0) = top-right cell
(0, -1) = bottom-left cell
(-1, -1) = bottom-right cell
```

### Spanning Cells

```python
data = [
    ['Header Spanning All Columns', '', '', ''],
    ['Col 1', 'Col 2', 'Col 3', 'Col 4'],
    ['A', 'B', 'C', 'D'],
]

table = Table(data)
table.setStyle(TableStyle([
    ('SPAN', (0, 0), (3, 0)),  # Span first row across all columns
    ('ALIGN', (0, 0), (3, 0), 'CENTER'),
    ('BACKGROUND', (0, 0), (3, 0), colors.grey),
]))
```

### Nested Content in Tables

```python
from reportlab.platypus import Paragraph, Image

data = [
    ['Description', 'Image'],
    [
        Paragraph('This is <b>formatted</b> text in a cell', styles['Normal']),
        Image('photo.jpg', width=100, height=75)
    ],
]

table = Table(data, colWidths=[300, 120])
```

## Page Templates

For complex layouts with headers, footers, and multiple frames.

### Headers and Footers

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import A4

def header_footer(canvas, doc):
    canvas.saveState()

    # Header
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(72, A4[1] - 50, "Company Name")
    canvas.drawRightString(A4[0] - 72, A4[1] - 50, "Report Title")

    # Header line
    canvas.setStrokeColor(colors.grey)
    canvas.line(72, A4[1] - 60, A4[0] - 72, A4[1] - 60)

    # Footer
    canvas.setFont('Helvetica', 9)
    canvas.drawString(72, 40, f"Generated: {datetime.now():%Y-%m-%d}")
    canvas.drawCentredString(A4[0] / 2, 40, f"Page {doc.page}")
    canvas.drawRightString(A4[0] - 72, 40, "Confidential")

    # Footer line
    canvas.line(72, 55, A4[0] - 72, 55)

    canvas.restoreState()

doc = SimpleDocTemplate(
    "output.pdf",
    pagesize=A4,
    topMargin=80,      # Space for header
    bottomMargin=70,   # Space for footer
)

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
```

### Multi-Column Layout

```python
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

doc = BaseDocTemplate("multicolumn.pdf", pagesize=A4)

frame_left = Frame(
    72, 72,           # x, y
    240, 700,         # width, height
    id='left'
)

frame_right = Frame(
    330, 72,
    240, 700,
    id='right'
)

template = PageTemplate(
    id='TwoColumn',
    frames=[frame_left, frame_right],
    onPage=header_footer
)

doc.addPageTemplates([template])
doc.build(story)
```

## Graphics with ReportLab Graphics

For charts and complex vector graphics.

### Drawing Object

```python
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String
from reportlab.graphics import renderPDF

# Create drawing
d = Drawing(400, 200)

# Add shapes
d.add(Rect(10, 10, 100, 80, fillColor=colors.lightblue, strokeColor=colors.blue))
d.add(Circle(200, 100, 50, fillColor=colors.pink))
d.add(Line(10, 150, 390, 150, strokeColor=colors.grey))
d.add(String(150, 170, "Title", fontSize=16, fillColor=colors.black))

# Save as PDF
renderPDF.drawToFile(d, "graphic.pdf", "My Drawing")

# Or add to Platypus story
story.append(d)
```

### Basic Charts

```python
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing

drawing = Drawing(400, 200)

chart = VerticalBarChart()
chart.x = 50
chart.y = 50
chart.height = 125
chart.width = 300

chart.data = [
    [10, 20, 30, 40],   # Series 1
    [15, 25, 35, 45],   # Series 2
]

chart.categoryAxis.categoryNames = ['Q1', 'Q2', 'Q3', 'Q4']
chart.bars[0].fillColor = colors.blue
chart.bars[1].fillColor = colors.red

drawing.add(chart)
story.append(drawing)
```

### Pie Chart

```python
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing

drawing = Drawing(300, 200)

pie = Pie()
pie.x = 100
pie.y = 25
pie.width = 150
pie.height = 150
pie.data = [30, 25, 20, 15, 10]
pie.labels = ['A', 'B', 'C', 'D', 'E']
pie.slices.strokeWidth = 0.5

# Colors for slices
pie.slices[0].fillColor = colors.red
pie.slices[1].fillColor = colors.blue
pie.slices[2].fillColor = colors.green
pie.slices[3].fillColor = colors.yellow
pie.slices[4].fillColor = colors.orange

drawing.add(pie)
story.append(drawing)
```

### Line Chart

```python
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing

drawing = Drawing(400, 200)

chart = HorizontalLineChart()
chart.x = 50
chart.y = 50
chart.height = 125
chart.width = 300

chart.data = [
    [1, 2, 3, 4, 5, 6],
    [1.5, 2.2, 3.1, 3.8, 4.2, 5.0],
]

chart.categoryAxis.categoryNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
chart.lines[0].strokeColor = colors.blue
chart.lines[1].strokeColor = colors.red

drawing.add(chart)
story.append(drawing)
```

## Common Patterns

### Invoice Template

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def create_invoice(filename, invoice_data):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Company header
    story.append(Paragraph("ACME Corporation", styles['Title']))
    story.append(Paragraph("123 Business St, City, State 12345", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))

    # Invoice details
    story.append(Paragraph(f"Invoice #{invoice_data['number']}", styles['Heading1']))
    story.append(Paragraph(f"Date: {invoice_data['date']}", styles['Normal']))
    story.append(Spacer(1, 0.25*inch))

    # Items table
    items = [['Description', 'Qty', 'Unit Price', 'Total']]
    for item in invoice_data['items']:
        items.append([
            item['desc'],
            str(item['qty']),
            f"${item['price']:.2f}",
            f"${item['qty'] * item['price']:.2f}"
        ])

    # Add subtotal, tax, total
    subtotal = sum(i['qty'] * i['price'] for i in invoice_data['items'])
    tax = subtotal * 0.1
    total = subtotal + tax

    items.append(['', '', 'Subtotal:', f"${subtotal:.2f}"])
    items.append(['', '', 'Tax (10%):', f"${tax:.2f}"])
    items.append(['', '', 'Total:', f"${total:.2f}"])

    table = Table(items, colWidths=[250, 60, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -4), 0.5, colors.grey),
        ('FONTNAME', (2, -3), (-1, -1), 'Helvetica-Bold'),
        ('LINEABOVE', (2, -3), (-1, -3), 1, colors.black),
    ]))

    story.append(table)
    doc.build(story)
```

### Report with Multiple Sections

```python
from reportlab.platypus import PageBreak, KeepTogether

def create_report(filename, sections):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    for section in sections:
        # Keep title and first paragraph together
        section_content = [
            Paragraph(section['title'], styles['Heading1']),
            Spacer(1, 12),
            Paragraph(section['content'], styles['Normal']),
        ]
        story.append(KeepTogether(section_content))
        story.append(Spacer(1, 24))

        if section.get('page_break'):
            story.append(PageBreak())

    doc.build(story)
```

### Table of Contents

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents

doc = SimpleDocTemplate("toc.pdf", pagesize=A4)

toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle(name='TOC1', fontSize=14, leftIndent=20, spaceAfter=6),
    ParagraphStyle(name='TOC2', fontSize=12, leftIndent=40, spaceAfter=4),
]

story = []
story.append(Paragraph("Table of Contents", styles['Title']))
story.append(toc)
story.append(PageBreak())

# Add content with bookmarks
story.append(Paragraph("Chapter 1", styles['Heading1']))
doc.addPageTemplates  # This needs multiBuild
```

## Performance Tips

1. **Reuse styles** - Create ParagraphStyle once, use many times
2. **Batch operations** - Build story list fully before calling `doc.build()`
3. **Use Table wisely** - Tables with many rows are expensive; consider splitting
4. **Image optimization** - Pre-resize images; don't rely on ReportLab scaling
5. **Font embedding** - Subset fonts when using custom TTF

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

## Documentation

- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Official Documentation](https://docs.reportlab.com/)
- [PyPI Package](https://pypi.org/project/reportlab/)
