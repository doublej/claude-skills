# Twilio Real-World Implementation Examples

## Table of Contents
- [Two-Factor Authentication (2FA)](#two-factor-authentication-2fa)
- [Appointment Reminders](#appointment-reminders)
- [Customer Support Bot](#customer-support-bot)
- [Order Status Notifications](#order-status-notifications)
- [Click-to-Call Widget](#click-to-call-widget)
- [SMS Survey System](#sms-survey-system)
- [Emergency Alert System](#emergency-alert-system)
- [Video Consultation Platform](#video-consultation-platform)

---

## Two-Factor Authentication (2FA)

Complete implementation using Twilio Verify API.

### Backend Implementation (Node.js/Express)

```javascript
const express = require('express');
const twilio = require('twilio');

const app = express();
app.use(express.json());

const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

const VERIFY_SERVICE_SID = process.env.TWILIO_VERIFY_SERVICE_SID;

// Step 1: Send verification code
app.post('/api/auth/send-code', async (req, res) => {
  const { phoneNumber } = req.body;

  try {
    const verification = await client.verify.v2
      .services(VERIFY_SERVICE_SID)
      .verifications
      .create({
        to: phoneNumber,
        channel: 'sms'  // or 'call', 'email', 'whatsapp'
      });

    res.json({
      success: true,
      status: verification.status,
      to: verification.to
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      error: error.message
    });
  }
});

// Step 2: Verify code
app.post('/api/auth/verify-code', async (req, res) => {
  const { phoneNumber, code } = req.body;

  try {
    const verificationCheck = await client.verify.v2
      .services(VERIFY_SERVICE_SID)
      .verificationChecks
      .create({
        to: phoneNumber,
        code: code
      });

    if (verificationCheck.status === 'approved') {
      // Generate JWT or session token
      const token = generateAuthToken(phoneNumber);

      res.json({
        success: true,
        verified: true,
        token: token
      });
    } else {
      res.status(400).json({
        success: false,
        verified: false,
        message: 'Invalid code'
      });
    }
  } catch (error) {
    res.status(400).json({
      success: false,
      error: error.message
    });
  }
});

function generateAuthToken(phoneNumber) {
  // Implement JWT generation
  const jwt = require('jsonwebtoken');
  return jwt.sign({ phone: phoneNumber }, process.env.JWT_SECRET, {
    expiresIn: '24h'
  });
}

app.listen(3000, () => console.log('Server running on port 3000'));
```

### Frontend Implementation (React)

```jsx
import React, { useState } from 'react';
import axios from 'axios';

function TwoFactorAuth() {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [code, setCode] = useState('');
  const [step, setStep] = useState('phone'); // 'phone' or 'verify'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const sendCode = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/api/auth/send-code', {
        phoneNumber
      });

      if (response.data.success) {
        setStep('verify');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send code');
    } finally {
      setLoading(false);
    }
  };

  const verifyCode = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/api/auth/verify-code', {
        phoneNumber,
        code
      });

      if (response.data.verified) {
        // Store token and redirect
        localStorage.setItem('authToken', response.data.token);
        window.location.href = '/dashboard';
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Invalid code');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      {step === 'phone' ? (
        <form onSubmit={sendCode}>
          <h2>Enter Your Phone Number</h2>
          <input
            type="tel"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            placeholder="+1234567890"
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Sending...' : 'Send Code'}
          </button>
        </form>
      ) : (
        <form onSubmit={verifyCode}>
          <h2>Enter Verification Code</h2>
          <p>We sent a code to {phoneNumber}</p>
          <input
            type="text"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="000000"
            maxLength="6"
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Verifying...' : 'Verify'}
          </button>
          <button type="button" onClick={() => setStep('phone')}>
            Change Number
          </button>
        </form>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default TwoFactorAuth;
```

---

## Appointment Reminders

Automated reminder system with scheduling.

### Database Schema

```sql
CREATE TABLE appointments (
  id SERIAL PRIMARY KEY,
  customer_name VARCHAR(255),
  customer_phone VARCHAR(20),
  appointment_time TIMESTAMP,
  service_type VARCHAR(100),
  reminder_sent BOOLEAN DEFAULT FALSE,
  reminder_sid VARCHAR(50)
);
```

### Reminder Service (Node.js)

```javascript
const cron = require('node-cron');
const twilio = require('twilio');
const { Pool } = require('pg');

const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

const db = new Pool({
  connectionString: process.env.DATABASE_URL
});

// Run every hour
cron.schedule('0 * * * *', async () => {
  await sendReminders();
});

async function sendReminders() {
  // Get appointments in next 24 hours that haven't been reminded
  const tomorrow = new Date();
  tomorrow.setHours(tomorrow.getHours() + 24);

  const result = await db.query(
    `SELECT * FROM appointments
     WHERE appointment_time <= $1
     AND appointment_time > NOW()
     AND reminder_sent = FALSE`,
    [tomorrow]
  );

  for (const appointment of result.rows) {
    await sendReminderSMS(appointment);
  }
}

async function sendReminderSMS(appointment) {
  const appointmentDate = new Date(appointment.appointment_time);
  const formattedDate = appointmentDate.toLocaleDateString();
  const formattedTime = appointmentDate.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  });

  const messageBody = `Hi ${appointment.customer_name}! This is a reminder about your ${appointment.service_type} appointment tomorrow at ${formattedTime} on ${formattedDate}. Reply YES to confirm or CANCEL to reschedule.`;

  try {
    const message = await client.messages.create({
      body: messageBody,
      from: process.env.TWILIO_PHONE_NUMBER,
      to: appointment.customer_phone,
      statusCallback: `${process.env.APP_URL}/sms-status/${appointment.id}`
    });

    // Update database
    await db.query(
      `UPDATE appointments
       SET reminder_sent = TRUE, reminder_sid = $1
       WHERE id = $2`,
      [message.sid, appointment.id]
    );

    console.log(`Reminder sent to ${appointment.customer_name}: ${message.sid}`);
  } catch (error) {
    console.error(`Failed to send reminder to ${appointment.customer_name}:`, error);
  }
}

// Handle responses
const express = require('express');
const app = express();

app.use(express.urlencoded({ extended: false }));

app.post('/sms-reply', async (req, res) => {
  const MessagingResponse = twilio.twiml.MessagingResponse;
  const twiml = new MessagingResponse();

  const incomingMsg = req.body.Body.toUpperCase().trim();
  const fromNumber = req.body.From;

  // Find appointment by phone number
  const result = await db.query(
    'SELECT * FROM appointments WHERE customer_phone = $1 AND appointment_time > NOW() ORDER BY appointment_time LIMIT 1',
    [fromNumber]
  );

  if (result.rows.length === 0) {
    twiml.message('No upcoming appointments found.');
  } else if (incomingMsg === 'YES' || incomingMsg === 'CONFIRM') {
    await db.query(
      'UPDATE appointments SET confirmed = TRUE WHERE id = $1',
      [result.rows[0].id]
    );
    twiml.message('Great! Your appointment is confirmed. See you then!');
  } else if (incomingMsg === 'CANCEL') {
    twiml.message('To reschedule, please call us at (555) 123-4567.');
  } else {
    twiml.message('Reply YES to confirm or CANCEL to reschedule your appointment.');
  }

  res.type('text/xml').send(twiml.toString());
});

app.listen(3000);
```

---

## Customer Support Bot

Interactive SMS chatbot with keyword routing.

```javascript
const express = require('express');
const twilio = require('twilio');
const Redis = require('ioredis');

const app = express();
app.use(express.urlencoded({ extended: false }));

const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

const redis = new Redis(process.env.REDIS_URL);

// Session management
async function getSession(phoneNumber) {
  const session = await redis.get(`session:${phoneNumber}`);
  return session ? JSON.parse(session) : { step: 'initial' };
}

async function setSession(phoneNumber, data) {
  await redis.setex(
    `session:${phoneNumber}`,
    1800,  // 30 minutes TTL
    JSON.stringify(data)
  );
}

// Main handler
app.post('/sms-bot', async (req, res) => {
  const MessagingResponse = twilio.twiml.MessagingResponse;
  const twiml = new MessagingResponse();

  const incomingMsg = req.body.Body.trim().toLowerCase();
  const fromNumber = req.body.From;

  const session = await getSession(fromNumber);

  let response = '';

  switch (session.step) {
    case 'initial':
      response = handleInitial(incomingMsg, session);
      break;
    case 'order_tracking':
      response = await handleOrderTracking(incomingMsg, session);
      break;
    case 'technical_support':
      response = handleTechnicalSupport(incomingMsg, session);
      break;
    case 'billing':
      response = handleBilling(incomingMsg, session);
      break;
    default:
      response = 'Something went wrong. Type MENU to start over.';
      session.step = 'initial';
  }

  await setSession(fromNumber, session);

  twiml.message(response);
  res.type('text/xml').send(twiml.toString());
});

function handleInitial(msg, session) {
  if (msg === 'menu' || msg === 'start') {
    return `Welcome to Customer Support! 🎉

Reply with:
1️⃣ TRACK - Track your order
2️⃣ TECH - Technical support
3️⃣ BILL - Billing questions
4️⃣ HUMAN - Talk to a person`;
  }

  if (msg === 'track' || msg === '1') {
    session.step = 'order_tracking';
    return 'Please enter your order number:';
  }

  if (msg === 'tech' || msg === '2') {
    session.step = 'technical_support';
    return `What type of issue are you experiencing?
1. Login problems
2. App crashes
3. Other`;
  }

  if (msg === 'bill' || msg === '3') {
    session.step = 'billing';
    return 'I can help with billing. Reply with your account email:';
  }

  if (msg === 'human' || msg === '4') {
    // Create TaskRouter task or notify agents
    createSupportTicket(session.phoneNumber);
    return 'Connecting you with an agent. Someone will call you shortly!';
  }

  return 'Hi! Reply MENU to see options.';
}

async function handleOrderTracking(orderNumber, session) {
  // Query order database
  const order = await lookupOrder(orderNumber);

  if (order) {
    session.step = 'initial';
    return `Order #${orderNumber}:
Status: ${order.status}
Estimated delivery: ${order.estimated_delivery}

Reply MENU for more options.`;
  } else {
    return 'Order not found. Please check the number and try again, or reply MENU.';
  }
}

function handleTechnicalSupport(msg, session) {
  if (msg === '1') {
    session.step = 'initial';
    return `For login issues:
1. Check your email/password
2. Try "Forgot Password"
3. Clear browser cache

Visit: https://help.example.com/login

Reply MENU for more help.`;
  }

  if (msg === '2') {
    session.step = 'initial';
    return `For app crashes:
1. Update to latest version
2. Restart your device
3. Reinstall the app

Still having issues? Reply HUMAN to speak with someone.`;
  }

  session.step = 'initial';
  return 'Please describe your issue briefly, and reply HUMAN if you need to talk to support.';
}

function handleBilling(email, session) {
  if (isValidEmail(email)) {
    // Look up account
    session.step = 'initial';
    return `Account found for ${email}.
Current balance: $29.99
Next billing date: Jan 15

Reply MENU for more options.`;
  }

  return 'Please enter a valid email address or reply MENU.';
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

async function lookupOrder(orderNumber) {
  // Mock implementation - replace with real database query
  return {
    status: 'Shipped',
    estimated_delivery: 'Jan 12, 2025'
  };
}

function createSupportTicket(phoneNumber) {
  // Create TaskRouter task or CRM ticket
  console.log(`Creating support ticket for ${phoneNumber}`);
}

app.listen(3000);
```

---

## Order Status Notifications

Real-time order updates via SMS with WhatsApp fallback.

```javascript
const twilio = require('twilio');
const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

class OrderNotificationService {
  constructor() {
    this.messagingServiceSid = process.env.TWILIO_MESSAGING_SERVICE_SID;
  }

  async sendOrderConfirmation(order, customer) {
    const message = `🎉 Order Confirmed!

Order #${order.id}
Total: $${order.total}

We'll notify you when it ships!

Track: ${order.trackingUrl}`;

    return this.sendNotification(customer, message, 'order_confirmation');
  }

  async sendShippingUpdate(order, customer, trackingNumber) {
    const message = `📦 Your order has shipped!

Order #${order.id}
Tracking: ${trackingNumber}
Estimated delivery: ${order.estimatedDelivery}

Track: ${order.trackingUrl}`;

    return this.sendNotification(customer, message, 'shipping_update');
  }

  async sendDeliveryNotification(order, customer) {
    const message = `✅ Delivered!

Order #${order.id} has been delivered.

Enjoy your purchase! Leave a review: ${order.reviewUrl}`;

    return this.sendNotification(customer, message, 'delivery');
  }

  async sendNotification(customer, messageBody, notificationType) {
    const channels = this.determineChannels(customer);

    for (const channel of channels) {
      try {
        const message = await this.sendViaChannel(
          channel,
          customer,
          messageBody
        );

        // Log success
        await this.logNotification({
          customerId: customer.id,
          channel: channel.type,
          messageSid: message.sid,
          notificationType,
          status: 'sent'
        });

        return message;  // Success, stop trying other channels
      } catch (error) {
        console.error(`Failed to send via ${channel.type}:`, error);
        // Try next channel
      }
    }

    throw new Error('All notification channels failed');
  }

  determineChannels(customer) {
    const channels = [];

    // Try WhatsApp first if opted in
    if (customer.whatsappOptIn && customer.phone) {
      channels.push({
        type: 'whatsapp',
        address: `whatsapp:${customer.phone}`
      });
    }

    // Fallback to SMS
    if (customer.phone) {
      channels.push({
        type: 'sms',
        address: customer.phone
      });
    }

    // Fallback to email (via SendGrid)
    if (customer.email) {
      channels.push({
        type: 'email',
        address: customer.email
      });
    }

    return channels;
  }

  async sendViaChannel(channel, customer, messageBody) {
    if (channel.type === 'whatsapp' || channel.type === 'sms') {
      return client.messages.create({
        body: messageBody,
        messagingServiceSid: this.messagingServiceSid,
        to: channel.address,
        statusCallback: `${process.env.APP_URL}/message-status`
      });
    }

    if (channel.type === 'email') {
      // Send via SendGrid
      const sgMail = require('@sendgrid/mail');
      sgMail.setApiKey(process.env.SENDGRID_API_KEY);

      return sgMail.send({
        to: channel.address,
        from: process.env.FROM_EMAIL,
        subject: 'Order Update',
        text: messageBody
      });
    }
  }

  async logNotification(data) {
    // Save to database
    const db = require('./database');
    await db.query(
      'INSERT INTO notifications (customer_id, channel, message_sid, type, status) VALUES ($1, $2, $3, $4, $5)',
      [data.customerId, data.channel, data.messageSid, data.notificationType, data.status]
    );
  }
}

// Usage
const notificationService = new OrderNotificationService();

async function handleOrderShipped(orderId) {
  const order = await getOrder(orderId);
  const customer = await getCustomer(order.customerId);

  await notificationService.sendShippingUpdate(
    order,
    customer,
    order.trackingNumber
  );
}

module.exports = OrderNotificationService;
```

---

## Click-to-Call Widget

Web widget for instant voice calls.

### Frontend Widget

```html
<!-- click-to-call-widget.html -->
<!DOCTYPE html>
<html>
<head>
  <script src="https://sdk.twilio.com/js/client/releases/1.14.0/twilio.min.js"></script>
  <style>
    .call-widget {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 300px;
      background: white;
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      padding: 20px;
    }
    .call-button {
      width: 100%;
      padding: 15px;
      background: #00A8E1;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 16px;
    }
    .call-button:hover {
      background: #0080B0;
    }
    .call-button:disabled {
      background: #ccc;
      cursor: not-allowed;
    }
  </style>
</head>
<body>
  <div class="call-widget">
    <h3>Need Help?</h3>
    <p>Talk to a support agent now</p>
    <button id="callButton" class="call-button">Call Now</button>
    <p id="status"></p>
  </div>

  <script>
    let device;
    let currentCall;

    // Initialize Twilio Device
    async function initDevice() {
      const response = await fetch('/api/token');
      const data = await response.json();

      device = new Twilio.Device(data.token, {
        codecPreferences: ['opus', 'pcmu'],
        fakeLocalDTMF: true,
        enableRingingState: true
      });

      device.on('ready', () => {
        console.log('Twilio Device Ready');
        updateStatus('Ready to call');
      });

      device.on('error', (error) => {
        console.error('Device error:', error);
        updateStatus('Error: ' + error.message);
      });

      device.on('connect', () => {
        updateStatus('Connected - Call in progress');
        document.getElementById('callButton').textContent = 'Hang Up';
      });

      device.on('disconnect', () => {
        updateStatus('Call ended');
        document.getElementById('callButton').textContent = 'Call Again';
        currentCall = null;
      });
    }

    // Make or hang up call
    document.getElementById('callButton').addEventListener('click', async () => {
      if (currentCall) {
        currentCall.disconnect();
      } else {
        makeCall();
      }
    });

    async function makeCall() {
      updateStatus('Connecting...');

      const params = {
        To: '+15551234567'  // Support number
      };

      currentCall = await device.connect({ params });
    }

    function updateStatus(message) {
      document.getElementById('status').textContent = message;
    }

    // Initialize on load
    initDevice();
  </script>
</body>
</html>
```

### Backend (Token Generation)

```javascript
const express = require('express');
const twilio = require('twilio');

const app = express();

const AccessToken = twilio.jwt.AccessToken;
const VoiceGrant = AccessToken.VoiceGrant;

app.get('/api/token', (req, res) => {
  const identity = `user_${Date.now()}`;

  const token = new AccessToken(
    process.env.TWILIO_ACCOUNT_SID,
    process.env.TWILIO_API_KEY,
    process.env.TWILIO_API_SECRET,
    { identity }
  );

  const voiceGrant = new VoiceGrant({
    outgoingApplicationSid: process.env.TWILIO_TWIML_APP_SID,
    incomingAllow: true
  });

  token.addGrant(voiceGrant);

  res.json({
    identity: identity,
    token: token.toJwt()
  });
});

// Handle outgoing calls
const VoiceResponse = twilio.twiml.VoiceResponse;

app.post('/voice', (req, res) => {
  const twiml = new VoiceResponse();

  const dial = twiml.dial({
    callerId: process.env.TWILIO_PHONE_NUMBER
  });

  // Route to support queue or agent
  dial.number('+15551234567');

  res.type('text/xml').send(twiml.toString());
});

app.listen(3000);
```

---

These real-world examples demonstrate production-ready implementations of common Twilio use cases. Each example includes error handling, best practices, and can be adapted to your specific needs.
