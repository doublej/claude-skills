# ElevenLabs Conversational AI Reference

## Overview

End-to-end conversational AI platform with best-in-class voice synthesis. Supports voice, text, and multimodal agents. Includes batch calling for outbound automation.

## Features (Conversational AI 2.0)

- Natural turn-taking with custom models
- Integrated RAG for knowledge base
- Multimodal (voice + text)
- Batch calling for outbound
- MCP server support
- Claude, GPT, Gemini LLM support

## SDK Installation

```bash
# Python
pip install elevenlabs

# JavaScript
npm install @11labs/client

# React
npm install @11labs/react
```

## Agent Setup (Dashboard)

1. Create agent at elevenlabs.io/conversational-ai
2. Configure:
   - Voice (choose from library or clone)
   - LLM (GPT-4o, Claude 3.5, Gemini)
   - First message
   - System prompt
   - Knowledge base (optional)
   - Tools (optional)
3. Get agent ID

## Python Client

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="...")

# Start conversation
conversation = client.conversational_ai.start_conversation(
    agent_id="your-agent-id"
)

# WebSocket for real-time audio
import websockets
import asyncio

async def converse():
    async with websockets.connect(
        f"wss://api.elevenlabs.io/v1/convai/conversation?agent_id=...",
        extra_headers={"xi-api-key": "..."}
    ) as ws:
        # Send audio
        await ws.send(audio_bytes)

        # Receive
        async for message in ws:
            data = json.loads(message)
            if data["type"] == "audio":
                play_audio(base64.b64decode(data["audio"]))
```

## JavaScript Client

```javascript
import { Conversation } from '@11labs/client';

const conversation = await Conversation.startSession({
  agentId: 'your-agent-id',
  onMessage: (message) => {
    console.log('Message:', message);
  },
  onAudio: (audio) => {
    playAudio(audio);
  },
  onError: (error) => {
    console.error('Error:', error);
  }
});

// Send audio
conversation.sendAudio(audioBlob);

// Send text (for text-based interaction)
conversation.sendText("Hello");

// End
conversation.endSession();
```

## React Integration

```jsx
import { useConversation } from '@11labs/react';

function VoiceAssistant() {
  const conversation = useConversation({
    agentId: 'your-agent-id',
    onMessage: console.log
  });

  return (
    <div>
      <button onClick={() => conversation.startSession()}>
        Start
      </button>
      <button onClick={() => conversation.endSession()}>
        End
      </button>
      <p>Status: {conversation.status}</p>
    </div>
  );
}
```

## Agent Configuration API

```python
# Create agent
agent = client.conversational_ai.create_agent(
    name="Support Agent",
    first_message="Hi, how can I help you today?",
    system_prompt="You are a helpful customer support agent...",
    llm={
        "provider": "openai",
        "model": "gpt-4o"
    },
    voice={
        "voice_id": "rachel",
        "stability": 0.5,
        "similarity_boost": 0.8
    }
)

# Update agent
client.conversational_ai.update_agent(
    agent_id="...",
    system_prompt="Updated prompt..."
)
```

## Knowledge Base (RAG)

```python
# Add knowledge base
kb = client.conversational_ai.create_knowledge_base(
    agent_id="...",
    name="Product Docs",
    documents=[
        {"url": "https://docs.example.com"},
        {"file": open("manual.pdf", "rb")}
    ]
)

# Agent will automatically retrieve relevant context
```

## Tools / Function Calling

```python
# Define tools in agent config
tools = [
    {
        "name": "check_order_status",
        "description": "Check the status of a customer order",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"}
            },
            "required": ["order_id"]
        }
    }
]

# Handle tool calls via webhook
@app.post("/webhook")
async def handle_tool_call(request):
    data = await request.json()
    if data["type"] == "tool_call":
        tool_name = data["tool"]["name"]
        args = data["tool"]["arguments"]

        result = execute_tool(tool_name, args)

        return {"result": result}
```

## Batch Calling

```python
# Outbound call automation
batch = client.conversational_ai.create_batch_call(
    agent_id="...",
    phone_numbers=[
        "+1234567890",
        "+0987654321"
    ],
    scheduled_time="2025-01-15T10:00:00Z"
)

# Check status
status = client.conversational_ai.get_batch_call_status(batch.id)
```

## Voice Selection

```python
# List voices
voices = client.voices.get_all()

# Use preset voice
voice_id = "rachel"  # or pMsXgVXv3BLzUgSXRplE

# Clone voice
cloned = client.voices.clone(
    name="My Voice",
    files=["sample1.wav", "sample2.wav"]
)
```

## Multimodal (Voice + Text)

```javascript
// Same agent handles both voice and text
const conversation = await Conversation.startSession({
  agentId: 'your-agent-id',
  mode: 'multimodal'  // or 'voice' or 'text'
});

// Switch modes dynamically
conversation.setMode('text');
conversation.sendText("I prefer typing now");

conversation.setMode('voice');
// Resume voice interaction
```

## Webhook Integration

```python
# Configure webhook for events
client.conversational_ai.update_agent(
    agent_id="...",
    webhook_url="https://your-server.com/webhook"
)

# Receive events
@app.post("/webhook")
async def webhook(request):
    data = await request.json()

    if data["type"] == "conversation.started":
        log_conversation_start(data)

    elif data["type"] == "conversation.ended":
        save_transcript(data["transcript"])

    elif data["type"] == "tool_call":
        return handle_tool(data)
```

## Error Handling

```python
from elevenlabs.errors import APIError, RateLimitError

try:
    conversation = client.conversational_ai.start_conversation(...)
except RateLimitError:
    await asyncio.sleep(1)
    # Retry
except APIError as e:
    logger.error(f"API error: {e}")
```

## Pricing

- Free: 15 min/month
- Starter: $5/month, 30 min
- Creator: $22/month, 100 min
- Pro: $99/month, 500 min (~$0.20/min)
- Scale: $330/month, 2000 min (~$0.17/min)
- Enterprise: Custom

## Best Practices

- Use voice cloning for brand consistency
- Enable RAG for knowledge-intensive use cases
- Implement webhooks for tool calling and analytics
- Use batch calling for outbound campaigns
- Test with multimodal before voice-only deployment
