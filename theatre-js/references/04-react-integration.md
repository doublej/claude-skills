# Theatre.js React Integration

## @theatre/react

React hooks for Theatre.js integration.

```bash
npm install @theatre/react
```

### useVal Hook

Subscribe to Theatre.js pointer values:

```tsx
import { useVal } from '@theatre/react'

function Component({ obj }) {
  // Reacts to changes
  const x = useVal(obj.props.x)
  const position = useVal(obj.props.position)

  return <div style={{ left: x }}>Position: {position.x}, {position.y}</div>
}
```

### usePrism Hook

Create reactive computations:

```tsx
import { usePrism } from '@theatre/react'
import { val } from '@theatre/core'

function Component({ obj }) {
  const computed = usePrism(() => {
    const x = val(obj.props.x)
    const y = val(obj.props.y)
    return Math.sqrt(x * x + y * y)
  }, [obj])

  return <div>Distance: {computed}</div>
}
```

## Theatric (Simplified API)

Quick prototyping with minimal setup:

```bash
npm install theatric
```

### useControls Hook

```tsx
import { useControls, types, button } from 'theatric'

function Component() {
  const { color, size, position } = useControls({
    color: '#ff0000',
    size: types.number(1, { range: [0.1, 5] }),
    position: { x: 0, y: 0, z: 0 }
  })

  return (
    <mesh position={[position.x, position.y, position.z]}>
      <boxGeometry args={[size, size, size]} />
      <meshStandardMaterial color={color} />
    </mesh>
  )
}
```

### Folder Organization

```tsx
const { lightColor } = useControls({
  lightColor: '#ffffff'
}, { folder: 'Lighting' })

const { meshColor } = useControls({
  meshColor: '#ff0000'
}, { folder: 'Materials' })
```

### Imperative Control

```tsx
const { age, $get, $set } = useControls({
  age: 28,
  incrementAge: button(() => {
    $set((v) => v.age, $get((v) => v.age) + 1)
  })
})
```

### Nested Properties

```tsx
const { person, $get, $set } = useControls({
  person: {
    name: 'Alice',
    age: 30
  },
  birthday: button(() => {
    $set((v) => v.person.age, $get((v) => v.person.age) + 1)
  })
})

return <div>{person.name} is {person.age} years old</div>
```

## Common Patterns

### Animation Playback on Mount

```tsx
import { useEffect } from 'react'
import { getProject } from '@theatre/core'

const project = getProject('Demo', { state })
const sheet = project.sheet('Scene')

function App() {
  useEffect(() => {
    project.ready.then(() => {
      sheet.sequence.play({ iterationCount: Infinity })
    })
  }, [])

  return <Scene sheet={sheet} />
}
```

### Syncing with React State

```tsx
function AnimatedComponent({ obj }) {
  const opacity = useVal(obj.props.opacity)
  const [isHovered, setIsHovered] = useState(false)

  return (
    <div
      style={{ opacity: isHovered ? 1 : opacity }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    />
  )
}
```

### Multiple Sheet Instances

```tsx
function Character({ id }) {
  const sheet = useMemo(() =>
    project.sheet('Character', id), [id]
  )

  // Each character has independent animation state
  return <CharacterMesh sheet={sheet} />
}
```
