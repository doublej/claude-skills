# Twilio Advanced Features Reference

## Table of Contents
- [Programmable Messaging Services](#programmable-messaging-services)
- [Advanced Voice Features](#advanced-voice-features)
- [Twilio Functions (Serverless)](#twilio-functions-serverless)
- [Studio (Visual Workflow Builder)](#studio-visual-workflow-builder)
- [Sync (Real-time State)](#sync-real-time-state)
- [TaskRouter (Contact Center)](#taskrouter-contact-center)
- [Flex (Contact Center Platform)](#flex-contact-center-platform)
- [Lookup API](#lookup-api)
- [Conversations API](#conversations-api)

---

## Programmable Messaging Services

Messaging Services provide message pooling, intelligent routing, and advanced features.

### Create a Messaging Service

```javascript
const service = await client.messaging.v1.services.create({
  friendlyName: 'My Messaging Service',
  inboundRequestUrl: 'https://example.com/inbound',
  fallbackUrl: 'https://example.com/fallback',
  statusCallback: 'https://example.com/status'
});

console.log(service.sid);  // MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Add Phone Numbers to Service

```javascript
await client.messaging.v1
  .services(serviceSid)
  .phoneNumbers
  .create({ phoneNumberSid: 'PNxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' });
```

### Send from Messaging Service

```javascript
const message = await client.messages.create({
  body: 'Sent from messaging service',
  messagingServiceSid: 'MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
  to: '+15559876543'
});
// Twilio automatically selects best phone number from pool
```

### Enable Copilot (Smart Sender Selection)

```javascript
const service = await client.messaging.v1.services(serviceSid).update({
  useInboundWebhookOnNumber: false,  // Use service-level webhook
  stickySender: true,  // Maintain sender-recipient relationship
  smartEncoding: true  // Automatic character encoding
});
```

### Advanced Features

**Geo-matching:**
```javascript
// Automatically select sender number closest to recipient
const service = await client.messaging.v1.services(serviceSid).update({
  useInboundWebhookOnNumber: false,
  areaCodeGeomatch: true
});
```

**Link Shortening:**
```javascript
const shortenedUrl = await client.messaging.v1
  .services(serviceSid)
  .shortCodes
  .create({
    shortCodeSid: 'SCxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  });
```

---

## Advanced Voice Features

### Conference Calls

**Start Conference:**
```javascript
const VoiceResponse = require('twilio').twiml.VoiceResponse;

app.post('/conference', (req, res) => {
  const twiml = new VoiceResponse();
  const dial = twiml.dial();

  dial.conference({
    startConferenceOnEnter: true,
    endConferenceOnExit: true,
    statusCallback: 'https://example.com/conference-status',
    statusCallbackEvent: ['start', 'end', 'join', 'leave']
  }, 'MyConferenceRoom');

  res.type('text/xml').send(twiml.toString());
});
```

**Conference Moderation:**
```javascript
// Mute participant
await client.conferences(conferenceSid)
  .participants(callSid)
  .update({ muted: true });

// Remove participant
await client.conferences(conferenceSid)
  .participants(callSid)
  .remove();

// Update conference
await client.conferences(conferenceSid)
  .update({ status: 'completed' });  // End conference
```

### Call Recording

**Record Calls:**
```javascript
const VoiceResponse = require('twilio').twiml.VoiceResponse;

const twiml = new VoiceResponse();
twiml.say('This call is being recorded.');
twiml.record({
  maxLength: 3600,  // 1 hour
  recordingStatusCallback: 'https://example.com/recording-complete',
  transcribe: true,
  transcribeCallback: 'https://example.com/transcription'
});

res.type('text/xml').send(twiml.toString());
```

**Access Recordings:**
```javascript
const recordings = await client.recordings.list({ limit: 20 });

recordings.forEach(r => {
  console.log(r.sid);
  const audioUrl = `https://api.twilio.com${r.uri.replace('.json', '.mp3')}`;
});

// Delete recording (for privacy/compliance)
await client.recordings('RExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx').remove();
```

### Speech Recognition (Gather with Speech)

```javascript
const twiml = new VoiceResponse();
const gather = twiml.gather({
  input: ['speech', 'dtmf'],
  timeout: 3,
  numDigits: 1,
  action: '/process-speech',
  language: 'en-US',
  hints: 'sales, support, billing',  // Improve recognition
  speechTimeout: 'auto'
});

gather.say('Say sales for sales, or press 1.');

res.type('text/xml').send(twiml.toString());
```

**Process Speech Input:**
```javascript
app.post('/process-speech', (req, res) => {
  const speechResult = req.body.SpeechResult;
  const confidence = req.body.Confidence;

  const twiml = new VoiceResponse();

  if (parseFloat(confidence) > 0.7) {
    twiml.say(`You said: ${speechResult}`);
  } else {
    twiml.say('Sorry, I didn\'t catch that.');
  }

  res.type('text/xml').send(twiml.toString());
});
```

### SIP Trunking

**Make SIP Call:**
```javascript
const call = await client.calls.create({
  url: 'http://demo.twilio.com/docs/voice.xml',
  to: 'sip:alice@example.com',
  from: '+15551234567'
});
```

---

## Twilio Functions (Serverless)

Deploy Node.js functions without managing servers.

### Create Function via API

```javascript
const service = await client.serverless.v1.services.create({
  uniqueName: 'my-service',
  friendlyName: 'My Twilio Service'
});

const environment = await client.serverless.v1
  .services(service.sid)
  .environments
  .create({ uniqueName: 'production' });
```

### Example Function Code

```javascript
// This runs on Twilio's infrastructure
exports.handler = function(context, event, callback) {
  // Access environment variables
  const accountSid = context.ACCOUNT_SID;
  const authToken = context.AUTH_TOKEN;

  // Access event parameters
  const phoneNumber = event.PhoneNumber;

  // Use Twilio client
  const client = context.getTwilioClient();

  client.messages
    .create({
      body: 'Hello from Twilio Function',
      to: phoneNumber,
      from: context.TWILIO_PHONE_NUMBER
    })
    .then(message => {
      callback(null, { success: true, messageSid: message.sid });
    })
    .catch(error => {
      callback(error);
    });
};
```

### Deploy with Twilio CLI

```bash
# Install Twilio CLI
npm install -g twilio-cli

# Login
twilio login

# Create new serverless project
twilio serverless:init my-project

# Deploy
cd my-project
twilio serverless:deploy
```

---

## Studio (Visual Workflow Builder)

Create complex communication flows visually.

### Trigger Studio Flow via API

```javascript
const execution = await client.studio.v2
  .flows('FWxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
  .executions
  .create({
    to: '+15559876543',
    from: '+15551234567',
    parameters: JSON.stringify({
      name: 'John Doe',
      orderId: '12345'
    })
  });
```

### Access Studio Flow Context

```javascript
// In a Twilio Function called from Studio
exports.handler = function(context, event, callback) {
  // Access flow variables
  const flowSid = event.flow.sid;
  const flowName = event.flow.friendly_name;
  const customerName = event.parameters.name;

  // Return data to Studio
  callback(null, {
    status: 'success',
    next_step: 'send_confirmation'
  });
};
```

---

## Sync (Real-time State)

Synchronized state across devices and clients.

### Create Sync Service

```javascript
const service = await client.sync.v1.services.create({
  friendlyName: 'My Sync Service'
});
```

### Sync Documents (Key-Value Store)

```javascript
// Create/Update document
const document = await client.sync.v1
  .services(serviceSid)
  .documents
  .create({
    uniqueName: 'user_preferences',
    data: { theme: 'dark', language: 'en' }
  });

// Read document
const doc = await client.sync.v1
  .services(serviceSid)
  .documents('user_preferences')
  .fetch();

console.log(doc.data);
```

### Sync Lists (Ordered Collections)

```javascript
// Create list
const list = await client.sync.v1
  .services(serviceSid)
  .syncLists
  .create({ uniqueName: 'todo_items' });

// Add items
await client.sync.v1
  .services(serviceSid)
  .syncLists('todo_items')
  .syncListItems
  .create({
    data: { task: 'Buy groceries', completed: false }
  });

// List items
const items = await client.sync.v1
  .services(serviceSid)
  .syncLists('todo_items')
  .syncListItems
  .list({ limit: 20 });
```

### Sync Maps (Key-Value Collections)

```javascript
const map = await client.sync.v1
  .services(serviceSid)
  .syncMaps
  .create({ uniqueName: 'user_sessions' });

// Add map item
await client.sync.v1
  .services(serviceSid)
  .syncMaps('user_sessions')
  .syncMapItems
  .create({
    key: 'session_123',
    data: { userId: 'user_456', loginTime: new Date() }
  });
```

---

## TaskRouter (Contact Center)

Route tasks to available workers.

### Create Workspace

```javascript
const workspace = await client.taskrouter.v1.workspaces.create({
  friendlyName: 'Customer Support',
  eventCallbackUrl: 'https://example.com/events'
});
```

### Create Workers

```javascript
const worker = await client.taskrouter.v1
  .workspaces(workspaceSid)
  .workers
  .create({
    friendlyName: 'Alice',
    attributes: JSON.stringify({
      skills: ['english', 'sales'],
      contact_uri: '+15551234567'
    })
  });
```

### Create Task Queues

```javascript
const queue = await client.taskrouter.v1
  .workspaces(workspaceSid)
  .taskQueues
  .create({
    friendlyName: 'Sales Queue',
    targetWorkers: 'skills HAS "sales"',
    reservationActivitySid: 'WAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  });
```

### Create Tasks

```javascript
const task = await client.taskrouter.v1
  .workspaces(workspaceSid)
  .tasks
  .create({
    attributes: JSON.stringify({
      from: '+15559876543',
      type: 'sales_inquiry',
      priority: 1
    }),
    workflowSid: 'WWxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  });
```

---

## Flex (Contact Center Platform)

Pre-built contact center solution.

### Flex WebChat

```javascript
// Initialize Flex WebChat
const manager = Twilio.FlexWebChat.Manager.create({
  accountSid: 'ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
  flexFlowSid: 'FOxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
});

// Start chat
manager.chatClient.getChannelBySid(channelSid).then(channel => {
  channel.sendMessage('Hello from webchat!');
});
```

### Flex Plugins

```javascript
// Custom Flex Plugin
import * as FlexPlugin from '@twilio/flex-plugin';

export default class CustomPlugin extends FlexPlugin {
  constructor() {
    super('CustomPlugin');
  }

  init(flex, manager) {
    // Add custom component
    flex.AgentDesktopView.Panel1.Content.add(
      <CustomComponent key="custom-component" />
    );

    // Listen to events
    manager.workerClient.on('reservationCreated', reservation => {
      console.log('New reservation:', reservation.sid);
    });
  }
}
```

---

## Lookup API

Validate and enrich phone numbers.

### Basic Lookup

```javascript
const phoneNumber = await client.lookups.v2
  .phoneNumbers('+15559876543')
  .fetch({ fields: 'line_type_intelligence' });

console.log(phoneNumber.lineTypeIntelligence);
// { mobile_network_code: "...", type: "mobile", carrier_name: "..." }
```

### Carrier Lookup

```javascript
const phoneNumber = await client.lookups.v2
  .phoneNumbers('+15559876543')
  .fetch({ fields: 'line_type_intelligence,caller_name' });

console.log(phoneNumber.callerName);
// { caller_name: "John Doe", caller_type: "CONSUMER" }
```

### Validation

```javascript
const phoneNumber = await client.lookups.v2
  .phoneNumbers('+15559876543')
  .fetch({ fields: 'validation' });

if (phoneNumber.valid) {
  console.log('Valid number:', phoneNumber.nationalFormat);
} else {
  console.log('Invalid number');
}
```

---

## Conversations API

Multi-channel conversations (SMS, WhatsApp, Chat).

### Create Conversation

```javascript
const conversation = await client.conversations.v1.conversations.create({
  friendlyName: 'Customer Support Chat'
});
```

### Add Participants

```javascript
// Add SMS participant
await client.conversations.v1
  .conversations(conversationSid)
  .participants
  .create({
    messagingBinding: {
      address: '+15559876543',
      proxyAddress: '+15551234567'
    }
  });

// Add WhatsApp participant
await client.conversations.v1
  .conversations(conversationSid)
  .participants
  .create({
    messagingBinding: {
      address: 'whatsapp:+15559876543',
      proxyAddress: 'whatsapp:+14155238886'
    }
  });

// Add chat participant
await client.conversations.v1
  .conversations(conversationSid)
  .participants
  .create({ identity: 'user@example.com' });
```

### Send Messages

```javascript
const message = await client.conversations.v1
  .conversations(conversationSid)
  .messages
  .create({
    author: 'system',
    body: 'Welcome to the conversation!'
  });
```

### Webhooks for Conversations

```javascript
const conversation = await client.conversations.v1.conversations.create({
  friendlyName: 'Support Chat',
  webhookUrl: 'https://example.com/conversation-webhook',
  webhookMethod: 'POST',
  webhookFilters: ['onMessageAdded', 'onParticipantAdded']
});
```

---

## Performance and Optimization

### Bulk Operations

```javascript
// Instead of sequential sends
const promises = phoneNumbers.map(number =>
  client.messages.create({
    body: message,
    from: twilioNumber,
    to: number
  }).catch(err => ({ error: err, number }))
);

const results = await Promise.allSettled(promises);
```

### Connection Pooling

```javascript
const https = require('https');

const agent = new https.Agent({
  keepAlive: true,
  maxSockets: 50
});

const client = twilio(accountSid, authToken, {
  httpClient: agent
});
```

### Caching Lookups

```javascript
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 3600 });

async function lookupWithCache(phoneNumber) {
  const cached = cache.get(phoneNumber);
  if (cached) return cached;

  const result = await client.lookups.v2
    .phoneNumbers(phoneNumber)
    .fetch({ fields: 'line_type_intelligence' });

  cache.set(phoneNumber, result);
  return result;
}
```

---

## Monitoring and Analytics

### Message Insights

```javascript
const messages = await client.messages.list({
  dateSentAfter: new Date('2025-01-01'),
  limit: 100
});

const stats = {
  total: messages.length,
  delivered: messages.filter(m => m.status === 'delivered').length,
  failed: messages.filter(m => m.status === 'failed').length
};
```

### Monitor API

```javascript
const alerts = await client.monitor.v1.alerts.list({ limit: 20 });

alerts.forEach(alert => {
  console.log(`Alert: ${alert.alertText}`);
  console.log(`Level: ${alert.logLevel}`);
});
```

### Usage Records

```javascript
const records = await client.usage.records.list({
  category: 'sms',
  startDate: '2025-01-01',
  endDate: '2025-01-31'
});

const totalUsage = records.reduce((sum, r) => sum + parseFloat(r.usage), 0);
console.log(`Total SMS: ${totalUsage}`);
```

---

This reference covers advanced Twilio features for building sophisticated communication applications. Refer to the main SKILL.md for basic usage patterns.
