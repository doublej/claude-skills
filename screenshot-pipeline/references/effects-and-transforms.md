# Effects and Transforms

Visual effects, perspective transforms, and watermarking. Pure CSS/SVG.

## Effects

### noise

```html
<svg style="position:absolute;width:0;height:0">
  <filter id="noise">
    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
</svg>
```

```css
.noise-overlay {
  position: absolute;
  inset: 0;
  opacity: 0.04;
  filter: url(#noise);
  pointer-events: none;
  z-index: 10;
}
```

Place `<div class="noise-overlay"></div>` as the last child of the body. Adjust `opacity` (0.02-0.08) to taste.

### vhs

Scan-line effect for retro/lo-fi aesthetics.

```css
.vhs-overlay {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    rgba(0,0,0,0.06) 0px,
    rgba(0,0,0,0.06) 1px,
    transparent 1px,
    transparent 3px
  );
  pointer-events: none;
  z-index: 10;
}
```

### subtle-texture

Dot pattern for depth on solid/gradient backgrounds.

```css
.texture-overlay {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(rgba(255,255,255,0.07) 1px, transparent 1px);
  background-size: 16px 16px;
  pointer-events: none;
  z-index: 1;
}
```

## Transforms

### zoom

Scale the frame for emphasis. Apply to `.device-frame`.

```css
.transform-zoom { transform: scale(1.05); }
```

Range: `1.02` (subtle) to `1.15` (dramatic). Values above 1.1 may clip — increase padding.

### tilt

Perspective rotation for 3D depth. Apply to `.device-frame`.

```css
.transform-tilt {
  transform: perspective(1200px) rotateY(-8deg);
  transform-origin: center center;
}
```

Axis options:
- `rotateY(-8deg)` — horizontal tilt (most common)
- `rotateX(4deg)` — vertical tilt
- `rotateY(-6deg) rotateX(3deg)` — compound

Keep angles under 12deg to avoid distortion.

### tilt + zoom combined

```css
.transform-tilt-zoom {
  transform: perspective(1200px) rotateY(-6deg) scale(1.04);
  transform-origin: center center;
}
```

## Watermark

### Logo watermark

Place a small logo in a corner.

```html
<img class="watermark-logo" src="logo.png" alt="">
```

```css
.watermark-logo {
  position: absolute;
  width: 32px;
  height: 32px;
  opacity: 0.6;
  z-index: 20;
}
```

### Text watermark

```html
<div class="watermark-text">appname.com</div>
```

```css
.watermark-text {
  position: absolute;
  font-family: system-ui, sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255,255,255,0.4);
  z-index: 20;
}
```

### Corner positions

```css
.pos-top-left     { top: 16px; left: 16px; }
.pos-top-right    { top: 16px; right: 16px; }
.pos-bottom-left  { bottom: 16px; left: 16px; }
.pos-bottom-right { bottom: 16px; right: 16px; }
```

For light backgrounds, use `color: rgba(0,0,0,0.3)` instead.
