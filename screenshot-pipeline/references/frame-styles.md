# Frame Styles

7 CSS frame presets for screenshot compositing. Apply one class to `.device-frame`.

## Presets

### default
```css
.frame-default {
  border-radius: 20px;
  border: 6px solid #2a2a2a;
  box-shadow: 0 25px 60px -12px rgba(0,0,0,0.5);
  overflow: hidden;
}
```

### glass-light
```css
.frame-glass-light {
  border-radius: 20px;
  border: 1.5px solid rgba(255,255,255,0.5);
  box-shadow: 0 8px 32px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.4);
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(12px);
  padding: 10px;
  overflow: hidden;
}
```

### glass-dark
```css
.frame-glass-dark {
  border-radius: 20px;
  border: 1.5px solid rgba(255,255,255,0.12);
  box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.08);
  background: rgba(0,0,0,0.25);
  backdrop-filter: blur(12px);
  padding: 10px;
  overflow: hidden;
}
```

### liquid-glass
```css
.frame-liquid-glass {
  border-radius: 28px;
  border: 1px solid rgba(255,255,255,0.25);
  box-shadow:
    0 20px 60px rgba(0,0,0,0.3),
    inset 0 1px 0 rgba(255,255,255,0.3),
    inset 0 -1px 0 rgba(0,0,0,0.1);
  background: linear-gradient(
    135deg,
    rgba(255,255,255,0.18) 0%,
    rgba(255,255,255,0.06) 100%
  );
  backdrop-filter: blur(20px) saturate(1.4);
  padding: 12px;
  overflow: hidden;
}
```

### inset-light
```css
.frame-inset-light {
  border-radius: 16px;
  border: 1px solid rgba(0,0,0,0.08);
  box-shadow:
    inset 0 2px 6px rgba(0,0,0,0.08),
    0 1px 0 rgba(255,255,255,0.9);
  background: #f0f0f0;
  padding: 10px;
  overflow: hidden;
}
```

### inset-dark
```css
.frame-inset-dark {
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.06);
  box-shadow:
    inset 0 2px 6px rgba(0,0,0,0.4),
    0 1px 0 rgba(255,255,255,0.05);
  background: #1a1a1a;
  padding: 10px;
  overflow: hidden;
}
```

### outline
```css
.frame-outline {
  border-radius: 16px;
  border: 2px solid rgba(255,255,255,0.25);
  box-shadow: none;
  overflow: hidden;
}
```

## Border Radius Variants

Override `border-radius` on any preset:

| Variant | Value | Use case |
|---------|-------|----------|
| sharp | `8px` | Technical/developer tools |
| curved | `20px` | Default, most apps |
| round | `36px` | Playful/mobile-first |

```css
/* Example: glass-light with sharp corners */
.frame-glass-light.radius-sharp { border-radius: 8px; }
```

## Inner Image Styling

Always apply to the image inside the frame:

```css
.device-frame img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: inherit;
}
```

When the frame has `padding`, the image inherits the rounding naturally.
