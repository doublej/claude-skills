# Canvas API Reference

Low-level PDF drawing with ReportLab Canvas.

## Coordinate System

- Origin (0, 0) is **bottom-left**
- Y increases upward
- Units are points (1/72 inch)
- A4 = 595.27 x 841.89 points
- Letter = 612 x 792 points

```python
from reportlab.lib.units import inch, cm, mm

c.drawString(1*inch, 10*inch, "One inch from left, 10 inches up")
c.drawString(2.5*cm, 20*cm, "Using centimeters")
```

## Text Operations

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

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

## Built-in Fonts

Always available (no embedding needed):

```
Helvetica, Helvetica-Bold, Helvetica-Oblique, Helvetica-BoldOblique
Times-Roman, Times-Bold, Times-Italic, Times-BoldItalic
Courier, Courier-Bold, Courier-Oblique, Courier-BoldOblique
Symbol, ZapfDingbats
```

## Custom Fonts (TTF)

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('MyFont', '/path/to/font.ttf'))
c.setFont('MyFont', 12)
c.drawString(100, 700, "Custom font text")
```

## Colors

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

## Drawing Shapes

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

## Paths (Complex Shapes)

```python
p = c.beginPath()
p.moveTo(100, 100)
p.lineTo(200, 200)
p.lineTo(150, 250)
p.curveTo(100, 300, 50, 250, 100, 200)  # Bezier curve
p.close()

c.drawPath(p, fill=1, stroke=1)
```

## Images

```python
# Draw image at position
c.drawImage("photo.jpg", 100, 500, width=200, height=150)

# Preserve aspect ratio
c.drawImage("photo.jpg", 100, 300, width=200, preserveAspectRatio=True)

# With mask (transparency)
c.drawImage("logo.png", 100, 100, mask='auto')
```

## State Management

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
