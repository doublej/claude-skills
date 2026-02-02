---
name: theatre-js
description: Use when implementing motion design, timeline animations, visual animation editors, animating Three.js/R3F scenes, creating keyframe animations, or using Theatre.js, @theatre/core, @theatre/studio, @theatre/r3f, theatric, or building animation tooling for the web.
---

# Theatre.js Best Practices

Motion design editor and animation library for the web. Provides a visual timeline editor (Studio) with programmatic control for high-fidelity animations.

## Installation

```bash
# Core + Studio (development)
npm install @theatre/core@0.7 @theatre/studio@0.7

# React Three Fiber integration
npm install @theatre/r3f@0.7

# React utilities
npm install @theatre/react

# Theatric (simplified controls for quick prototyping)
npm install theatric

# CDN (no bundler)
# core + studio: https://cdn.jsdelivr.net/npm/@theatre/browser-bundles@0.5.0-insiders.88df1ef/dist/core-and-studio.js
# core only: https://cdn.jsdelivr.net/npm/@theatre/browser-bundles@0.5.0-insiders.88df1ef/dist/core-only.min.js
```

## Quick Start

```tsx
import * as core from '@theatre/core'
import studio from '@theatre/studio'

// Initialize Studio (dev only)
if (import.meta.env.DEV) {
  studio.initialize()
}

// Create project → sheet → object
const project = core.getProject('My Project')
const sheet = project.sheet('Main')
const obj = sheet.object('Box', {
  position: { x: 0, y: 0 },
  opacity: 1
})

// Read values
console.log(obj.value.position.x)

// Listen to changes
obj.onValuesChange((values) => {
  element.style.opacity = values.opacity
  element.style.transform = `translate(${values.position.x}px, ${values.position.y}px)`
})

// Play animation
sheet.sequence.play({ iterationCount: Infinity })
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Project** | Container for all animation data; maps to exported JSON state |
| **Sheet** | A scene or component; contains objects and one sequence |
| **Object** | Animatable entity with typed props |
| **Sequence** | Timeline with keyframes; controls playback |
| **Props** | Typed values (number, compound, rgba, etc.) |

## Reference Index

| Reference | Use When |
|-----------|----------|
| `references/01-core-api.md` | Project, sheet, object, sequence APIs |
| `references/02-prop-types.md` | Defining props, custom types, constraints |
| `references/03-studio.md` | Studio UI, keyboard shortcuts, extensions |
| `references/04-react-integration.md` | useVal, usePrism, @theatre/react hooks |
| `references/05-r3f-integration.md` | React Three Fiber, editable components |
| `references/06-production.md` | Export state, deployment, tree-shaking |
| `references/07-audio-sync.md` | Audio synchronization with animations |

## Common Patterns

### Animate DOM Element

```tsx
const obj = sheet.object('Card', {
  x: 0,
  y: 0,
  rotation: 0,
  scale: 1,
  opacity: 1
})

obj.onValuesChange(({ x, y, rotation, scale, opacity }) => {
  element.style.transform = `translate(${x}px, ${y}px) rotate(${rotation}deg) scale(${scale})`
  element.style.opacity = opacity
})
```

### HTML/SVG Animation (No Bundler)

```html
<script type="module">
  import 'https://cdn.jsdelivr.net/npm/@theatre/browser-bundles@0.5.0-insiders.88df1ef/dist/core-and-studio.js'
  const { core, studio } = Theatre
  studio.initialize()

  const project = core.getProject('HTML Animation')
  const sheet = project.sheet('Main')
  const obj = sheet.object('Heading', {
    y: 0,
    opacity: core.types.number(1, { range: [0, 1] })
  })

  const el = document.getElementById('heading')
  obj.onValuesChange(({ y, opacity }) => {
    el.style.transform = `translateY(${y}px)`
    el.style.opacity = opacity
  })
</script>
```

### Sequence Playback Control

```tsx
const seq = sheet.sequence

// Play once
seq.play()

// Play with options
seq.play({
  iterationCount: Infinity,  // loop forever
  range: [0, 2],             // play seconds 0-2
  rate: 1.5,                 // 1.5x speed
  direction: 'alternate'     // ping-pong
})

// Pause and seek
seq.pause()
seq.position = 1.5  // jump to 1.5s

// Await completion
await seq.play({ iterationCount: 1 })
console.log('Animation complete')
```

### React Three Fiber Scene

```tsx
import { Canvas } from '@react-three/fiber'
import { editable as e, SheetProvider, PerspectiveCamera } from '@theatre/r3f'
import { getProject } from '@theatre/core'
import studio from '@theatre/studio'
import extension from '@theatre/r3f/dist/extension'

// Dev setup
if (import.meta.env.DEV) {
  studio.initialize()
  studio.extend(extension)
}

const sheet = getProject('R3F Demo').sheet('Scene')

function App() {
  return (
    <Canvas>
      <SheetProvider sheet={sheet}>
        <PerspectiveCamera theatreKey="Camera" makeDefault position={[5, 5, -5]} fov={75} />
        <ambientLight />
        <e.pointLight theatreKey="Light" position={[10, 10, 10]} />
        <e.mesh theatreKey="Cube">
          <boxGeometry />
          <meshStandardMaterial color="orange" />
        </e.mesh>
      </SheetProvider>
    </Canvas>
  )
}
```

### Vanilla Three.js Scene

```tsx
import * as THREE from 'three'
import { getProject, types } from '@theatre/core'
import studio from '@theatre/studio'

if (import.meta.env.DEV) studio.initialize()

const project = getProject('THREE.js Demo')
const sheet = project.sheet('Scene')

// Create mesh
const mesh = new THREE.Mesh(
  new THREE.BoxGeometry(),
  new THREE.MeshStandardMaterial({ color: 'orange' })
)

// Define animatable props
const meshObj = sheet.object('Cube', {
  rotation: types.compound({
    x: types.number(0, { range: [-2, 2] }),
    y: types.number(0, { range: [-2, 2] }),
    z: types.number(0, { range: [-2, 2] })
  }),
  position: types.compound({
    x: types.number(0),
    y: types.number(0),
    z: types.number(0)
  })
})

// Connect to Three.js
meshObj.onValuesChange((values) => {
  mesh.rotation.set(
    values.rotation.x * Math.PI,
    values.rotation.y * Math.PI,
    values.rotation.z * Math.PI
  )
  mesh.position.set(values.position.x, values.position.y, values.position.z)
})
```

### Theatric Controls (Quick Prototyping)

```tsx
import { useControls, types, button } from 'theatric'

function Component() {
  const { color, intensity, position, $get, $set } = useControls({
    color: '#ff0000',
    intensity: types.number(1, { range: [0, 2] }),
    position: { x: 0, y: 0, z: 0 },
    reset: button(() => {
      $set((v) => v.position.x, 0)
      $set((v) => v.position.y, 0)
    })
  }, { folder: 'Light Settings' })

  return <mesh position={[position.x, position.y, position.z]} />
}
```

### Audio Synchronization

```tsx
// Attach audio to sequence
sheet.sequence.attachAudio({
  source: '/audio/music.mp3'
}).then(() => {
  console.log('Audio loaded and synced!')
})

// Custom Web Audio API graph
const audioContext = new AudioContext()
sheet.sequence.attachAudio({
  source: audioBuffer,
  audioContext,
  destinationNode: audioContext.destination
})
```

## Prop Types Reference

```tsx
import { types } from '@theatre/core'

const obj = sheet.object('Example', {
  // Number with range and nudge
  x: types.number(0, { range: [-100, 100], nudgeMultiplier: 0.1 }),

  // Compound (nested object)
  position: types.compound({
    x: types.number(0),
    y: types.number(0),
    z: types.number(0)
  }),

  // Color (RGBA, 0-1 normalized)
  color: types.rgba({ r: 1, g: 0.5, b: 0, a: 1 }),

  // Boolean
  visible: types.boolean(true),

  // String
  label: types.string('Hello'),

  // Enum (radio or menu)
  mode: types.stringLiteral('auto', { auto: 'Auto', manual: 'Manual' }, { as: 'switch' }),

  // Image asset (v0.6.0+)
  texture: types.image('', { label: 'Texture' }),

  // File asset (v0.7.0+)
  data: types.file('', { label: 'Data File' })
})
```

## Studio Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Alt/Option + \` | Toggle Studio visibility |
| `Space` | Play/pause sequence |
| `Shift + drag` | Create focus range in timeline |
| `Right-click prop` | Sequence prop / add keyframe |
| `Click keyframe connector` | Open tween/easing editor |

## Critical Mistakes to Avoid

### 1. Studio in Production
```tsx
// ❌ Includes studio in bundle
import studio from '@theatre/studio'
studio.initialize()

// ✅ Dev-only initialization
if (import.meta.env.DEV) {
  studio.initialize()
}
```

### 2. Missing State in Production
```tsx
// ❌ No animations without state
const project = core.getProject('My Project')

// ✅ Load exported state
import state from './state.json'
const project = core.getProject('My Project', { state })
```

### 3. Object Key Collisions
```tsx
// ❌ Same key = same object (shared state)
sheet.object('Box', { x: 0 })
sheet.object('Box', { y: 0 })  // Overwrites!

// ✅ Unique keys per object
sheet.object('Box1', { x: 0 })
sheet.object('Box2', { y: 0 })
```

### 4. Missing R3F Extension
```tsx
// ❌ No 3D controls in Studio
studio.initialize()

// ✅ Extend with R3F extension
import extension from '@theatre/r3f/dist/extension'
studio.initialize()
studio.extend(extension)
```

### 5. Forgetting theatreKey
```tsx
// ❌ Not editable
<e.mesh>

// ✅ Requires theatreKey
<e.mesh theatreKey="MyCube">
```

### 6. Not Waiting for Project Ready
```tsx
// ❌ May play before state loaded
sheet.sequence.play()

// ✅ Wait for project ready
project.ready.then(() => {
  sheet.sequence.play()
})
```

### 7. Blocking Audio Autoplay
```tsx
// ❌ Audio blocked by browser
sheet.sequence.attachAudio({ source: '/music.mp3' })
sheet.sequence.play()

// ✅ Trigger from user interaction
button.onclick = async () => {
  await sheet.sequence.attachAudio({ source: '/music.mp3' })
  sheet.sequence.play()
}
```

## Production Checklist

1. Export state JSON from Studio (Project → Export)
2. Import state in `getProject({ state })`
3. Remove `studio.initialize()` and `studio.extend()` calls
4. Use environment checks (`import.meta.env.DEV` or `process.env.NODE_ENV`)
5. Add playback trigger (user interaction or `project.ready`)
6. Verify bundler tree-shakes studio package

## Quick Reference

| Task | Solution |
|------|----------|
| Create project | `getProject('Name', { state? })` |
| Create sheet | `project.sheet('Name')` |
| Create object | `sheet.object('Key', { props })` |
| Listen to values | `obj.onValuesChange(cb)` |
| Read value | `obj.value.propName` |
| Play animation | `sheet.sequence.play(opts?)` |
| Pause animation | `sheet.sequence.pause()` |
| Seek position | `sheet.sequence.position = 1.5` |
| Attach audio | `sheet.sequence.attachAudio({ source })` |
| R3F editable | `<e.mesh theatreKey="Key">` |
| React value hook | `useVal(obj.props.x)` |
| Export state | Studio → Project → Export (JSON) |
| Toggle studio | `Alt/Option + \` |
| Remove object | `sheet.detachObject('Key')` |
