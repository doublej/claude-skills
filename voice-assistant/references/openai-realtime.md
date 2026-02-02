# OpenAI Realtime API Reference

## Overview

Speech-to-speech API with native audio understanding. Uses `gpt-realtime` model optimized for voice interactions. Supports WebRTC (browser) and WebSocket connections.

## Key Features

- Native speech-to-speech (no intermediate text)
- Server-side VAD (voice activity detection)
- Interruption handling
- Function calling
- MCP server support
- SIP phone calling
- Image input support

## JavaScript Setup

```bash
npm install @openai/realtime-api-beta
```

```javascript
import { RealtimeClient } from '@openai/realtime-api-beta';

const client = new RealtimeClient({
  apiKey: process.env.OPENAI_API_KEY
});

await client.connect();
```

## Session Configuration

```javascript
client.updateSession({
  // Voice selection
  voice: 'alloy',  // alloy, echo, fable, onyx, nova, shimmer

  // System instructions
  instructions: `You are a helpful voice assistant.
    Keep responses concise and conversational.`,

  // Turn detection
  turn_detection: {
    type: 'server_vad',
    threshold: 0.5,
    prefix_padding_ms: 300,
    silence_duration_ms: 500
  },

  // Input/output audio format
  input_audio_format: 'pcm16',
  output_audio_format: 'pcm16',

  // Temperature
  temperature: 0.8,

  // Max response length
  max_response_output_tokens: 4096
});
```

## Audio Input

```javascript
// Send audio chunks
client.appendInputAudio(audioData);  // Int16Array or base64

// Commit when done (if not using VAD)
client.createResponse();
```

## Event Handling

```javascript
// Transcription events
client.on('conversation.item.input_audio_transcription.completed', ({ transcript }) => {
  console.log('User:', transcript);
});

// Response audio
client.on('response.audio.delta', ({ delta }) => {
  playAudio(delta);  // base64 audio chunk
});

// Response text
client.on('response.audio_transcript.delta', ({ delta }) => {
  console.log('Assistant:', delta);
});

// Response complete
client.on('response.done', ({ response }) => {
  console.log('Response finished');
});

// Errors
client.on('error', ({ error }) => {
  console.error('Error:', error);
});
```

## Function Calling

```javascript
// Define tools
client.addTool({
  name: 'get_weather',
  description: 'Get current weather for a location',
  parameters: {
    type: 'object',
    properties: {
      location: { type: 'string', description: 'City name' }
    },
    required: ['location']
  }
}, async ({ location }) => {
  // Tool implementation
  const weather = await fetchWeather(location);
  return { temperature: weather.temp, condition: weather.condition };
});

// Handle tool calls
client.on('conversation.item.created', async ({ item }) => {
  if (item.type === 'function_call') {
    // Tool is called automatically if handler provided
  }
});
```

## Interruption Handling

```javascript
// Server VAD handles interruptions automatically
client.on('input_audio_buffer.speech_started', () => {
  // User started speaking - current response may be interrupted
});

client.on('input_audio_buffer.speech_stopped', () => {
  // User stopped speaking
});

// Cancel current response manually
client.cancelResponse();
```

## WebRTC (Browser)

```javascript
// Browser: Use WebRTC for lower latency
const pc = new RTCPeerConnection();

// Add audio track from microphone
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
pc.addTrack(stream.getTracks()[0]);

// Handle remote audio
pc.ontrack = (event) => {
  const audio = document.createElement('audio');
  audio.srcObject = event.streams[0];
  audio.play();
};

// Connect to OpenAI Realtime
const offer = await pc.createOffer();
await pc.setLocalDescription(offer);

const response = await fetch('https://api.openai.com/v1/realtime/connect', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/sdp'
  },
  body: offer.sdp
});

const answer = await response.text();
await pc.setRemoteDescription({ type: 'answer', sdp: answer });
```

## Python Setup

```bash
pip install openai
```

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def main():
    async with client.beta.realtime.connect(
        model="gpt-4o-realtime-preview"
    ) as conn:
        await conn.session.update(
            session={
                "voice": "alloy",
                "instructions": "You are a helpful assistant.",
                "turn_detection": {"type": "server_vad"}
            }
        )

        # Send audio
        await conn.input_audio_buffer.append(audio_data)

        # Receive responses
        async for event in conn:
            if event.type == "response.audio.delta":
                play_audio(event.delta)

asyncio.run(main())
```

## MCP Integration

```javascript
client.updateSession({
  tools: [{
    type: 'mcp',
    server_label: 'filesystem',
    server_url: 'mcp://localhost:3000'
  }]
});
```

## Image Input

```javascript
// Send image for multimodal conversation
client.sendUserMessageContent([
  { type: 'input_text', text: 'What do you see?' },
  {
    type: 'input_image',
    image: {
      url: 'data:image/jpeg;base64,...'
    }
  }
]);
```

## Conversation History

```javascript
// Get conversation items
const items = client.conversation.getItems();

// Add context from previous conversation
client.sendUserMessageContent([
  { type: 'input_text', text: 'Previous context: ...' }
]);
```

## Error Handling

```javascript
client.on('error', ({ error }) => {
  switch (error.code) {
    case 'rate_limit_exceeded':
      // Wait and retry
      break;
    case 'invalid_audio':
      // Check audio format
      break;
    case 'session_expired':
      // Reconnect
      break;
  }
});
```

## Pricing

- Audio input: ~$0.06/min
- Audio output: ~$0.24/min
- Text (if used): Standard GPT-4o pricing
- No session limits (as of Feb 2025)

## Best Practices

- Use WebRTC in browsers for lowest latency
- Keep instructions concise for faster responses
- Use server VAD for natural turn-taking
- Handle interruptions gracefully
- Implement reconnection logic for production
- Monitor token usage for cost control
