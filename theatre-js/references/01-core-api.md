# Theatre.js Core API Reference

## getProject(id, config?)

Creates or retrieves a project instance.

```typescript
import { getProject } from '@theatre/core'

// Basic
const project = getProject('My Project')

// With saved state (production)
import state from './state.json'
const project = getProject('My Project', { state })
```

## Project API

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `ready` | `Promise<void>` | Resolves when project loads |
| `isReady` | `boolean` | Whether project is ready |
| `address` | `{ projectId }` | Project identifier |

### Methods

```typescript
// Create/get a sheet
const sheet = project.sheet('Scene')

// With instance ID (for multiple instances)
const sheet = project.sheet('Character', 'player1')

// Get asset URL (v0.6.0+)
const url = project.getAssetUrl(assetHandle)
```

## Sheet API

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `sequence` | `Sequence` | Animation timeline |
| `project` | `Project` | Parent project |
| `address` | `object` | `{ projectId, sheetId, sheetInstanceId }` |

### Methods

```typescript
// Create animatable object
const obj = sheet.object('Box', {
  x: 0,
  y: 0,
  color: types.rgba()
})

// With options
const obj = sheet.object('Box', props, {
  reconfigure: true  // Allow prop changes
})

// Remove object (v0.5.1+)
sheet.detachObject('Box')
```

## Object API

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `value` | `object` | Current prop values |
| `props` | `Pointer` | Pointer to props |
| `sheet` | `Sheet` | Parent sheet |
| `project` | `Project` | Parent project |
| `address` | `object` | Full address |
| `initialValue` | `object` | Default values |

### Methods

```typescript
// Listen to all value changes
const unsubscribe = obj.onValuesChange((values) => {
  console.log(values.x, values.y)
})

// Stop listening
unsubscribe()
```

## Sequence API

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `position` | `number` | Current time in seconds (read/write) |
| `pointer` | `Pointer` | Pointer to sequence state |

### Methods

```typescript
const seq = sheet.sequence

// Play with defaults
seq.play()

// Play with options
seq.play({
  iterationCount: Infinity,    // or number
  range: [0, 5],               // [start, end] in seconds
  rate: 1,                     // playback speed
  direction: 'normal',         // 'normal' | 'reverse' | 'alternate' | 'alternateReverse'
  rafDriver: customDriver      // custom RAF driver
})

// Pause
seq.pause()

// Seek
seq.position = 2.5

// Attach audio
await seq.attachAudio({
  source: '/audio.mp3',        // URL, AudioBuffer, or HTMLAudioElement
  audioContext?: AudioContext, // optional custom context
  destinationNode?: AudioNode  // optional custom destination
})

// Get keyframes (v0.6.1+, experimental)
const keyframes = seq.__experimental_getKeyframes(obj.props.x)
```

## Pointer Utilities

```typescript
import { val, onChange } from '@theatre/core'

// Read current value
const x = val(obj.props.x)

// Watch for changes
const unsubscribe = onChange(obj.props.x, (newValue) => {
  console.log('x changed to', newValue)
})

// With custom RAF driver
onChange(obj.props.x, callback, customRafDriver)
```

## RAF Driver

Custom animation frame driver for advanced control:

```typescript
import { createRafDriver } from '@theatre/core'

const driver = createRafDriver({ name: 'custom' })

// Tick manually
driver.tick(performance.now())

// Use with sequence
seq.play({ rafDriver: driver })
```
