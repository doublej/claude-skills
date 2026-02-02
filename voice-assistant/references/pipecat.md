# Pipecat Framework Reference

## Overview

Open-source Python framework for building real-time voice and multimodal conversational AI. BSD-2-Clause license, 179+ contributors.

## Installation

```bash
# Core
uv add pipecat-ai

# With services
uv add "pipecat-ai[daily,openai,deepgram,cartesia,elevenlabs]"
```

## Service Extras

```bash
# STT
pipecat-ai[deepgram]
pipecat-ai[openai]     # Whisper
pipecat-ai[assemblyai]
pipecat-ai[azure]

# LLM
pipecat-ai[openai]
pipecat-ai[anthropic]
pipecat-ai[google]     # Gemini
pipecat-ai[groq]

# TTS
pipecat-ai[cartesia]
pipecat-ai[elevenlabs]
pipecat-ai[openai]
pipecat-ai[google]

# Transport
pipecat-ai[daily]      # WebRTC
pipecat-ai[websocket]
pipecat-ai[local]
```

## Pipeline Architecture

```python
from pipecat.pipeline import Pipeline
from pipecat.frames import Frame

# Frames flow through pipeline stages
pipeline = Pipeline([
    input_transport,    # Audio capture
    stt_service,        # Speech → Text
    llm_service,        # Text → Response
    tts_service,        # Response → Speech
    output_transport    # Audio playback
])
```

## Complete Example

```python
import asyncio
from pipecat.pipeline import Pipeline
from pipecat.frames import EndFrame
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.openai import OpenAILLMService
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.transports.daily import DailyTransport

async def main():
    # WebRTC transport via Daily
    transport = DailyTransport(
        room_url="https://your-domain.daily.co/room",
        token="...",
        bot_name="Assistant"
    )

    # Services
    stt = DeepgramSTTService(api_key="...")
    llm = OpenAILLMService(
        api_key="...",
        model="gpt-4o",
        system_prompt="You are a helpful voice assistant. Keep responses brief."
    )
    tts = CartesiaTTSService(
        api_key="...",
        voice_id="..."
    )

    # Build pipeline
    pipeline = Pipeline([
        transport.input(),
        stt,
        llm,
        tts,
        transport.output()
    ])

    # Run until EndFrame
    await pipeline.run()

asyncio.run(main())
```

## Custom Processors

```python
from pipecat.processors import FrameProcessor
from pipecat.frames import TextFrame

class SentimentFilter(FrameProcessor):
    async def process_frame(self, frame: Frame):
        if isinstance(frame, TextFrame):
            # Modify or filter frames
            if "angry" in frame.text.lower():
                frame.text = "[filtered]"
        await self.push_frame(frame)
```

## Function Calling

```python
from pipecat.services.openai import OpenAILLMService

llm = OpenAILLMService(
    api_key="...",
    model="gpt-4o",
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                }
            }
        }
    }]
)

@llm.on_function_call("get_weather")
async def handle_weather(location: str):
    return {"temperature": 72, "condition": "sunny"}
```

## Interruption Handling

```python
from pipecat.pipeline import Pipeline

pipeline = Pipeline([...])

@pipeline.on("user_started_speaking")
async def handle_interrupt():
    # Stop current TTS playback
    await tts.flush()
    # Cancel pending LLM generation
    await llm.cancel()
```

## Context Management

```python
from pipecat.services.openai import OpenAILLMService

llm = OpenAILLMService(
    api_key="...",
    model="gpt-4o",
    system_prompt="...",
    max_tokens=150,
    context_window=10  # Keep last 10 turns
)
```

## WebSocket Transport

```python
from pipecat.transports.websocket import WebSocketTransport

transport = WebSocketTransport(
    host="0.0.0.0",
    port=8765
)

# Client connects via ws://localhost:8765
```

## Local Testing

```python
from pipecat.transports.local import LocalTransport

# Uses microphone/speakers
transport = LocalTransport()
```

## Video Support

```python
from pipecat.services.heygen import HeyGenVideoService

video = HeyGenVideoService(
    api_key="...",
    avatar_id="..."
)

pipeline = Pipeline([
    transport.input(),
    stt,
    llm,
    tts,
    video,  # Generates avatar video
    transport.output()
])
```

## Error Handling

```python
from pipecat.pipeline import Pipeline

pipeline = Pipeline([...])

@pipeline.on("error")
async def handle_error(error):
    if "rate_limit" in str(error):
        await asyncio.sleep(1)
        # Retry
    else:
        logger.error(f"Pipeline error: {error}")
```

## Best Practices

- Use `async`/`await` throughout - Pipecat is async-first
- Keep LLM responses short for voice UX
- Pre-initialize services before pipeline starts
- Use WebRTC (Daily) for lowest latency
- Monitor frame queue sizes to detect bottlenecks
