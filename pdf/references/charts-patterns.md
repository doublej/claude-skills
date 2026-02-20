# Charts and Common Patterns

Graphics, charts, and reusable patterns for ReportLab.

## Drawing Object

```python
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String
from reportlab.graphics import renderPDF
from reportlab.lib import colors

d = Drawing(400, 200)

d.add(Rect(10, 10, 100, 80, fillColor=colors.lightblue, strokeColor=colors.blue))
d.add(Circle(200, 100, 50, fillColor=colors.pink))
d.add(Line(10, 150, 390, 150, strokeColor=colors.grey))
d.add(String(150, 170, "Title", fontSize=16, fillColor=colors.black))

# Save as PDF
renderPDF.drawToFile(d, "graphic.pdf", "My Drawing")

# Or add to Platypus story
story.append(d)
```

## Bar Chart

```python
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors

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

## Pie Chart

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

pie.slices[0].fillColor = colors.red
pie.slices[1].fillColor = colors.blue
pie.slices[2].fillColor = colors.green
pie.slices[3].fillColor = colors.yellow
pie.slices[4].fillColor = colors.orange

drawing.add(pie)
story.append(drawing)
```

## Line Chart

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

## Invoice Template

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
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
    ]))

    story.append(table)
    doc.build(story)
```

## Report with Multiple Sections

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

## Performance Tips

1. **Reuse styles** - Create ParagraphStyle once, use many times
2. **Batch operations** - Build story list fully before calling `doc.build()`
3. **Use Table wisely** - Tables with many rows are expensive; consider splitting
4. **Image optimization** - Pre-resize images; don't rely on ReportLab scaling
5. **Font embedding** - Subset fonts when using custom TTF
