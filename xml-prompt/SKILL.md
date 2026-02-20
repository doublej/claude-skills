---
name: xml-prompt
description: Write well-structured XML prompts for Claude following Anthropic's official best practices. Use when writing system prompts, CLAUDE.md files, skill instructions, API prompts, or any structured prompt that benefits from XML tags. Covers the 10-component framework, common tag patterns, long context structure, and chain-of-thought with XML.
---

# XML Prompt Writing

Write structured, high-quality prompts for Claude using XML tags.

## When to Use XML Tags

- Prompt has multiple components (context, instructions, data, examples)
- Data and instructions must not be confused
- Output needs to be parseable (extract specific sections)
- Complex task requiring CoT separation (`<thinking>` / `<answer>`)
- Long context with multiple documents

## Quick Reference: Common Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `<instructions>` | Task steps | Numbered steps Claude must follow |
| `<context>` | Background info | Domain knowledge, situation |
| `<example>` / `<examples>` | Few-shot demos | Input/output pairs |
| `<document>` | Long content | PDFs, reports, code |
| `<thinking>` / `<answer>` | CoT separation | Reasoning vs. final output |
| `<constraints>` | Rules/limits | Length, format, tone |
| `<formatting_example>` | Output template | Desired structure |
| `<data>` | Input data | Spreadsheets, logs, user content |

## The 10-Component Framework

Structure prompts using up to 10 components. Not all are needed every time — use what fits.

```
1. Task Context       — WHO: Role and overall task
2. Tone Context       — HOW: Communication style
3. Background Data    — WHAT: Relevant documents/data
4. Rules              — MUST: Boundaries and requirements
5. Examples           — SHOW: 1-3 input/output pairs
6. Conversation History — PRIOR: Relevant context from before
7. Immediate Task     — NOW: Specific deliverable needed
8. Chain of Thought   — THINK: Reasoning steps
9. Output Format      — SHAPE: Structure of the response
10. Prefilled Response — START: Begin Claude's response
```

### Minimal Prompt (3 components)

```xml
<task>Summarise customer feedback into categories.</task>

<data>
{{FEEDBACK}}
</data>

<output_format>
Category: ...
Sentiment: Positive/Neutral/Negative
Priority: High/Medium/Low
</output_format>
```

### Full Prompt (all 10)

```xml
<role>You are a senior financial analyst at a B2B SaaS company.</role>

<tone>Professional, concise, data-driven. Use lists, not prose.</tone>

<background>
<document index="1">
  <source>q2_financials.xlsx</source>
  <document_content>{{Q2_DATA}}</document_content>
</document>
</background>

<rules>
1. Always cite specific numbers from the data.
2. Flag any metric that deviates >10% from Q1.
3. Maximum 500 words.
</rules>

<examples>
<example>
<input>Revenue: $12M (Q1) → $15M (Q2)</input>
<output>Revenue: $15M (+25% QoQ) — Flag: exceeds 10% threshold. Growth driven by enterprise segment.</output>
</example>
</examples>

<task>
Analyse Q2 financials. Highlight trends, flag concerns, recommend actions.
</task>

<thinking_instructions>
Before answering, reason through:
1. Which metrics changed significantly?
2. What caused the changes?
3. What actions follow?
Put reasoning in <thinking> tags, final report in <report> tags.
</thinking_instructions>

<output_format>
<report>
## Revenue
## Margins
## Cash Flow
## Recommendations
</report>
</output_format>
```

## Core Best Practices

### 1. Be Consistent
Use the same tag names throughout. Reference them explicitly:

```
Using the contract in <contract> tags, identify risks in these areas...
```

### 2. Nest for Hierarchy

```xml
<documents>
  <document index="1">
    <source>report.pdf</source>
    <document_content>{{CONTENT}}</document_content>
  </document>
</documents>
```

### 3. Separate Data from Instructions
Data at top, instructions below. Prevents Claude confusing input with directives.

```xml
<data>{{USER_INPUT}}</data>

<instructions>
Analyse the data above and produce a summary.
</instructions>
```

### 4. Use Tags for Parseable Output
Ask Claude to wrap output in tags for extraction:

```xml
Put your analysis in <analysis> tags and your recommendation in <recommendation> tags.
```

### 5. Long Context: Documents First, Query Last

```xml
<documents>
  <document index="1">
    <source>annual_report.pdf</source>
    <document_content>{{REPORT}}</document_content>
  </document>
  <document index="2">
    <source>competitor.xlsx</source>
    <document_content>{{COMPETITOR}}</document_content>
  </document>
</documents>

Analyse the annual report and competitor analysis. Identify strategic advantages.
```

Queries at the end improve response quality by up to 30%.

## Chain of Thought with XML

### Basic CoT
```
Think step-by-step before answering. Put reasoning in <thinking> tags, answer in <answer> tags.
```

### Guided CoT
```xml
<thinking_steps>
1. Identify key components of the problem
2. List assumptions
3. Evaluate options with trade-offs
4. Select best approach
</thinking_steps>

Put your reasoning in <thinking> tags following the steps above.
Put your final answer in <answer> tags.
```

### Extended Thinking Mode
When using Claude's built-in extended thinking, use `<scratchpad>` or `<thinking>` in few-shot examples — Claude generalises the pattern.

## Multishot Prompting with XML

Wrap examples in `<examples>` with nested `<example>` tags. Include 3-5 diverse examples.

```xml
<examples>
<example>
<input>The dashboard is slow and the export button is missing.</input>
<output>
Category: UI/UX, Performance
Sentiment: Negative
Priority: High
</output>
</example>
<example>
<input>Love the Salesforce integration! Would be great to add HubSpot too.</input>
<output>
Category: Integration, Feature Request
Sentiment: Positive
Priority: Medium
</output>
</example>
</examples>

Now analyse this feedback: {{FEEDBACK}}
```

## System Prompt Patterns

### Role + Behaviour
```xml
<role>You are a senior security auditor specialising in web applications.</role>

<behaviour>
- Always check OWASP Top 10 vulnerabilities
- Cite specific CWE identifiers
- Rate severity using CVSS v3.1
- Never suggest disabling security controls as a fix
</behaviour>
```

### Agentic Patterns

```xml
<default_to_action>
Implement changes rather than suggesting them.
If intent is unclear, infer the most useful action.
</default_to_action>
```

```xml
<investigate_first>
Never speculate about code you have not read.
Read relevant files BEFORE answering questions.
</investigate_first>
```

## Prompt Chaining with XML

Pass output between prompts using XML tags as handoff points:

**Prompt 1** → outputs `<analysis>...</analysis>`
**Prompt 2** → receives `<analysis>{{PREV_OUTPUT}}</analysis>` as input

```xml
<!-- Prompt 2 -->
Based on this analysis:
<analysis>{{ANALYSIS_FROM_STEP_1}}</analysis>

Draft actionable recommendations in <recommendations> tags.
```

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Tags without referencing them | Claude may ignore structured data | "Using the data in `<data>` tags..." |
| Putting instructions inside data tags | Confuses data/instruction boundary | Separate `<data>` and `<instructions>` |
| Inconsistent tag names | Creates ambiguity | Pick one name, use everywhere |
| Over-nesting (>3 levels deep) | Reduces clarity | Flatten where possible |
| HTML-like tags (`<div>`, `<span>`) | May trigger HTML parsing behaviour | Use semantic names (`<section>`, `<context>`) |
| Tags for single-sentence content | Adds noise without benefit | Use plain text for simple content |

## Validation Checklist

Before finalising an XML-structured prompt:

- [ ] Every tag is referenced in the instructions ("Using the X in `<X>` tags...")
- [ ] Data appears before instructions
- [ ] Tags are consistent (same names throughout)
- [ ] Examples are wrapped in `<example>` / `<examples>`
- [ ] Long documents use `<document index="N">` with `<source>` metadata
- [ ] Output format is specified (either via tags or explicit structure)
- [ ] No tags nested deeper than 3 levels
- [ ] CoT uses separate tags for reasoning vs. answer
