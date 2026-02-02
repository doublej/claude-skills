# Shadow Presets

5 shadow options for the device frame. Apply via `box-shadow` on `.device-frame`.

## Presets

### none
```css
box-shadow: none;
```
Use for: outline frame, transparent exports, minimal designs.

### spread
```css
box-shadow: 0 25px 60px -12px rgba(0,0,0,0.5);
```
Wide, diffuse shadow. Default for most compositions. Good on dark backgrounds.

### hug
```css
box-shadow:
  0 4px 12px rgba(0,0,0,0.15),
  0 1px 3px rgba(0,0,0,0.1);
```
Tight, close shadow. Clean and subtle. Best on light backgrounds.

### adaptive
```css
box-shadow:
  0 20px 40px -8px rgba(0,0,0,0.35),
  0 8px 16px -4px rgba(0,0,0,0.2);
```
Two-layer shadow with depth. Works on both light and dark backgrounds.

### elevated
```css
box-shadow:
  0 40px 80px -20px rgba(0,0,0,0.5),
  0 16px 32px -8px rgba(0,0,0,0.3),
  0 4px 8px rgba(0,0,0,0.15);
```
Three-layer dramatic shadow. Creates a floating effect. Best for hero images.

## Opacity Guidance

| Background tone | Shadow opacity | Reason |
|----------------|---------------|--------|
| Dark (#0a-#2d) | 0.4 - 0.6 | Needs more opacity to be visible |
| Medium (#4a-#8a) | 0.25 - 0.4 | Balanced |
| Light (#c0-#ff) | 0.1 - 0.25 | Less opacity avoids harshness |

Scale the `rgba` alpha values in the presets accordingly.

## Combining with Frames

Some frame presets include their own `box-shadow` (glass, inset). When using a shadow preset with these frames, replace the frame's shadow entirely rather than combining — stacking shadows creates muddy results.
