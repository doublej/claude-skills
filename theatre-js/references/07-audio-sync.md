# Theatre.js Audio Synchronization

## Basic Audio Attachment

```typescript
const sheet = project.sheet('Scene')

// Attach audio file
sheet.sequence.attachAudio({
  source: '/audio/soundtrack.mp3'
}).then(() => {
  console.log('Audio loaded!')
  sheet.sequence.play()
})
```

## Audio Sources

### URL String

```typescript
sheet.sequence.attachAudio({
  source: 'https://example.com/audio.mp3'
})
```

### AudioBuffer

```typescript
const audioContext = new AudioContext()
const response = await fetch('/audio.mp3')
const arrayBuffer = await response.arrayBuffer()
const audioBuffer = await audioContext.decodeAudioData(arrayBuffer)

sheet.sequence.attachAudio({
  source: audioBuffer
})
```

### HTMLAudioElement

```typescript
const audio = new Audio('/audio.mp3')
await audio.load()

sheet.sequence.attachAudio({
  source: audio
})
```

## Browser Autoplay Restrictions

Browsers block audio until user interaction. Handle this properly:

```typescript
// Show play button for user interaction
function App() {
  const [ready, setReady] = useState(false)

  const handlePlay = async () => {
    await sheet.sequence.attachAudio({
      source: '/audio/music.mp3'
    })
    sheet.sequence.play()
    setReady(true)
  }

  return (
    <>
      {!ready && (
        <button onClick={handlePlay}>
          Click to Start
        </button>
      )}
      <Scene />
    </>
  )
}
```

## Custom Audio Graph

Control audio processing with Web Audio API:

```typescript
const audioContext = new AudioContext()

// Create custom audio graph
const gainNode = audioContext.createGain()
gainNode.gain.value = 0.5

gainNode.connect(audioContext.destination)

sheet.sequence.attachAudio({
  source: '/audio.mp3',
  audioContext,
  destinationNode: gainNode  // Route through gain
})
```

## Effects Chain Example

```typescript
const audioContext = new AudioContext()

// Create effects
const compressor = audioContext.createDynamicsCompressor()
const reverb = audioContext.createConvolver()
const masterGain = audioContext.createGain()

// Connect chain
compressor.connect(reverb)
reverb.connect(masterGain)
masterGain.connect(audioContext.destination)

// Attach with custom destination
sheet.sequence.attachAudio({
  source: audioBuffer,
  audioContext,
  destinationNode: compressor
})
```

## Accessing Theatre's Audio Graph

```typescript
const { decodedBuffer, audioContext, gainNode } = await sheet.sequence.attachAudio({
  source: '/audio.mp3'
})

// Modify Theatre's gain node
gainNode.gain.value = 0.8

// Access decoded audio data
console.log('Duration:', decodedBuffer.duration)
console.log('Sample rate:', decodedBuffer.sampleRate)
```

## Audio Visualization

```typescript
const audioContext = new AudioContext()
const analyser = audioContext.createAnalyser()
analyser.fftSize = 256

const { gainNode } = await sheet.sequence.attachAudio({
  source: '/audio.mp3',
  audioContext
})

// Insert analyser before destination
gainNode.disconnect()
gainNode.connect(analyser)
analyser.connect(audioContext.destination)

// Read frequency data
const dataArray = new Uint8Array(analyser.frequencyBinCount)

function animate() {
  analyser.getByteFrequencyData(dataArray)
  // Use dataArray for visualization
  requestAnimationFrame(animate)
}
animate()
```

## Sync Considerations

- Audio and animation are tightly synchronized
- Sequence position controls audio playback position
- Pause/play affects both animation and audio
- Seeking updates audio position instantly

```typescript
// Seek to specific time (audio follows)
sheet.sequence.position = 10.5

// Pause both animation and audio
sheet.sequence.pause()

// Resume both
sheet.sequence.play()
```

## Multiple Audio Tracks

Theatre.js supports one audio per sequence. For multiple tracks:

```typescript
// Option 1: Pre-mix audio files
// Mix tracks in audio editor before importing

// Option 2: Use Web Audio API for additional sounds
const sfxContext = new AudioContext()
const sfxBuffer = await loadAudio('/sfx/explosion.mp3')

// Trigger SFX at specific animation points
obj.onValuesChange((values) => {
  if (values.triggerExplosion) {
    const source = sfxContext.createBufferSource()
    source.buffer = sfxBuffer
    source.connect(sfxContext.destination)
    source.start()
  }
})
```

## Production Tips

1. Preload audio before showing play button
2. Handle AudioContext suspension on mobile
3. Provide volume controls for accessibility
4. Consider fallback for unsupported browsers
5. Keep audio files reasonably sized (compress)
