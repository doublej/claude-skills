---
name: voice-assistant
description: Build conversational voice assistants with real-time speech-to-speech capabilities. Covers Pipecat, LiveKit Agents, OpenAI Realtime API, and ElevenLabs. Use when building voice AI agents, real-time speech interfaces, AI companions, customer support bots, or multimodal conversational systems.
---

# Conversational Voice Assistant Development

## Framework Selection

| Framework | Language | Best For | Latency |
|-----------|----------|----------|---------|
| **Pipecat** | Python | Open-source, multimodal, full control | Ultra-low |
| **LiveKit Agents** | Python | Production, telephony, video | Low |
| **OpenAI Realtime API** | JS/Python | Speech-to-speech, quick setup | Low |
| **ElevenLabs ConvAI** | Multi-SDK | Best voice quality, batch calling | Low |

See `references/` for framework-specific patterns.

## Quick Start: Pipecat

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv init my-voice-agent && cd my-voice-agent
uv add "pipecat-ai[daily,openai,deepgram,cartesia]"
```

```python
import asyncio
from pipecat.pipeline import Pipeline
from pipecat.frames import TransportFrame
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.openai import OpenAILLMService
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.transports.daily import DailyTransport

async def main():
    transport = DailyTransport(room_url="...", token="...")

    pipeline = Pipeline([
        transport.input(),
        DeepgramSTTService(api_key="..."),
        OpenAILLMService(api_key="...", model="gpt-4o"),
        CartesiaTTSService(api_key="..."),
        transport.output()
    ])

    await pipeline.run()

asyncio.run(main())
```

## Quick Start: LiveKit Agents

```bash
pip install "livekit-agents[openai,silero,deepgram,cartesia,turn-detector]~=1.0"
```

```python
from livekit.agents import Agent, AgentSession, JobContext

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    agent = Agent(
        instructions="You are a friendly voice assistant. Be concise."
    )

    session = AgentSession(
        stt="deepgram/nova-3",
        llm="openai/gpt-4o",
        tts="cartesia/sonic-2"
    )

    await session.start(agent=agent, room=ctx.room)

# Run: python myagent.py dev
```

## Quick Start: OpenAI Realtime API

```javascript
import { RealtimeClient } from '@openai/realtime-api-beta';

const client = new RealtimeClient({ apiKey: process.env.OPENAI_API_KEY });

await client.connect();

client.updateSession({
  instructions: 'You are a helpful voice assistant.',
  voice: 'alloy',
  turn_detection: { type: 'server_vad' }
});

// Handle audio input/output
client.on('conversation.item.completed', ({ item }) => {
  console.log('Assistant:', item.formatted.transcript);
});
```

## Quick Start: ElevenLabs Conversational AI

```python
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai import ConversationalAI

client = ElevenLabs(api_key="...")

agent = ConversationalAI(
    agent_id="your-agent-id",
    llm="gpt-4o",
    voice_id="rachel",
    first_message="Hi, how can I help you today?"
)

# WebSocket connection for real-time conversation
async with agent.connect() as session:
    async for event in session:
        if event.type == "audio":
            play_audio(event.audio)
```

## Architecture Patterns

### Pipeline Architecture (Pipecat)
```
Audio In → STT → LLM → TTS → Audio Out
              ↓
         Context/Memory
```

### Agent-Session Pattern (LiveKit)
```
EntryPoint → Connect → Agent (instructions) → Session (STT+LLM+TTS) → Room
```

### Event-Driven Pattern (OpenAI Realtime)
```
WebSocket ↔ Server VAD → Model → Audio Stream
```

## Service Integrations

### Speech-to-Text (STT)
| Provider | Model | Best For |
|----------|-------|----------|
| Deepgram | Nova-3 | Speed, accuracy |
| OpenAI | Whisper | Multilingual |
| AssemblyAI | Universal | Diarization |
| Azure | Speech | Enterprise |

### Text-to-Speech (TTS)
| Provider | Voice | Best For |
|----------|-------|----------|
| ElevenLabs | Various | Most natural |
| Cartesia | Sonic-2 | Speed |
| OpenAI | Alloy/Echo | Consistency |
| PlayHT | PlayHT 2.0 | Cloning |

### LLMs
| Provider | Model | Best For |
|----------|-------|----------|
| OpenAI | gpt-4o, gpt-realtime | General, real-time |
| Anthropic | Claude 3.5 | Reasoning |
| Groq | Llama 3 | Speed |
| Gemini | 2.0 Flash | Multimodal |

## Key Features to Implement

### Turn Detection
```python
# Server-side VAD (Voice Activity Detection)
session = AgentSession(
    turn_detection="semantic"  # Uses transformer model
)

# OpenAI server VAD
client.updateSession({
    turn_detection: {
        type: 'server_vad',
        threshold: 0.5,
        silence_duration_ms: 500
    }
})
```

### Interruption Handling
```python
# Pipecat
@pipeline.on_interrupt
async def handle_interrupt():
    await tts.stop()
    await llm.cancel()

# LiveKit - built-in semantic turn detection
```

### Context/Memory
```python
# Store conversation history
context = []

async def on_message(user_text):
    context.append({"role": "user", "content": user_text})
    response = await llm.complete(context)
    context.append({"role": "assistant", "content": response})
```

### Tool/Function Calling
```python
# LiveKit with MCP
agent = Agent(
    instructions="...",
    mcp_servers=["filesystem", "web-search"]
)

# Pipecat function calling
@llm.function("get_weather")
async def get_weather(location: str):
    return await weather_api.fetch(location)
```

## Deployment Options

### Local Testing
```bash
# Pipecat
python main.py

# LiveKit
python myagent.py console  # Terminal testing
python myagent.py dev      # Hot reload
```

### Production
```bash
# LiveKit
python myagent.py start

# Docker
docker run -e OPENAI_API_KEY=... voice-agent
```

### Telephony Integration
```python
# LiveKit SIP
from livekit.agents import sip

sip.connect(
    phone_number="+1234567890",
    agent=agent
)

# ElevenLabs Batch Calling
agent.batch_call(phone_numbers=[...], message="...")
```

## Best Practices

### Latency Optimization
- Use streaming responses (don't wait for full LLM output)
- Pre-warm TTS with common phrases
- Use WebRTC for transport (lower latency than WebSocket)
- Choose geographically close STT/TTS providers

### Voice UX
- Keep responses concise (1-2 sentences)
- Use natural pauses and filler words sparingly
- Acknowledge user input quickly ("Got it", "Let me check")
- Handle "um", "uh" gracefully

### Error Handling
```python
async def handle_stt_error(error):
    await tts.speak("Sorry, I didn't catch that. Could you repeat?")

async def handle_network_error(error):
    # Reconnect logic with exponential backoff
    pass
```

### Privacy & Security
- Process audio in-memory, don't persist unless needed
- Use secure WebSocket (wss://) connections
- Validate user identity before sensitive operations
- Comply with call recording laws (two-party consent)

## Cost Considerations

| Service | Pricing Model |
|---------|---------------|
| Deepgram | ~$0.0043/min (Nova-3) |
| OpenAI Whisper | ~$0.006/min |
| ElevenLabs | ~$0.30/min (Pro) |
| OpenAI TTS | ~$0.015/1K chars |
| OpenAI Realtime | ~$0.06/min audio in, ~$0.24/min audio out |

## Resources

- **Pipecat**: https://github.com/pipecat-ai/pipecat | https://docs.pipecat.ai
- **LiveKit Agents**: https://github.com/livekit/agents
- **OpenAI Realtime**: https://platform.openai.com/docs/guides/realtime
- **ElevenLabs**: https://elevenlabs.io/docs/conversational-ai/overview
