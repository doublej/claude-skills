---
name: prompt
description: Analyze and optimize prompts or briefings. Use when asked to review, improve, combine, or rewrite a prompt, system message, or AI instruction set. Extracts high-value elements, removes redundancy, and synthesizes a cleaner result.
---

# Prompt Optimizer

Analyze prompts for structure and effectiveness, then synthesize an optimized version. Prefer specificity over generality. Identify only essential elements — ruthlessly cut redundancy.

## Analysis Framework

Work through these four lenses:

**Structure**
- Role definition — is it clear, grounded, appropriately scoped?
- Context — does it give the model what it needs and nothing more?
- Instructions — are they unambiguous and actionable?
- Constraints — are output format and limits explicit?

**Element quality**
- High-value: specific methodologies, concrete examples, measurable criteria
- Low-value: vague adjectives ("be helpful"), restating the obvious, nested redundancy

**Effectiveness**
- Clarity — would a capable model misinterpret any instruction?
- Specificity — are general statements replaceable with concrete ones?
- Alignment — do all instructions point toward the same goal?
- Conflicts — do any instructions contradict each other?

**Redundancy**
- Same instruction stated multiple times → keep once, strongest form
- Role described in both system and instructions → consolidate
- Meta-commentary about the prompt itself → cut

## Synthesis Process

1. List elements found across all source prompts (if combining multiple)
2. Score each: keep / cut / merge
3. Resolve conflicts — pick the more specific or safety-oriented rule
4. Draft optimized prompt: role → context → instructions → constraints → output format
5. Verify: read output aloud — does every sentence add new information?

## Output Format

Deliver:

```
## What changed
- [bullet: element kept, cut, or merged and why]

## Optimized prompt
[the rewritten prompt, ready to use]
```

If combining multiple prompts, add a brief note on conflicts resolved.

## Prompt Engineering Principles

- **Role**: one sentence, active voice — "You are a X that does Y"
- **Instructions**: imperative form — "Extract", "Return", "Avoid"
- **Examples**: show one good example rather than explaining the pattern
- **Constraints**: state what NOT to do only when the failure mode is real
- **Output format**: specify format explicitly when it matters (JSON, markdown table, bullet list)
- **Length guidance**: a shorter prompt that works beats a longer one that might
