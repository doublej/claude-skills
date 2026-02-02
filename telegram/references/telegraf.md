# Telegraf.js Reference

## Installation

```bash
npm install telegraf
# TypeScript
npm install telegraf @types/node
```

## Basic Setup

```javascript
const { Telegraf } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start(ctx => ctx.reply('Welcome!'));
bot.help(ctx => ctx.reply('Send me a message'));

bot.launch();

// Graceful shutdown
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
```

## TypeScript Setup

```typescript
import { Telegraf, Context } from 'telegraf';
import { Update } from 'telegraf/types';

interface MyContext extends Context {
  myProp?: string;
}

const bot = new Telegraf<MyContext>(process.env.BOT_TOKEN!);
```

## Command Handlers

```javascript
// Basic command
bot.command('start', ctx => ctx.reply('Hello!'));

// With arguments
bot.command('echo', ctx => {
  const args = ctx.message.text.split(' ').slice(1).join(' ');
  return ctx.reply(args || 'Nothing to echo');
});

// Multiple commands
bot.command(['help', 'h'], ctx => ctx.reply('Help message'));
```

## Message Handlers

```javascript
// Text messages
bot.on('text', ctx => ctx.reply(`You said: ${ctx.message.text}`));

// Photos
bot.on('photo', async ctx => {
  const photo = ctx.message.photo.pop(); // Highest res
  const file = await ctx.telegram.getFile(photo.file_id);
  ctx.reply(`Photo received: ${file.file_path}`);
});

// Documents
bot.on('document', ctx => {
  const doc = ctx.message.document;
  ctx.reply(`File: ${doc.file_name} (${doc.mime_type})`);
});

// Location
bot.on('location', ctx => {
  const { latitude, longitude } = ctx.message.location;
  ctx.reply(`Location: ${latitude}, ${longitude}`);
});

// Stickers
bot.on('sticker', ctx => ctx.reply('Nice sticker!'));

// Any message
bot.on('message', ctx => ctx.reply('Got a message'));
```

## Inline Keyboards

```javascript
const { Markup } = require('telegraf');

bot.command('menu', ctx => {
  return ctx.reply('Choose option:', Markup.inlineKeyboard([
    [Markup.button.callback('Option 1', 'opt1')],
    [Markup.button.callback('Option 2', 'opt2')],
    [Markup.button.url('Visit Site', 'https://example.com')],
  ]));
});

// Handle callbacks
bot.action('opt1', ctx => {
  ctx.answerCbQuery(); // Required
  return ctx.editMessageText('You chose option 1');
});

// Pattern matching
bot.action(/^page_(\d+)$/, ctx => {
  const page = ctx.match[1];
  ctx.answerCbQuery();
  return ctx.editMessageText(`Page ${page}`);
});
```

## Reply Keyboards

```javascript
const { Markup } = require('telegraf');

bot.command('keyboard', ctx => {
  return ctx.reply('Choose:', Markup.keyboard([
    ['Option A', 'Option B'],
    ['Option C'],
    [Markup.button.contactRequest('Share Contact')],
    [Markup.button.locationRequest('Share Location')],
  ]).resize().oneTime());
});

// Remove keyboard
bot.command('done', ctx => {
  return ctx.reply('Done', Markup.removeKeyboard());
});
```

## Scenes (Conversation State)

```javascript
const { Scenes, session } = require('telegraf');

// Create wizard scene
const registerWizard = new Scenes.WizardScene(
  'register',
  // Step 1
  async ctx => {
    await ctx.reply('Enter your name:');
    return ctx.wizard.next();
  },
  // Step 2
  async ctx => {
    ctx.wizard.state.name = ctx.message.text;
    await ctx.reply('Enter your email:');
    return ctx.wizard.next();
  },
  // Step 3
  async ctx => {
    ctx.wizard.state.email = ctx.message.text;
    const { name, email } = ctx.wizard.state;
    await ctx.reply(`Name: ${name}\nEmail: ${email}\nRegistered!`);
    return ctx.scene.leave();
  }
);

// Setup
const stage = new Scenes.Stage([registerWizard]);
bot.use(session());
bot.use(stage.middleware());

bot.command('register', ctx => ctx.scene.enter('register'));
```

## Middleware

```javascript
// Logging
bot.use(async (ctx, next) => {
  const start = Date.now();
  await next();
  const ms = Date.now() - start;
  console.log(`Response time: ${ms}ms`);
});

// Auth middleware
const adminOnly = async (ctx, next) => {
  const adminIds = [12345, 67890];
  if (!adminIds.includes(ctx.from?.id)) {
    return ctx.reply('Not authorized');
  }
  return next();
};

bot.command('admin', adminOnly, ctx => ctx.reply('Admin area'));
```

## Session

```javascript
const { session } = require('telegraf');

// In-memory session
bot.use(session());

bot.command('count', ctx => {
  ctx.session.count = (ctx.session.count || 0) + 1;
  return ctx.reply(`Count: ${ctx.session.count}`);
});

// Redis session
const { Redis } = require('@telegraf/session/redis');

bot.use(session({
  store: Redis({ url: 'redis://localhost:6379' })
}));
```

## Media Handling

```javascript
// Send photo
bot.command('photo', ctx => {
  return ctx.replyWithPhoto({ source: './image.jpg' });
  // Or URL
  return ctx.replyWithPhoto('https://example.com/image.jpg');
  // Or file_id
  return ctx.replyWithPhoto('AgACAgIAAxk...');
});

// Send document
bot.command('file', ctx => {
  return ctx.replyWithDocument(
    { source: './file.pdf' },
    { caption: 'Here is your file' }
  );
});

// Media group
bot.command('album', ctx => {
  return ctx.replyWithMediaGroup([
    { type: 'photo', media: { source: './photo1.jpg' } },
    { type: 'photo', media: { source: './photo2.jpg' } },
  ]);
});

// Download file
bot.on('document', async ctx => {
  const file = await ctx.telegram.getFile(ctx.message.document.file_id);
  const url = `https://api.telegram.org/file/bot${token}/${file.file_path}`;
  // Download from url
});
```

## Webhook Setup

```javascript
const { Telegraf } = require('telegraf');
const express = require('express');

const bot = new Telegraf(process.env.BOT_TOKEN);
const app = express();

// Webhook handler
app.use(bot.webhookCallback('/webhook'));

// Set webhook
bot.telegram.setWebhook('https://yourdomain.com/webhook');

app.listen(3000);
```

## Error Handling

```javascript
bot.catch((err, ctx) => {
  console.error(`Error for ${ctx.updateType}:`, err);

  if (err.code === 403) {
    // Bot blocked by user
  } else if (err.code === 400) {
    // Bad request
  }
});
```

## Telegraf Context Shortcuts

```javascript
ctx.reply(text)              // sendMessage
ctx.replyWithPhoto(photo)    // sendPhoto
ctx.replyWithDocument(doc)   // sendDocument
ctx.replyWithAudio(audio)    // sendAudio
ctx.replyWithVideo(video)    // sendVideo
ctx.replyWithSticker(sticker)// sendSticker
ctx.replyWithLocation(lat, lon)
ctx.editMessageText(text)    // editMessageText
ctx.deleteMessage()          // deleteMessage
ctx.answerCbQuery(text)      // answerCallbackQuery
ctx.telegram.sendMessage(chatId, text)  // Direct API
```
