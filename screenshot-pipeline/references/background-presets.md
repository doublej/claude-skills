# Background Presets

10 named background presets plus custom options. Apply to `body` or `.bg`.

## Named Presets

### cosmic (default dark)
```css
background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #2d1b69 100%);
```

### mystic
```css
background: linear-gradient(135deg, #1a0533 0%, #3b1460 40%, #0f2747 100%);
```

### ocean
```css
background: linear-gradient(135deg, #0a1628 0%, #0d3b5e 50%, #1a6b7a 100%);
```

### sunset
```css
background: linear-gradient(135deg, #1a0a2e 0%, #6b2150 45%, #c4553a 100%);
```

### earth
```css
background: linear-gradient(135deg, #1a1a0f 0%, #3d4a2a 50%, #5a6340 100%);
```

### radiant
```css
background: radial-gradient(ellipse at 30% 40%, #3b1460 0%, #0f0f23 70%);
```

### glass
```css
background: linear-gradient(135deg, #e8ecf1 0%, #d5dce6 50%, #c3ccd8 100%);
```

### clean (default light)
```css
background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f0 100%);
```

### dark
```css
background: #0a0a0a;
```

### transparent
```css
background: transparent;
```
Use with Playwright's `omitBackground: true` for PNG with alpha.

## Custom Solid Color

```css
background: {{COLOR}};
```

## Custom Gradient

```css
/* 2-stop */
background: linear-gradient({{ANGLE}}deg, {{COLOR_1}} 0%, {{COLOR_2}} 100%);

/* 3-stop */
background: linear-gradient({{ANGLE}}deg, {{COLOR_1}} 0%, {{COLOR_2}} 50%, {{COLOR_3}} 100%);
```

## Mesh / Multi-gradient Pattern

Layer multiple gradients for a richer look:

```css
background:
  radial-gradient(ellipse at 20% 50%, rgba(99,50,200,0.4) 0%, transparent 50%),
  radial-gradient(ellipse at 80% 20%, rgba(50,100,220,0.3) 0%, transparent 50%),
  radial-gradient(ellipse at 50% 80%, rgba(200,50,100,0.2) 0%, transparent 50%),
  #0f0f23;
```

## Brand-Derived

Extract 2-3 dominant colors from the app, reduce saturation 20-30%, and create a gradient at 135deg. Works well for product-specific assets.

## Selection Guide

| Context | Recommended |
|---------|-------------|
| Dark UI app | cosmic, mystic, dark |
| Light UI app | clean, glass |
| Colorful/creative | sunset, ocean, radiant |
| Transparent overlay | transparent |
| Brand-specific | brand-derived or custom gradient |
