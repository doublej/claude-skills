# Theatre.js Production Deployment

## Export Animation State

1. Open Studio in development
2. Click project name in Outline panel
3. Select "Export [Project Name]" from menu
4. Save `state.json` to your project

## Load State in Production

```typescript
import { getProject } from '@theatre/core'
import state from './state.json'

const project = getProject('My Project', { state })
```

## Remove Studio from Bundle

### Vite

```typescript
// main.ts
if (import.meta.env.DEV) {
  const studio = await import('@theatre/studio')
  studio.default.initialize()

  // For R3F
  const { default: extension } = await import('@theatre/r3f/dist/extension')
  studio.default.extend(extension)
}
```

### Webpack / Create React App

```typescript
if (process.env.NODE_ENV === 'development') {
  require('@theatre/studio').default.initialize()
}
```

### Conditional Imports (Tree-Shaking)

```typescript
// studio.ts
export async function initStudio() {
  if (import.meta.env.DEV) {
    const { default: studio } = await import('@theatre/studio')
    studio.initialize()
    return studio
  }
  return null
}

// main.ts
import { initStudio } from './studio'
await initStudio()
```

## Playback in Production

### Wait for Project Ready

```typescript
const project = getProject('My Project', { state })
const sheet = project.sheet('Scene')

// Always wait for ready before playing
project.ready.then(() => {
  sheet.sequence.play({ iterationCount: Infinity })
})
```

### User-Triggered Playback

```typescript
function App() {
  const [started, setStarted] = useState(false)

  const handleStart = async () => {
    await project.ready
    sheet.sequence.play()
    setStarted(true)
  }

  return (
    <>
      {!started && <button onClick={handleStart}>Start</button>}
      <Scene />
    </>
  )
}
```

### Scroll-Triggered Animation

```typescript
useEffect(() => {
  const handleScroll = () => {
    const progress = window.scrollY / (document.body.scrollHeight - window.innerHeight)
    sheet.sequence.position = progress * sheet.sequence.length
  }

  window.addEventListener('scroll', handleScroll)
  return () => window.removeEventListener('scroll', handleScroll)
}, [])
```

## Asset Management

### Using Assets in Production

```typescript
// In state.json, assets are stored as handles
// Use getAssetUrl to resolve

const textureHandle = obj.value.texture
const textureUrl = project.getAssetUrl(textureHandle)

const loader = new TextureLoader()
const texture = await loader.loadAsync(textureUrl)
```

### Asset Base Path

Configure asset loading path:

```typescript
const project = getProject('My Project', {
  state,
  assets: {
    baseUrl: '/assets/'  // or CDN URL
  }
})
```

## Licensing Notes

| Package | License | Production Use |
|---------|---------|----------------|
| @theatre/core | Apache 2.0 | Free |
| @theatre/studio | AGPL 3.0 | Dev only |
| @theatre/r3f | Apache 2.0 | Free |
| theatric | Apache 2.0 | Free |

**Important**: `@theatre/studio` is AGPL licensed. It must NOT be included in production bundles unless you comply with AGPL terms.

## Production Checklist

- [ ] Export state.json from Studio
- [ ] Import state in `getProject({ state })`
- [ ] Wrap `studio.initialize()` in dev check
- [ ] Verify Studio not in production bundle
- [ ] Add `project.ready` before playback
- [ ] Test animations with exported state
- [ ] Configure asset base URL if needed
- [ ] Test on target browsers/devices

## Bundle Size Tips

1. Dynamic imports for studio
2. Only import used packages
3. Use production builds (`npm run build`)
4. Verify tree-shaking works

```bash
# Check bundle contents
npx source-map-explorer dist/assets/*.js
```
