# Telegram Bot API - Raw HTTP Reference

## Base URL

```
https://api.telegram.org/bot<token>/<method>
```

## Authentication

All requests require the bot token in the URL path:
```
https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getMe
```

## Request Methods

Both GET and POST work for all methods. POST recommended for:
- Sending files
- Large payloads
- Sensitive data

### Content Types

```
application/json           - JSON body
multipart/form-data        - File uploads
application/x-www-form-urlencoded - Form data
```

## Common Methods

### getMe

```bash
curl "https://api.telegram.org/bot$TOKEN/getMe"
```

### sendMessage

```bash
curl -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": 12345678,
    "text": "Hello!",
    "parse_mode": "HTML"
  }'
```

### sendPhoto

```bash
# URL
curl -X POST "https://api.telegram.org/bot$TOKEN/sendPhoto" \
  -d "chat_id=12345678" \
  -d "photo=https://example.com/image.jpg" \
  -d "caption=My photo"

# File upload
curl -X POST "https://api.telegram.org/bot$TOKEN/sendPhoto" \
  -F "chat_id=12345678" \
  -F "photo=@/path/to/image.jpg" \
  -F "caption=My photo"
```

### sendDocument

```bash
curl -X POST "https://api.telegram.org/bot$TOKEN/sendDocument" \
  -F "chat_id=12345678" \
  -F "document=@/path/to/file.pdf" \
  -F "caption=Your document"
```

### getUpdates (Polling)

```bash
curl "https://api.telegram.org/bot$TOKEN/getUpdates?offset=0&timeout=30"
```

### setWebhook

```bash
curl -X POST "https://api.telegram.org/bot$TOKEN/setWebhook" \
  -d "url=https://yourdomain.com/webhook" \
  -d "secret_token=your-secret-token"
```

### deleteWebhook

```bash
curl "https://api.telegram.org/bot$TOKEN/deleteWebhook?drop_pending_updates=true"
```

## Python Raw Implementation

```python
import requests

TOKEN = "your-bot-token"
BASE = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text, **kwargs):
    return requests.post(f"{BASE}/sendMessage", json={
        "chat_id": chat_id,
        "text": text,
        **kwargs
    }).json()

def send_photo(chat_id, photo, caption=None):
    if photo.startswith("http"):
        return requests.post(f"{BASE}/sendPhoto", json={
            "chat_id": chat_id,
            "photo": photo,
            "caption": caption
        }).json()
    else:
        with open(photo, "rb") as f:
            return requests.post(f"{BASE}/sendPhoto", data={
                "chat_id": chat_id,
                "caption": caption
            }, files={"photo": f}).json()

def get_updates(offset=None, timeout=30):
    params = {"timeout": timeout}
    if offset:
        params["offset"] = offset
    return requests.get(f"{BASE}/getUpdates", params=params).json()

# Polling loop
def poll():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get("result", []):
            offset = update["update_id"] + 1
            handle_update(update)

def handle_update(update):
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")

        if text.startswith("/start"):
            send_message(chat_id, "Hello!")
```

## Node.js Raw Implementation

```javascript
const fetch = require('node-fetch');
const FormData = require('form-data');
const fs = require('fs');

const TOKEN = process.env.BOT_TOKEN;
const BASE = `https://api.telegram.org/bot${TOKEN}`;

async function sendMessage(chatId, text, options = {}) {
  const res = await fetch(`${BASE}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: chatId, text, ...options })
  });
  return res.json();
}

async function sendPhoto(chatId, photo, caption) {
  if (photo.startsWith('http')) {
    const res = await fetch(`${BASE}/sendPhoto`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, photo, caption })
    });
    return res.json();
  }

  const form = new FormData();
  form.append('chat_id', chatId);
  form.append('photo', fs.createReadStream(photo));
  if (caption) form.append('caption', caption);

  const res = await fetch(`${BASE}/sendPhoto`, { method: 'POST', body: form });
  return res.json();
}

async function getUpdates(offset, timeout = 30) {
  const params = new URLSearchParams({ timeout });
  if (offset) params.set('offset', offset);

  const res = await fetch(`${BASE}/getUpdates?${params}`);
  return res.json();
}
```

## Webhook Handler (Express)

```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.post('/webhook', (req, res) => {
  const update = req.body;

  if (update.message) {
    const chatId = update.message.chat.id;
    const text = update.message.text || '';

    if (text === '/start') {
      sendMessage(chatId, 'Hello!');
    }
  }

  res.sendStatus(200);
});

app.listen(3000);
```

## Webhook Handler (Python Flask)

```python
from flask import Flask, request
import requests

app = Flask(__name__)

@app.post("/webhook")
def webhook():
    update = request.json

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "Hello!")

    return "OK"
```

## Serverless (AWS Lambda)

```python
import json
import urllib.request

TOKEN = "your-token"
BASE = f"https://api.telegram.org/bot{TOKEN}"

def handler(event, context):
    body = json.loads(event["body"])

    if "message" in body:
        chat_id = body["message"]["chat"]["id"]
        text = body["message"].get("text", "")

        if text == "/start":
            data = json.dumps({"chat_id": chat_id, "text": "Hello!"}).encode()
            req = urllib.request.Request(
                f"{BASE}/sendMessage",
                data=data,
                headers={"Content-Type": "application/json"}
            )
            urllib.request.urlopen(req)

    return {"statusCode": 200, "body": "ok"}
```

## Response Format

All responses follow this structure:

```json
{
  "ok": true,
  "result": { ... }
}
```

Error response:
```json
{
  "ok": false,
  "error_code": 400,
  "description": "Bad Request: message text is empty"
}
```

## Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| chat_id | int/string | Target chat ID or @username |
| text | string | Message text |
| parse_mode | string | "HTML" or "MarkdownV2" |
| reply_markup | object | Keyboard markup |
| disable_notification | bool | Silent message |
| reply_to_message_id | int | Reply to message |

## Formatting

### HTML

```html
<b>bold</b>
<i>italic</i>
<u>underline</u>
<s>strikethrough</s>
<code>inline code</code>
<pre>code block</pre>
<a href="http://example.com">link</a>
```

### MarkdownV2

```
*bold*
_italic_
__underline__
~strikethrough~
`inline code`
```code block```
[link](http://example.com)
```

Escape these characters: `_*[]()~`>#+-=|{}.!`

## Inline Keyboard

```json
{
  "reply_markup": {
    "inline_keyboard": [
      [{"text": "Button 1", "callback_data": "btn1"}],
      [{"text": "URL", "url": "https://example.com"}]
    ]
  }
}
```

## Reply Keyboard

```json
{
  "reply_markup": {
    "keyboard": [
      [{"text": "Option 1"}, {"text": "Option 2"}],
      [{"text": "Share Location", "request_location": true}]
    ],
    "resize_keyboard": true,
    "one_time_keyboard": true
  }
}
```
