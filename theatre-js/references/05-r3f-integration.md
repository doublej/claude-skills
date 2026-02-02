# Theatre.js React Three Fiber Integration

## Setup

```bash
npm install @theatre/core @theatre/studio @theatre/r3f
npm install react three @react-three/fiber
```

```tsx
import { getProject } from '@theatre/core'
import studio from '@theatre/studio'
import extension from '@theatre/r3f/dist/extension'

// Dev-only
if (import.meta.env.DEV) {
  studio.initialize()
  studio.extend(extension)  // Required for 3D controls
}

const project = getProject('R3F Project')
const sheet = project.sheet('Scene')
```

## SheetProvider

Wrap your scene to connect to Theatre.js:

```tsx
import { Canvas } from '@react-three/fiber'
import { SheetProvider } from '@theatre/r3f'

function App() {
  return (
    <Canvas>
      <SheetProvider sheet={sheet}>
        {/* Editable objects go here */}
      </SheetProvider>
    </Canvas>
  )
}
```

## editable Components

Create animatable R3F elements:

```tsx
import { editable as e } from '@theatre/r3f'

// Mesh
<e.mesh theatreKey="MyCube">
  <boxGeometry />
  <meshStandardMaterial color="orange" />
</e.mesh>

// Light
<e.pointLight theatreKey="MainLight" position={[10, 10, 10]} />
<e.spotLight theatreKey="SpotLight" />

// Group
<e.group theatreKey="CharacterGroup">
  <Model />
</e.group>
```

## theatreKey Prop

**Required** - unique identifier for each editable:

```tsx
// ❌ Error: missing theatreKey
<e.mesh>

// ✅ Correct
<e.mesh theatreKey="Cube">

// Unique per sheet
<e.mesh theatreKey="Cube1">
<e.mesh theatreKey="Cube2">
```

## visible Prop

Control visibility:

```tsx
// Always visible
<e.mesh theatreKey="Cube" visible={true}>

// Never visible
<e.mesh theatreKey="Cube" visible={false}>

// Visible only in snapshot editor (helpers)
<e.mesh theatreKey="Helper" visible="editor">
```

## additionalProps

Add custom animatable properties:

```tsx
<e.mesh
  theatreKey="Cube"
  additionalProps={{
    customScale: types.number(1, { range: [0, 2] }),
    tint: types.rgba()
  }}
>
```

## objRef

Access backing Theatre.js object:

```tsx
import { useRef, useEffect } from 'react'

function AnimatedMesh() {
  const objRef = useRef()

  useEffect(() => {
    if (objRef.current) {
      objRef.current.onValuesChange((values) => {
        console.log('Custom props:', values)
      })
    }
  }, [])

  return (
    <e.mesh theatreKey="Cube" objRef={objRef}>
      <boxGeometry />
    </e.mesh>
  )
}
```

## Cameras

Built-in editable cameras:

```tsx
import { PerspectiveCamera, OrthographicCamera } from '@theatre/r3f'

// Perspective
<PerspectiveCamera
  theatreKey="MainCamera"
  makeDefault
  position={[5, 5, 5]}
  fov={75}
/>

// Orthographic
<OrthographicCamera
  theatreKey="OrthoCamera"
  makeDefault
  zoom={50}
/>

// Look at target
<PerspectiveCamera
  theatreKey="Camera"
  lookAt={targetRef}
/>
```

## useCurrentSheet Hook

Access sheet in nested components:

```tsx
import { useCurrentSheet } from '@theatre/r3f'

function NestedComponent() {
  const sheet = useCurrentSheet()

  useEffect(() => {
    sheet.sequence.play()
  }, [])

  return <mesh />
}
```

## refreshSnapshot

Update snapshot after dynamic loading:

```tsx
import { refreshSnapshot, RefreshSnapshot } from '@theatre/r3f'

// Programmatic
useEffect(() => {
  loadAssets().then(() => {
    refreshSnapshot()
  })
}, [])

// Component-based (with Suspense)
<Suspense fallback={<Loading />}>
  <Model />
  <RefreshSnapshot />
</Suspense>
```

## Custom Components with editable()

Wrap custom components:

```tsx
import { editable } from '@theatre/r3f'

// Your custom component
function CustomLight({ intensity, color }) {
  return <pointLight intensity={intensity} color={color} />
}

// Make it editable
const EditableLight = editable(CustomLight, 'pointLight')

// Usage
<EditableLight
  theatreKey="CustomLight"
  intensity={1}
  color="white"
/>
```

## Production Build

```tsx
import { getProject } from '@theatre/core'
import state from './state.json'

const project = getProject('R3F Project', { state })
const sheet = project.sheet('Scene')

function App() {
  useEffect(() => {
    project.ready.then(() => {
      sheet.sequence.play({ iterationCount: Infinity })
    })
  }, [])

  return (
    <Canvas>
      <SheetProvider sheet={sheet}>
        <Scene />
      </SheetProvider>
    </Canvas>
  )
}
```
