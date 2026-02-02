---
name: twilio-api
description: "Expert guidance for implementing Twilio API integrations including SMS, voice calls, WhatsApp, email, and video. Use when building communication features with Twilio services."
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
metadata:
  category: "api-integration"
  version: "1.0"
  twilio_api_version: "2010-04-01"
---

# Twilio API Integration Skill

## Overview

This skill provides comprehensive guidance for integrating Twilio's communication APIs into applications. Twilio enables developers to programmatically send/receive SMS, make voice calls, send WhatsApp messages, send emails via SendGrid, implement video calls, and more.

## When to Use This Skill

Use this skill when:
- Building SMS messaging functionality (notifications, 2FA, alerts)
- Implementing voice calling features (IVR, call forwarding, conferencing)
- Adding WhatsApp Business messaging
- Sending transactional or marketing emails (via SendGrid)
- Building video chat or conferencing features (Twilio Video)
- Implementing phone number verification
- Creating chatbots or conversational AI with messaging
- Setting up webhook handlers for Twilio callbacks

## Quick Start

### Installation

```bash
# Node.js
npm install twilio

# Python
pip install twilio

# Ruby
gem install twilio-ruby

# PHP
composer require twilio/sdk

# C# / .NET
dotnet add package Twilio
```

### Basic Authentication

All Twilio API requests require your Account SID and Auth Token:

```javascript
// Node.js
const twilio = require('twilio');
const client = twilio(accountSid, authToken);
```

```python
# Python
from twilio.rest import Client
client = Client(account_sid, auth_token)
```

**Security Best Practice:** Never hardcode credentials. Use environment variables:
```bash
export TWILIO_ACCOUNT_SID='ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
export TWILIO_AUTH_TOKEN='your_auth_token'
```

## Core Twilio Services

### 1. SMS Messaging

**Send SMS:**
```javascript
// Node.js
const message = await client.messages.create({
  body: 'Hello from Twilio!',
  from: '+15551234567',  // Your Twilio number
  to: '+15559876543'     // Recipient number
});
console.log(message.sid);
```

```python
# Python
message = client.messages.create(
    body='Hello from Twilio!',
    from_='+15551234567',
    to='+15559876543'
)
print(message.sid)
```

**Receive SMS (Webhook Handler):**
```javascript
// Express.js
const express = require('express');
const MessagingResponse = require('twilio').twiml.MessagingResponse;

app.post('/sms', (req, res) => {
  const twiml = new MessagingResponse();
  const incomingMsg = req.body.Body;
  const fromNumber = req.body.From;

  twiml.message(`You said: ${incomingMsg}`);
  res.type('text/xml').send(twiml.toString());
});
```

### 2. Voice Calls

**Make Outbound Call:**
```javascript
const call = await client.calls.create({
  url: 'http://demo.twilio.com/docs/voice.xml',  // TwiML instructions
  to: '+15559876543',
  from: '+15551234567'
});
```

**Handle Incoming Call (TwiML):**
```javascript
const VoiceResponse = require('twilio').twiml.VoiceResponse;

app.post('/voice', (req, res) => {
  const twiml = new VoiceResponse();
  twiml.say('Hello! Thank you for calling.');
  twiml.play('https://example.com/welcome.mp3');

  // Gather user input
  const gather = twiml.gather({
    numDigits: 1,
    action: '/gather'
  });
  gather.say('Press 1 for sales, 2 for support.');

  res.type('text/xml').send(twiml.toString());
});
```

### 3. WhatsApp Messaging

**Send WhatsApp Message:**
```python
message = client.messages.create(
    from_='whatsapp:+14155238886',  # Twilio sandbox number
    body='Hello from WhatsApp!',
    to='whatsapp:+15559876543'
)
```

**WhatsApp Template Message (approved templates only):**
```javascript
const message = await client.messages.create({
  from: 'whatsapp:+14155238886',
  contentSid: 'HXb5a6e1d5cf90e031b3c87934b78a571a',  // Approved template
  contentVariables: JSON.stringify({
    1: 'John Doe',
    2: '123456'
  }),
  to: 'whatsapp:+15559876543'
});
```

### 4. Email (SendGrid)

**Send Email via SendGrid:**
```javascript
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const msg = {
  to: 'recipient@example.com',
  from: 'sender@example.com',
  subject: 'Hello from SendGrid',
  text: 'Plain text content',
  html: '<strong>HTML content</strong>',
};

await sgMail.send(msg);
```

### 5. Phone Number Verification (Verify API)

**Start Verification:**
```javascript
const verification = await client.verify.v2
  .services('VAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
  .verifications
  .create({ to: '+15559876543', channel: 'sms' });
```

**Check Verification Code:**
```javascript
const verification_check = await client.verify.v2
  .services('VAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
  .verificationChecks
  .create({ to: '+15559876543', code: '123456' });

console.log(verification_check.status);  // 'approved' or 'pending'
```

### 6. Video (Twilio Video)

**Create Video Room:**
```javascript
const room = await client.video.v1.rooms.create({
  uniqueName: 'my-video-room',
  type: 'group',  // 'group' or 'peer-to-peer'
  recordParticipantsOnConnect: false
});
```

**Generate Access Token:**
```javascript
const AccessToken = require('twilio').jwt.AccessToken;
const VideoGrant = AccessToken.VideoGrant;

const token = new AccessToken(
  accountSid,
  apiKeySid,
  apiKeySecret,
  { identity: 'user@example.com' }
);

const videoGrant = new VideoGrant({
  room: 'my-video-room'
});
token.addGrant(videoGrant);

const jwt = token.toJwt();
```

## Implementation Patterns

### Pattern 1: Error Handling

Always handle Twilio errors properly:

```javascript
try {
  const message = await client.messages.create({
    body: 'Test message',
    from: '+15551234567',
    to: '+15559876543'
  });
} catch (error) {
  if (error.code === 21211) {
    console.error('Invalid phone number');
  } else if (error.code === 21408) {
    console.error('Permission to send SMS not enabled');
  } else {
    console.error('Error:', error.message);
  }
}
```

### Pattern 2: Webhook Validation

**Validate webhook requests to ensure they're from Twilio:**

```javascript
const twilio = require('twilio');

app.post('/sms', (req, res) => {
  const authToken = process.env.TWILIO_AUTH_TOKEN;
  const twilioSignature = req.headers['x-twilio-signature'];
  const url = 'https://yourdomain.com/sms';

  const isValid = twilio.validateRequest(
    authToken,
    twilioSignature,
    url,
    req.body
  );

  if (!isValid) {
    return res.status(403).send('Forbidden');
  }

  // Process webhook...
});
```

### Pattern 3: Retry Logic for Failed Messages

```python
import time
from twilio.base.exceptions import TwilioRestException

def send_sms_with_retry(client, to, from_, body, max_retries=3):
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                body=body,
                from_=from_,
                to=to
            )
            return message
        except TwilioRestException as e:
            if e.code in [20429, 20500, 20503]:  # Rate limit or server errors
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
            raise
```

### Pattern 4: Message Status Tracking

```javascript
// Set status callback URL when sending
const message = await client.messages.create({
  body: 'Track me!',
  from: '+15551234567',
  to: '+15559876543',
  statusCallback: 'https://yourdomain.com/message-status'
});

// Handle status webhook
app.post('/message-status', (req, res) => {
  const messageSid = req.body.MessageSid;
  const status = req.body.MessageStatus;

  console.log(`Message ${messageSid} status: ${status}`);
  // Status can be: queued, sent, delivered, failed, undelivered

  res.sendStatus(200);
});
```

## Best Practices

### Security

1. **Never expose credentials:**
   - Use environment variables for Account SID and Auth Token
   - Rotate auth tokens regularly
   - Use API keys for specific applications instead of main auth token

2. **Validate all webhooks:**
   - Always verify `X-Twilio-Signature` header
   - Use HTTPS for all webhook URLs
   - Implement IP allowlisting if possible

3. **Rate limiting:**
   - Implement backoff for 429 (Too Many Requests) errors
   - Queue messages during high-volume sends
   - Use message pools for different priorities

### Phone Numbers

1. **E.164 format:**
   - Always use international format: `+15551234567`
   - Validate numbers before sending
   - Handle local number formatting for display

2. **Sender ID compliance:**
   - Register business profile for better deliverability
   - Use verified sender IDs
   - Follow A2P 10DLC registration for US messaging

### Cost Optimization

1. **Message length:**
   - SMS messages over 160 characters count as multiple segments
   - Use SMS character counter to optimize length
   - Consider using WhatsApp for longer messages (cheaper per message)

2. **Phone number usage:**
   - Use toll-free numbers for high-volume messaging
   - Port existing numbers when possible
   - Release unused numbers to avoid monthly fees

3. **Batch operations:**
   - Use Messaging Services for pooling
   - Implement message queuing for bulk sends
   - Schedule non-urgent messages during off-peak hours

### Reliability

1. **Idempotency:**
   - Use idempotency keys for critical operations
   - Store message SIDs to prevent duplicates
   - Implement deduplication logic

2. **Error handling:**
   - Log all errors with context
   - Implement retry logic with exponential backoff
   - Monitor error rates and set up alerts

3. **Testing:**
   - Use Twilio test credentials for development
   - Test webhook handlers with ngrok or similar tools
   - Verify international number formats

## Anti-Patterns

❌ **Hardcoding credentials:**
```javascript
// DON'T DO THIS
const client = twilio('AC123...', 'secret123...');
```

✅ **Use environment variables:**
```javascript
const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);
```

❌ **Not validating webhooks:**
```javascript
// INSECURE
app.post('/sms', (req, res) => {
  processMessage(req.body);  // Anyone can POST here
});
```

✅ **Always validate:**
```javascript
app.post('/sms', (req, res) => {
  if (!twilio.validateRequest(...)) {
    return res.status(403).send('Forbidden');
  }
  processMessage(req.body);
});
```

❌ **Synchronous bulk sending:**
```javascript
// SLOW AND ERROR-PRONE
for (const recipient of recipients) {
  await client.messages.create({...});
}
```

✅ **Use async batch processing:**
```javascript
const promises = recipients.map(recipient =>
  client.messages.create({...})
    .catch(err => ({ error: err, recipient }))
);
const results = await Promise.allSettled(promises);
```

❌ **Not handling message status:**
```javascript
// No way to know if message was delivered
await client.messages.create({ body: 'Important!', ... });
```

✅ **Track delivery status:**
```javascript
const message = await client.messages.create({
  body: 'Important!',
  statusCallback: 'https://yourdomain.com/status',
  ...
});
// Store message.sid and track status via webhook
```

## Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 20003 | Authentication error | Check Account SID and Auth Token |
| 21211 | Invalid 'To' phone number | Verify number format (E.164) |
| 21408 | Permission denied | Enable SMS capability for number |
| 21610 | Unsubscribed recipient | Respect opt-out, remove from list |
| 21614 | Invalid 'From' number | Verify ownership of sender number |
| 30003 | Unreachable destination | Number not in service or blocked |
| 30005 | Unknown destination | Invalid phone number |
| 30006 | Landline or unreachable | Can't send SMS to landlines |

## Testing and Development

### Use Twilio Test Credentials

For development without charges:
```
Account SID: ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Auth Token: your_test_auth_token
```

Magic test phone numbers (won't actually send):
- `+15005550006` - Valid number (will succeed)
- `+15005550001` - Invalid number (will fail)
- `+15005550007` - Message blocked
- `+15005550009` - Message queued

### Local Webhook Testing

```bash
# Install ngrok
npm install -g ngrok

# Start your local server
node app.js

# Expose it publicly
ngrok http 3000

# Use the ngrok URL in Twilio console
# https://abc123.ngrok.io/sms
```

## Reference Resources

For deep-dive documentation, see:
- [Official Twilio Documentation](https://www.twilio.com/docs)
- [Twilio Helper Libraries](https://www.twilio.com/docs/libraries)
- [TwiML Reference](https://www.twilio.com/docs/voice/twiml)
- [Twilio Status Codes](https://www.twilio.com/docs/api/errors)
- [SMS Best Practices](https://www.twilio.com/docs/sms/best-practices)
- [WhatsApp Business API](https://www.twilio.com/docs/whatsapp)
- [Verify API Documentation](https://www.twilio.com/docs/verify)
- [Video API Documentation](https://www.twilio.com/docs/video)

## Quick Decision Tree

```
Need to send messages?
├─ SMS/Text → Use Messaging API
├─ Rich media/International → Consider WhatsApp
├─ Verification codes → Use Verify API
└─ Email → Use SendGrid (Twilio)

Need voice features?
├─ Outbound calls → Use Voice API
├─ Inbound IVR → Use TwiML with Gather
├─ Conference calls → Use Conference API
└─ Recording → Use Recording API

Need video/calling?
├─ 1-to-1 video → Use peer-to-peer rooms
├─ Group video → Use group rooms
└─ WebRTC browser → Use Twilio Video JS SDK

Need authentication?
├─ Phone verification → Use Verify API
└─ Two-factor auth → Use Authy (Twilio)
```

## Implementation Checklist

- [ ] Install Twilio SDK for your language
- [ ] Set up environment variables for credentials
- [ ] Obtain Twilio phone number (if needed)
- [ ] Configure webhook URLs in Twilio console
- [ ] Implement webhook signature validation
- [ ] Add error handling and retry logic
- [ ] Set up logging and monitoring
- [ ] Test with Twilio test credentials
- [ ] Verify compliance requirements (A2P 10DLC for US)
- [ ] Implement status tracking for critical messages
- [ ] Set up billing alerts
- [ ] Document API usage for team members

---

**Version:** 1.0
**Last Updated:** 2025
**Twilio API Version:** 2010-04-01 (stable)
