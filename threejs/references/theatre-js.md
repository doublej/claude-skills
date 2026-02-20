# Theatre.js Reference

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
```

## Core API

### Project

```ts
import { getProject } from '@theatre/core'

const project = getProject('My Project')

// Production: load exported state
import state from './state.json'
const project = getProject('My Project', { state })
```

| Property | Type | Description |
|----------|------|-------------|
| `ready` | `Promise<void>` | Resolves when project loads |
| `isReady` | `boolean` | Whether project is ready |

### Sheet

```ts
const sheet = project.sheet('Scene')

// Multiple instances
const sheet = project.sheet('Character', 'player1')
```

### Object

```ts
const obj = sheet.object('Box', {
  x: 0,
  y: 0,
  color: types.rgba()
})

// With reconfiguration support
const obj = sheet.object('Box', props, { reconfigure: true })

// Listen to changes
const unsub = obj.onValuesChange((values) => {
  console.log(values.x, values.y)
})

// Read current value
console.log(obj.value.x)

// Remove object
sheet.detachObject('Box')
```

### Sequence

```ts
const seq = sheet.sequence

// Play with options
seq.play({
  iterationCount: Infinity,
  range: [0, 2],
  rate: 1.5,
  direction: 'alternate' // 'normal' | 'reverse' | 'alternate' | 'alternateReverse'
})

seq.pause()
seq.position = 1.5  // seek

// Await completion
await seq.play({ iterationCount: 1 })
```

### Pointer Utilities

```ts
import { val, onChange } from '@theatre/core'

const x = val(obj.props.x)

const unsub = onChange(obj.props.x, (newValue) => {
  console.log('x changed to', newValue)
})
```

### Custom RAF Driver

```ts
import { createRafDriver } from '@theatre/core'

const driver = createRafDriver({ name: 'custom' })
driver.tick(performance.now())
seq.play({ rafDriver: driver })
```

## Prop Types

```ts
import { types } from '@theatre/core'

const obj = sheet.object('Example', {
  // Number with range
  x: types.number(0, { range: [-100, 100], nudgeMultiplier: 0.1 }),

  // Compound (nested)
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

  // Enum (dropdown or radio switch)
  mode: types.stringLiteral('auto', { auto: 'Auto', manual: 'Manual' }, { as: 'switch' }),

  // Image asset (v0.6.0+)
  texture: types.image('', { label: 'Texture' }),

  // File asset (v0.7.0+)
  data: types.file('', { label: 'Data File' })
})
```

### Shorthand (auto-inferred)

```ts
sheet.object('Box', {
  x: 0,                    // -> types.number(0)
  visible: true,           // -> types.boolean(true)
  label: 'Hello',          // -> types.string('Hello')
  position: { x: 0, y: 0 } // -> types.compound(...)
})
```

### Custom Interpolation

```ts
rotation: types.number(0, {
  interpolate: (left, right, progression) => {
    const diff = ((right - left + 540) % 360) - 180
    return left + diff * progression
  }
})
```

## Studio

### Initialization

```ts
import studio from '@theatre/studio'

if (import.meta.env.DEV) {
  studio.initialize()
}

// With R3F extension
import extension from '@theatre/r3f/dist/extension'
studio.initialize()
studio.extend(extension)
```

### UI Panels

| Panel | Description |
|-------|-------------|
| **Outline** | Project/sheet/object hierarchy |
| **Details** | Props for selected object |
| **Sequence Editor** | Timeline with keyframes |
| **Toolbar** | Extension buttons |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Alt/Option + \` | Toggle Studio |
| `Space` | Play/pause |
| `Shift + drag` | Focus range in timeline |
| Right-click prop | Sequence prop |
| Click between keyframes | Open easing editor |
| `Delete` | Delete selected keyframes |

### Transactions & Scrubs

```ts
// Atomic changes (single undo level)
studio.transaction(({ set }) => {
  set(obj.props.x, 10)
  set(obj.props.y, 20)
})

// Temporary changes
const scrub = studio.scrub()
scrub.capture(({ set }) => { set(obj.props.x, 10) })
scrub.commit()   // or scrub.discard()
```

### State Export

```ts
const state = studio.createContentOfSaveFile('My Project')
console.log(JSON.stringify(state, null, 2))
```

### Creating Extensions

```ts
const myExtension = {
  id: 'my-extension',
  toolbars: {
    global(set, studio) {
      set([{
        type: 'Icon',
        title: 'My Button',
        svgSource: '...',
        onClick: () => console.log('clicked')
      }])
    }
  },
  panes: [{
    class: 'my-pane',
    mount({ paneId, node }) {
      node.innerHTML = '<h1>Custom Pane</h1>'
      return () => { /* cleanup */ }
    }
  }]
}

studio.extend(myExtension)
studio.initialize()
studio.createPane('my-pane')
```

## React Integration

### useVal Hook

```tsx
import { useVal } from '@theatre/react'

function Component({ obj }) {
  const x = useVal(obj.props.x)
  return <div style={{ left: x }} />
}
```

### usePrism Hook

```tsx
import { usePrism } from '@theatre/react'
import { val } from '@theatre/core'

function Component({ obj }) {
  const distance = usePrism(() => {
    const x = val(obj.props.x)
    const y = val(obj.props.y)
    return Math.sqrt(x * x + y * y)
  }, [obj])
  return <div>Distance: {distance}</div>
}
```

### Theatric (Quick Prototyping)

```tsx
import { useControls, types, button } from 'theatric'

function Component() {
  const { color, size, position, $get, $set } = useControls({
    color: '#ff0000',
    size: types.number(1, { range: [0.1, 5] }),
    position: { x: 0, y: 0, z: 0 },
    reset: button(() => {
      $set((v) => v.position.x, 0)
      $set((v) => v.position.y, 0)
    })
  }, { folder: 'Settings' })

  return <mesh position={[position.x, position.y, position.z]} />
}
```

## R3F Integration

### Setup

```tsx
import { Canvas } from '@react-three/fiber'
import { editable as e, SheetProvider, PerspectiveCamera } from '@theatre/r3f'
import { getProject } from '@theatre/core'
import studio from '@theatre/studio'
import extension from '@theatre/r3f/dist/extension'

if (import.meta.env.DEV) {
  studio.initialize()
  studio.extend(extension) // Required for 3D controls
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

### editable Components

```tsx
<e.mesh theatreKey="MyCube">       {/* Mesh */}
<e.pointLight theatreKey="Light">  {/* Light */}
<e.group theatreKey="Group">       {/* Group */}
```

- `theatreKey` is **required** and must be unique per sheet
- `visible="editor"` makes objects visible only in Studio
- `additionalProps={{ custom: types.number(1) }}` adds animatable props
- `objRef={ref}` gives access to the backing Theatre.js object

### Cameras

```tsx
import { PerspectiveCamera, OrthographicCamera } from '@theatre/r3f'

<PerspectiveCamera theatreKey="MainCam" makeDefault position={[5, 5, 5]} fov={75} />
<OrthographicCamera theatreKey="OrthoCam" makeDefault zoom={50} />
<PerspectiveCamera theatreKey="Camera" lookAt={targetRef} />
```

### useCurrentSheet Hook

```tsx
import { useCurrentSheet } from '@theatre/r3f'

function Nested() {
  const sheet = useCurrentSheet()
  useEffect(() => { sheet.sequence.play() }, [])
  return <mesh />
}
```

### Custom Editable Components

```tsx
import { editable } from '@theatre/r3f'

const EditableLight = editable(CustomLight, 'pointLight')
<EditableLight theatreKey="Custom" intensity={1} />
```

## Vanilla Three.js + Theatre.js

```ts
import * as THREE from 'three'
import { getProject, types } from '@theatre/core'
import studio from '@theatre/studio'

if (import.meta.env.DEV) studio.initialize()

const project = getProject('Demo')
const sheet = project.sheet('Scene')

const mesh = new THREE.Mesh(
  new THREE.BoxGeometry(),
  new THREE.MeshStandardMaterial({ color: 'orange' })
)

const meshObj = sheet.object('Cube', {
  rotation: types.compound({
    x: types.number(0, { range: [-2, 2] }),
    y: types.number(0, { range: [-2, 2] }),
    z: types.number(0, { range: [-2, 2] })
  }),
  position: types.compound({
    x: types.number(0), y: types.number(0), z: types.number(0)
  })
})

meshObj.onValuesChange((v) => {
  mesh.rotation.set(v.rotation.x * Math.PI, v.rotation.y * Math.PI, v.rotation.z * Math.PI)
  mesh.position.set(v.position.x, v.position.y, v.position.z)
})
```

## Audio Synchronization

```ts
// Attach audio to sequence
sheet.sequence.attachAudio({ source: '/audio/music.mp3' })
  .then(() => sheet.sequence.play())

// Custom Web Audio API graph
const audioContext = new AudioContext()
const gainNode = audioContext.createGain()
gainNode.connect(audioContext.destination)

sheet.sequence.attachAudio({
  source: audioBuffer,
  audioContext,
  destinationNode: gainNode
})
```

**Browser autoplay**: audio is blocked until user interaction. Trigger `attachAudio` + `play` from a click handler.

### Audio Visualization

```ts
const analyser = audioContext.createAnalyser()
analyser.fftSize = 256

const { gainNode } = await sheet.sequence.attachAudio({ source: '/audio.mp3', audioContext })
gainNode.disconnect()
gainNode.connect(analyser)
analyser.connect(audioContext.destination)

const dataArray = new Uint8Array(analyser.frequencyBinCount)
function animate() {
  analyser.getByteFrequencyData(dataArray)
  requestAnimationFrame(animate)
}
```

## Production Deployment

### Export & Load State

1. Studio -> click project name -> "Export" -> save `state.json`
2. Import in code:

```ts
import state from './state.json'
const project = getProject('My Project', { state })
```

### Remove Studio from Bundle

```ts
// Vite (dynamic import, tree-shakes in prod)
if (import.meta.env.DEV) {
  const studio = await import('@theatre/studio')
  studio.default.initialize()
}
```

### Playback Triggers

```ts
// Auto-play on ready
project.ready.then(() => sheet.sequence.play({ iterationCount: Infinity }))

// Scroll-driven
window.addEventListener('scroll', () => {
  const progress = scrollY / (document.body.scrollHeight - innerHeight)
  sheet.sequence.position = progress * sheet.sequence.length
})
```

### Licensing

| Package | License | Production |
|---------|---------|------------|
| @theatre/core | Apache 2.0 | Free |
| @theatre/studio | AGPL 3.0 | Dev only |
| @theatre/r3f | Apache 2.0 | Free |
| theatric | Apache 2.0 | Free |

## Common Mistakes

1. **Studio in production** -- wrap `studio.initialize()` in `import.meta.env.DEV`
2. **Missing state** -- no animations without exported `state.json`
3. **Key collisions** -- `sheet.object('Box', {x:0})` twice overwrites; use unique keys
4. **Missing R3F extension** -- no 3D controls without `studio.extend(extension)`
5. **Missing theatreKey** -- `<e.mesh>` without `theatreKey` throws error
6. **Not waiting for ready** -- `project.ready.then(...)` before `play()`
7. **Blocked audio** -- must trigger from user interaction (click handler)

## Production Checklist

- [ ] Export state.json from Studio
- [ ] Import state in `getProject({ state })`
- [ ] Remove `studio.initialize()` / `studio.extend()` in prod
- [ ] Use `import.meta.env.DEV` or `process.env.NODE_ENV` checks
- [ ] Add `project.ready` before playback
- [ ] Verify Studio not in production bundle
- [ ] Configure asset base URL if needed
