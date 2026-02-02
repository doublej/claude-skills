# Theatre.js Prop Types

All types are imported from `@theatre/core`:

```typescript
import { types } from '@theatre/core'
```

## types.number(default, opts?)

Numeric value with optional constraints.

```typescript
// Basic
x: types.number(0)

// With range (UI hint, not validation)
x: types.number(0, { range: [-100, 100] })

// With nudge multiplier
x: types.number(0, {
  range: [0, 1],
  nudgeMultiplier: 0.01  // Shift+drag increment
})

// Custom nudge function
x: types.number(0, {
  nudgeFn: (params) => {
    // params: { deltaX, deltaFraction, magnitude }
    return params.deltaX * 0.1
  }
})

// With custom interpolation
x: types.number(0, {
  interpolate: (left, right, progression) => {
    // Custom easing between keyframes
    return left + (right - left) * progression
  }
})
```

## types.compound(props, opts?)

Group props into nested structure.

```typescript
position: types.compound({
  x: types.number(0),
  y: types.number(0),
  z: types.number(0)
})

// Access: obj.value.position.x

// Nested compounds
transform: types.compound({
  position: types.compound({
    x: types.number(0),
    y: types.number(0)
  }),
  rotation: types.number(0)
})
```

## types.rgba(default?)

Color with RGBA channels (0-1 normalized).

```typescript
// Default white
color: types.rgba()

// Custom default
color: types.rgba({ r: 1, g: 0.5, b: 0, a: 1 })

// Hex shorthand in UI: #RGB, #RGBA, #RRGGBB, #RRGGBBAA
```

## types.boolean(default, opts?)

True/false value.

```typescript
visible: types.boolean(true)

// With label
visible: types.boolean(true, { label: 'Show' })
```

## types.string(default, opts?)

Text string.

```typescript
label: types.string('Hello World')

// With label
label: types.string('', { label: 'Display Text' })
```

## types.stringLiteral(default, options, opts?)

Enum/select from predefined values.

```typescript
// As dropdown menu
mode: types.stringLiteral('auto', {
  auto: 'Automatic',
  manual: 'Manual',
  disabled: 'Disabled'
})

// As radio switch
mode: types.stringLiteral('auto', {
  auto: 'Auto',
  manual: 'Manual'
}, { as: 'switch' })

// With label
mode: types.stringLiteral('auto', options, { label: 'Mode' })
```

## types.image(default, opts?) [v0.6.0+]

Image asset reference.

```typescript
texture: types.image('', { label: 'Texture' })

// Usage: returns asset handle
const url = project.getAssetUrl(obj.value.texture)
```

## types.file(default, opts?) [v0.7.0+]

File asset reference.

```typescript
data: types.file('', { label: 'Data File' })

// Usage
const url = project.getAssetUrl(obj.value.data)
```

## Shorthand Props

Without `types`, Theatre.js infers type:

```typescript
const obj = sheet.object('Box', {
  x: 0,                    // → types.number(0)
  visible: true,           // → types.boolean(true)
  label: 'Hello',          // → types.string('Hello')
  position: { x: 0, y: 0 } // → types.compound({ x: number, y: number })
})
```

## Custom Interpolation

All types support custom `interpolate` function:

```typescript
rotation: types.number(0, {
  interpolate: (left, right, progression) => {
    // Spherical interpolation for angles
    const diff = ((right - left + 540) % 360) - 180
    return left + diff * progression
  }
})
```
