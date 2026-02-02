# LiveKit Agents Framework Reference

## Overview

Production-ready Python framework for building realtime voice agents. Apache-2.0 license. Supports telephony, video, and multimodal interactions.

## Installation

```bash
pip install "livekit-agents[openai,silero,deepgram,cartesia,turn-detector]~=1.0"
```

## Core Concepts

- **Agent**: LLM-based application with instructions
- **AgentSession**: Container managing user interactions
- **entrypoint**: Starting point (like a web request handler)

## Minimal Example

```python
from livekit.agents import Agent, AgentSession, JobContext, cli

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    agent = Agent(instructions="You are a friendly voice assistant.")

    session = AgentSession(
        stt="deepgram/nova-3",
        llm="openai/gpt-4o",
        tts="cartesia/sonic-2"
    )

    await session.start(agent=agent, room=ctx.room)

if __name__ == "__main__":
    cli.run_app(entrypoint)
```

## Running Modes

```bash
# Local testing with terminal I/O
python myagent.py console

# Development with hot reload
python myagent.py dev

# Production
python myagent.py start
```

## Agent Configuration

```python
agent = Agent(
    instructions="""You are a customer support agent for Acme Inc.
    Be helpful and concise. If you don't know something, say so.""",

    # MCP server integration
    mcp_servers=["filesystem", "web-search"],

    # Function tools
    tools=[get_order_status, check_inventory]
)
```

## Session Configuration

```python
session = AgentSession(
    # STT options
    stt="deepgram/nova-3",

    # LLM options
    llm="openai/gpt-4o",

    # TTS options
    tts="cartesia/sonic-2",

    # Turn detection
    turn_detection="semantic",  # Uses transformer model

    # Voice activity detection
    vad="silero"
)
```

## Provider Shortcuts

### STT
- `deepgram/nova-3` - Fast, accurate
- `openai/whisper` - Multilingual
- `azure/speech` - Enterprise

### LLM
- `openai/gpt-4o` - General purpose
- `openai/gpt-4o-mini` - Faster, cheaper
- `anthropic/claude-3-5-sonnet` - Strong reasoning

### TTS
- `cartesia/sonic-2` - Fast, natural
- `elevenlabs/multilingual-v2` - Best quality
- `openai/tts-1` - Consistent

## Function Tools

```python
from livekit.agents import function_tool

@function_tool
async def get_weather(location: str) -> str:
    """Get current weather for a location."""
    # Implementation
    return f"Weather in {location}: 72F, sunny"

@function_tool
async def book_appointment(date: str, time: str) -> str:
    """Book an appointment."""
    return f"Booked for {date} at {time}"

agent = Agent(
    instructions="...",
    tools=[get_weather, book_appointment]
)
```

## MCP Integration

```python
agent = Agent(
    instructions="You can search the web and access files.",
    mcp_servers=[
        "web-search",      # Built-in web search
        "filesystem",      # File access
        "my-custom-mcp"    # Custom MCP server
    ]
)
```

## Event Handling

```python
session = AgentSession(...)

@session.on("user_speech_started")
async def on_speech_start():
    # User started talking
    pass

@session.on("user_speech_ended")
async def on_speech_end(transcript: str):
    print(f"User said: {transcript}")

@session.on("agent_speech_started")
async def on_agent_start():
    pass

@session.on("agent_speech_ended")
async def on_agent_end():
    pass
```

## Multi-Agent Handoff

```python
support_agent = Agent(instructions="You handle customer support...")
sales_agent = Agent(instructions="You handle sales inquiries...")

@function_tool
async def transfer_to_sales():
    """Transfer call to sales department."""
    await session.handoff(sales_agent)
    return "Transferring you to sales..."

support_agent.tools.append(transfer_to_sales)
```

## Telephony (SIP)

```python
from livekit.agents import sip

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    # Handle inbound calls
    if ctx.job.call_info:
        caller = ctx.job.call_info.caller_number
        print(f"Incoming call from {caller}")

    agent = Agent(instructions="...")
    session = AgentSession(...)
    await session.start(agent=agent, room=ctx.room)

# Outbound call
await sip.dial(
    phone_number="+1234567890",
    room=room,
    participant_identity="outbound-call"
)
```

## Video Avatars

```python
from livekit.agents import video

session = AgentSession(
    stt="deepgram/nova-3",
    llm="openai/gpt-4o",
    tts="cartesia/sonic-2",
    avatar="heygen/avatar-id"  # Video avatar
)
```

## Testing Framework

```python
from livekit.agents.testing import AgentTest

class MyAgentTest(AgentTest):
    async def test_greeting(self):
        response = await self.say("Hello")
        self.assertIn("hello", response.lower())

    async def test_weather_tool(self):
        response = await self.say("What's the weather in NYC?")
        self.assertToolCalled("get_weather")
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "myagent.py", "start"]
```

### Environment Variables

```bash
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
OPENAI_API_KEY=...
DEEPGRAM_API_KEY=...
CARTESIA_API_KEY=...
```

## Best Practices

- Use semantic turn detection for natural conversations
- Keep agent instructions focused and concise
- Implement proper error handling for production
- Use MCP for complex tool integrations
- Test with the built-in testing framework
