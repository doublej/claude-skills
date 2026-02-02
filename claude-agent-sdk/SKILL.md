---
name: claude-agent-sdk
description: Builds production-ready AI agents with Claude Agent SDK. Covers installation, authentication, tool permissions, MCP integration, and agent patterns. Use when building custom AI agents, integrating Claude as an autonomous agent, or extending Claude Code capabilities.
---

# Claude Agent SDK Skill

## Overview
Build production-ready custom AI agents with the Claude Agent SDK. Built on the agent harness that powers Claude Code, it provides everything needed for building autonomous agents with advanced capabilities.

**Key advantage**: Automatic context management, rich tool ecosystem, fine-grained permissions, and built-in error handling.

## Installation

### TypeScript
```bash
npm install @anthropic-ai/claude-agent-sdk
```

### Python
```bash
pip install claude-agent-sdk
```

## SDK Forms Available
- **TypeScript SDK** - For Node.js and web applications
- **Python SDK** - For Python applications and data science
- **Streaming vs Single Mode** - Choose input mode based on your use case

## Why Use Claude Agent SDK?

### Built-in Capabilities
- **Context Management**: Automatic compaction and context management prevents running out of context
- **Rich Tool Ecosystem**: File operations, code execution, web search, MCP extensibility
- **Advanced Permissions**: Fine-grained control over agent capabilities
- **Production Essentials**: Error handling, session management, monitoring
- **Performance**: Automatic prompt caching and optimizations

## Authentication Methods

### Primary (Anthropic API)
```
Set ANTHROPIC_API_KEY environment variable
Get key from: https://platform.claude.com/api
```

### Third-Party Providers
- **Amazon Bedrock**: Set `CLAUDE_CODE_USE_BEDROCK=1` + AWS credentials
- **Google Vertex AI**: Set `CLAUDE_CODE_USE_VERTEX=1` + Google Cloud credentials
- **Microsoft Foundry**: Set `CLAUDE_CODE_USE_FOUNDRY=1` + Azure credentials

## Core Concepts

### Agent Structure
1. **System Prompt**: Define role, expertise, behavior
2. **Tool Permissions**: Control which tools agent can use
3. **Context Management**: Handle large conversations
4. **Session Management**: Track agent state

### Tool Permissions
- `allowedTools` - Explicitly allow specific tools
- `disallowedTools` - Block specific tools
- `permissionMode` - Set overall permission strategy

## Full Claude Code Feature Support

The SDK provides access to all Claude Code features:
- **Subagents** (`./.claude/agents/`) - Specialized agents
- **Agent Skills** (`./.claude/skills/`) - Extended capabilities
- **Hooks** (`./.claude/settings.json`) - Custom command execution
- **Slash Commands** (`./.claude/commands/`) - Custom commands
- **Plugins** - Load custom extensions programmatically
- **Memory (CLAUDE.md)** - Project context persistence

Set `settingSources: ['project']` (TypeScript) or `setting_sources=["project"]` (Python) to load CLAUDE.md files.

## Model Context Protocol (MCP)

Extend agents with custom tools through MCP servers:
- Connect to databases
- Integrate external APIs
- Add specialized capabilities
- Custom service integrations

## Example Agent Types

### Coding Agents
- SRE agents for production issue diagnosis and fixes
- Security review bots auditing code for vulnerabilities
- Oncall engineering assistants for incident triage
- Code review agents enforcing style and best practices

### Business Agents
- Legal assistants reviewing contracts and compliance
- Finance advisors analyzing reports and forecasts
- Customer support agents resolving technical issues
- Content creation assistants for marketing teams

## Quick Start Pattern

1. **Set up authentication**
   - Export `ANTHROPIC_API_KEY` or configure third-party provider

2. **Define system prompt**
   - Specify agent role and capabilities

3. **Configure tool permissions**
   - Use `allowedTools` or `disallowedTools`

4. **Initialize agent**
   - Create agent instance with desired configuration

5. **Handle input/output**
   - Choose streaming or single mode based on use case

## Best Practices

- **Start minimal**: Begin with essential tools, add features as needed
- **Test permissions**: Verify agent can only access intended tools
- **Handle errors**: Implement proper error handling at system boundaries
- **Monitor context**: Watch for context growth in long-running agents
- **Use MCP wisely**: Extend capabilities through MCP for custom integrations
- **Document prompts**: Keep system prompts clear and maintainable

## Configuration Files

### CLAUDE.md (Project-level instructions)
Place in `.claude/CLAUDE.md` or project root. Loaded when `settingSources: ['project']` is set.

### .claude/settings.json
Configure hooks, commands, and settings for agent behavior.

### Environment Variables
- `ANTHROPIC_API_KEY` - Anthropic API authentication
- `CLAUDE_CODE_USE_BEDROCK` - Enable Amazon Bedrock
- `CLAUDE_CODE_USE_VERTEX` - Enable Google Vertex AI
- `CLAUDE_CODE_USE_FOUNDRY` - Enable Microsoft Foundry

## Streaming vs Single Mode

- **Streaming Mode**: Real-time output, better UX for long operations
- **Single Mode**: Complete response at once, simpler integration

Choose based on your application's needs and interaction patterns.

## Resources

- **Documentation**: https://platform.claude.com/docs/en/agent-sdk/overview
- **TypeScript GitHub**: https://github.com/anthropics/claude-agent-sdk-typescript
- **Python GitHub**: https://github.com/anthropics/claude-agent-sdk-python
- **Changelog**: Check GitHub repos for latest updates
- **Support**: Report issues on GitHub issue trackers

## Branding Guidelines (for partners)

**Allowed naming**:
- "Claude Agent" (preferred)
- "Claude" (in agent menus)
- "{YourAgentName} Powered by Claude"

**Not allowed**:
- "Claude Code" or "Claude Code Agent"
- Claude Code branded elements

## Key Takeaways

✓ Production-ready agent building
✓ Automatic context and session management
✓ Fine-grained tool permissions
✓ MCP extensibility for custom integrations
✓ Full Claude Code feature parity
✓ Multiple authentication methods
✓ Optimized performance with prompt caching
