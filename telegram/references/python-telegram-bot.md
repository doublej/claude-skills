# python-telegram-bot Reference

## Installation

```bash
pip install python-telegram-bot
# With optional dependencies
pip install "python-telegram-bot[job-queue]"
```

## Application Setup

```python
from telegram.ext import Application, CommandHandler, MessageHandler, filters

app = Application.builder().token("BOT_TOKEN").build()

# Add handlers
app.add_handler(CommandHandler("start", start_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

# Run
app.run_polling(allowed_updates=Update.ALL_TYPES)
```

## Handler Types

### CommandHandler

```python
from telegram.ext import CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(f"Hi {user.mention_html()}!")

app.add_handler(CommandHandler("start", start))
```

### MessageHandler with Filters

```python
from telegram.ext import MessageHandler, filters

# Text only
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# Photos
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

# Documents
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

# Voice/Audio
app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))

# Location
app.add_handler(MessageHandler(filters.LOCATION, handle_location))

# Specific user
app.add_handler(MessageHandler(filters.User(user_id=12345), handle_admin))

# Regex
app.add_handler(MessageHandler(filters.Regex(r"^hello", re.IGNORECASE), handle_hello))
```

### CallbackQueryHandler

```python
from telegram.ext import CallbackQueryHandler

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Required

    if query.data == "option1":
        await query.edit_message_text("You chose option 1")
    elif query.data.startswith("page_"):
        page = int(query.data.split("_")[1])
        await show_page(query, page)

# Match all callbacks
app.add_handler(CallbackQueryHandler(button))

# Match specific pattern
app.add_handler(CallbackQueryHandler(page_handler, pattern="^page_"))
```

### ConversationHandler

```python
from telegram.ext import ConversationHandler

WAITING_NAME, WAITING_EMAIL, CONFIRM = range(3)

async def start_registration(update, context):
    await update.message.reply_text("Enter your name:")
    return WAITING_NAME

async def receive_name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Enter your email:")
    return WAITING_EMAIL

async def receive_email(update, context):
    context.user_data["email"] = update.message.text
    name = context.user_data["name"]
    email = context.user_data["email"]

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Confirm", callback_data="confirm")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")],
    ])
    await update.message.reply_text(
        f"Name: {name}\nEmail: {email}\n\nConfirm?",
        reply_markup=keyboard
    )
    return CONFIRM

async def confirm_handler(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "confirm":
        # Save data
        await query.edit_message_text("Registration complete!")
    else:
        await query.edit_message_text("Cancelled.")

    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("register", start_registration)],
    states={
        WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
        WAITING_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_email)],
        CONFIRM: [CallbackQueryHandler(confirm_handler)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    per_message=False,  # For callback queries
)
```

## Job Queue (Scheduled Tasks)

```python
from telegram.ext import Application

async def reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="Reminder!")

async def set_reminder(update, context):
    chat_id = update.effective_chat.id

    # One-time job (60 seconds)
    context.job_queue.run_once(reminder, 60, chat_id=chat_id, name=str(chat_id))

    # Repeating job (every hour)
    context.job_queue.run_repeating(reminder, interval=3600, chat_id=chat_id)

    # Daily job (at specific time)
    from datetime import time
    context.job_queue.run_daily(reminder, time=time(9, 0), chat_id=chat_id)

# Remove job
def remove_job(name, context):
    jobs = context.job_queue.get_jobs_by_name(name)
    for job in jobs:
        job.schedule_removal()
```

## Persistence

```python
from telegram.ext import PicklePersistence

persistence = PicklePersistence(filepath="bot_data.pickle")

app = Application.builder().token("TOKEN").persistence(persistence).build()

# Data available in handlers:
# context.user_data - per user
# context.chat_data - per chat
# context.bot_data - global
```

## Keyboard Markup

### Inline Keyboard

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("URL", url="https://example.com")],
    [InlineKeyboardButton("Callback", callback_data="action")],
    [
        InlineKeyboardButton("1", callback_data="1"),
        InlineKeyboardButton("2", callback_data="2"),
    ],
])
```

### Reply Keyboard

```python
from telegram import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Option 1"), KeyboardButton("Option 2")],
        [KeyboardButton("Share Location", request_location=True)],
        [KeyboardButton("Share Contact", request_contact=True)],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

# Remove keyboard
from telegram import ReplyKeyboardRemove
await update.message.reply_text("Done", reply_markup=ReplyKeyboardRemove())
```

## Media Groups

```python
from telegram import InputMediaPhoto, InputMediaDocument

# Send multiple photos
media_group = [
    InputMediaPhoto(open("photo1.jpg", "rb"), caption="First"),
    InputMediaPhoto(open("photo2.jpg", "rb")),
    InputMediaPhoto("https://example.com/photo3.jpg"),
]
await update.message.reply_media_group(media_group)
```

## Error Handling

```python
from telegram.error import (
    TelegramError, Forbidden, NetworkError,
    BadRequest, TimedOut, ChatMigrated
)

async def error_handler(update, context):
    error = context.error

    if isinstance(error, Forbidden):
        # Bot blocked by user
        pass
    elif isinstance(error, BadRequest):
        if "Message is not modified" in str(error):
            pass  # Ignore
    elif isinstance(error, NetworkError):
        # Retry
        pass
    elif isinstance(error, ChatMigrated):
        new_chat_id = error.new_chat_id
        # Update stored chat_id
    else:
        raise error

app.add_error_handler(error_handler)
```

## Webhook Setup

```python
from flask import Flask, request

flask_app = Flask(__name__)
application = Application.builder().token("TOKEN").build()

@flask_app.post("/webhook")
async def webhook():
    update = Update.de_json(request.json, application.bot)
    await application.process_update(update)
    return "OK"

# Set webhook
async def setup():
    await application.bot.set_webhook(
        url="https://yourdomain.com/webhook",
        secret_token="your-secret",
        allowed_updates=["message", "callback_query"],
    )
```
