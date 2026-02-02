---
name: telegram
description: Build Telegram bots and integrate with the Telegram Bot API. Covers python-telegram-bot, Telethon (async), Telegraf.js (Node), and raw HTTP API. Use when creating Telegram bots, handling commands/messages, implementing inline keyboards, processing media, setting up webhooks, or managing conversation state.
---

# Telegram Bot Development

## Quick Start

### Get Bot Token

1. Message @BotFather on Telegram
2. Send `/newbot`, follow prompts
3. Copy token: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### Minimal Bot (Python)

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")

app = Application.builder().token("TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
```

### Minimal Bot (Node.js)

```javascript
const { Telegraf } = require('telegraf');
const bot = new Telegraf('TOKEN');
bot.start(ctx => ctx.reply('Hello!'));
bot.launch();
```

## Framework Selection

| Framework | Language | Best For |
|-----------|----------|----------|
| python-telegram-bot | Python | Most bots, sync/async |
| Telethon | Python | User accounts, MTProto |
| Telegraf.js | Node.js | JavaScript ecosystem |
| Raw HTTP | Any | Simple webhooks, serverless |

See `references/` for framework-specific patterns:
- `references/python-telegram-bot.md` - Python patterns
- `references/telegraf.md` - Node.js patterns
- `references/raw-api.md` - Direct HTTP API

## Core Patterns

### Command Handlers

```python
# Python
@app.command("help")
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available: /start, /help")

# With arguments
@app.command("echo")
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args) or "Nothing to echo"
    await update.message.reply_text(text)
```

### Inline Keyboards

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Option 1", callback_data="opt1")],
    [InlineKeyboardButton("Option 2", callback_data="opt2")],
])
await update.message.reply_text("Choose:", reply_markup=keyboard)

# Handle callback
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Always acknowledge
    await query.edit_message_text(f"Selected: {query.data}")

app.add_handler(CallbackQueryHandler(button_callback))
```

### Media Handling

```python
# Send photo
await update.message.reply_photo(photo=open("image.jpg", "rb"))
await update.message.reply_photo(photo="https://example.com/image.jpg")

# Send document
await update.message.reply_document(document=open("file.pdf", "rb"))

# Receive media
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]  # Highest resolution
    file = await context.bot.get_file(photo.file_id)
    await file.download_to_drive("downloaded.jpg")

app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
```

### Conversation State

```python
from telegram.ext import ConversationHandler, MessageHandler, filters

NAME, AGE = range(2)

async def start_form(update, context):
    await update.message.reply_text("What's your name?")
    return NAME

async def get_name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("How old are you?")
    return AGE

async def get_age(update, context):
    name = context.user_data["name"]
    age = update.message.text
    await update.message.reply_text(f"Hi {name}, age {age}!")
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("form", start_form)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
    },
    fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
)
```

## Deployment

### Polling (Development)

```python
app.run_polling()
```

### Webhook (Production)

```python
# Set webhook
await bot.set_webhook(url="https://yourdomain.com/webhook")

# Flask handler
@flask_app.post("/webhook")
def webhook():
    update = Update.de_json(request.json, bot)
    await app.process_update(update)
    return "ok"
```

### Serverless (AWS Lambda)

```python
import json
from telegram import Update, Bot

bot = Bot(token="TOKEN")

def handler(event, context):
    update = Update.de_json(json.loads(event["body"]), bot)
    # Process update
    return {"statusCode": 200, "body": "ok"}
```

## Common Bot Methods

| Method | Purpose |
|--------|---------|
| `send_message` | Send text |
| `send_photo/document/audio` | Send media |
| `edit_message_text` | Update message |
| `delete_message` | Remove message |
| `answer_callback_query` | Acknowledge button |
| `get_chat` | Get chat info |
| `get_chat_member` | Get user in chat |
| `ban_chat_member` | Ban user |

## Error Handling

```python
from telegram.error import TelegramError, NetworkError, TimedOut

async def error_handler(update, context):
    if isinstance(context.error, NetworkError):
        # Retry logic
        pass
    elif isinstance(context.error, TimedOut):
        # Timeout handling
        pass
    else:
        logger.error(f"Update {update} caused error {context.error}")

app.add_error_handler(error_handler)
```

## Rate Limits

- 30 messages/second to same chat
- 20 messages/minute to same group
- Bulk: max 30 messages/second overall
- Use `asyncio.sleep()` for bulk operations

## Security

- Validate webhook requests (check secret token)
- Never expose bot token
- Sanitize user input before using in commands
- Use `chat_id` to verify authorized users
