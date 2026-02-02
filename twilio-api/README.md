# Twilio API Integration Skill

Expert guidance for implementing Twilio API integrations in your applications.

## What This Skill Provides

This skill gives Claude comprehensive knowledge about:

- **SMS Messaging**: Send and receive text messages programmatically
- **Voice Calls**: Make and handle phone calls with IVR capabilities
- **WhatsApp Business**: Send WhatsApp messages and build chatbots
- **Email (SendGrid)**: Transactional and marketing email delivery
- **Video**: Build video chat and conferencing features
- **Phone Verification**: Implement 2FA and OTP verification
- **Advanced Features**: Messaging Services, TaskRouter, Conversations API, and more

## When Claude Will Use This Skill

Claude will automatically use this skill when you:

- Ask to implement SMS or phone call functionality
- Need to build two-factor authentication
- Want to send notifications via SMS, WhatsApp, or voice
- Need to create IVR (Interactive Voice Response) systems
- Ask about Twilio APIs or integration
- Build customer communication features
- Implement phone number verification

## What's Included

### Core Documentation
- **SKILL.md**: Complete Twilio API guide with quick starts, patterns, and best practices

### Advanced References
- **advanced-features.md**: In-depth coverage of:
  - Messaging Services and Copilot
  - Conference calls and call recording
  - Twilio Functions (serverless)
  - Studio visual workflows
  - Sync real-time state
  - TaskRouter for contact centers
  - Lookup API for phone validation
  - Conversations API for multi-channel chat

- **real-world-examples.md**: Production-ready implementations:
  - Two-factor authentication (2FA) system
  - Appointment reminder service
  - Customer support chatbot
  - Order status notifications with fallback
  - Click-to-call web widget
  - SMS survey system
  - Emergency alert system

## Quick Start Examples

### Send an SMS

```javascript
const twilio = require('twilio');
const client = twilio(accountSid, authToken);

const message = await client.messages.create({
  body: 'Hello from Twilio!',
  from: '+15551234567',
  to: '+15559876543'
});
```

### Verify Phone Number (2FA)

```javascript
// Send verification code
await client.verify.v2
  .services(serviceSid)
  .verifications
  .create({ to: '+15559876543', channel: 'sms' });

// Check code
const check = await client.verify.v2
  .services(serviceSid)
  .verificationChecks
  .create({ to: '+15559876543', code: '123456' });

console.log(check.status); // 'approved'
```

### Make a Phone Call

```javascript
const call = await client.calls.create({
  url: 'http://demo.twilio.com/docs/voice.xml',
  to: '+15559876543',
  from: '+15551234567'
});
```

## Installation

This skill is part of the Claude Code skills library. To install:

```bash
cd /Users/jurrejan/Documents/development/_management/claude_skills
./install-skill.sh twilio-api
```

Or install all skills:

```bash
./install-skill.sh --all
```

## Skill Features

- ✅ **Multi-language support**: Examples in JavaScript, Python, Ruby, PHP, C#
- ✅ **Security best practices**: Webhook validation, credential management
- ✅ **Error handling**: Comprehensive error codes and retry strategies
- ✅ **Cost optimization**: Tips for reducing messaging costs
- ✅ **Production-ready**: Real-world examples with proper error handling
- ✅ **Testing guidance**: Test credentials and local development setup

## Prerequisites

To use Twilio APIs, you need:

1. A Twilio account (sign up at [twilio.com](https://www.twilio.com))
2. Account SID and Auth Token (from Twilio Console)
3. A Twilio phone number (for SMS/voice features)
4. The Twilio SDK for your programming language

## Environment Setup

```bash
# Set environment variables
export TWILIO_ACCOUNT_SID='ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
export TWILIO_AUTH_TOKEN='your_auth_token'
export TWILIO_PHONE_NUMBER='+15551234567'
```

## Use Cases Covered

- 📱 SMS notifications and alerts
- 🔐 Two-factor authentication (2FA)
- 📞 Voice calls and IVR systems
- 💬 WhatsApp Business messaging
- 📧 Transactional emails
- 📹 Video conferencing
- 🗓️ Appointment reminders
- 🤖 Customer support chatbots
- 📊 Order status tracking
- ⚠️ Emergency notifications

## Support & Resources

- [Twilio Documentation](https://www.twilio.com/docs)
- [Twilio Helper Libraries](https://www.twilio.com/docs/libraries)
- [API Status](https://status.twilio.com/)
- [Twilio Blog](https://www.twilio.com/blog)

## License

MIT

## Version

1.0 - Initial release (2025)

---

Built for Claude Code - AI-powered development assistant
