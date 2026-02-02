# Maya1 TTS Server

FastAPI-based text-to-speech server using Maya1 model.

## Setup

Install dependencies:
```bash
uv sync
```

## Configuration

Create `.env` file:
```bash
echo "HF_TOKEN=your_huggingface_token" > .env
```

Login to HuggingFace:
```bash
huggingface-cli login
```

## Running

Start the server:
```bash
bash start.sh
```

Server runs on http://localhost:9527

## API Usage

Generate speech:
```bash
curl -X POST "http://localhost:9527/v1/tts/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Male voice in their 30s with american accent",
    "text": "Hello world <excited> this is amazing!",
    "stream": false
  }' \
  --output output.wav
```

## Emotion Tags

`<angry>`, `<chuckle>`, `<cry>`, `<curious>`, `<disappointed>`, `<excited>`, `<exhale>`, `<gasp>`, `<giggle>`, `<gulp>`, `<laugh>`, `<laugh_harder>`, `<mischievous>`, `<sarcastic>`, `<scream>`, `<sigh>`, `<sing>`, `<snort>`, `<whisper>`

## Endpoints

- `POST /v1/tts/generate` - Generate speech
- `GET /health` - Health check
- `GET /` - Service info
