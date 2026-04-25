---
name: small-model-prompt
description: "Prompts and configs for small 8B models (Llama 3.1), Ollama/llama.cpp"
---

# Small Model Prompt

Write prompts that actually work on 8B models. These models are capable but unforgiving — they need clear, constrained prompts with no ambiguity.

<core_constraint>

## The 8B Reality

8B models have ~10% of a frontier model's capacity. They can follow instructions well IF you respect their limits:

- **One task per prompt** — no multi-step chains
- **Short system prompts** — under 200 words, ideally under 100
- **Explicit output format** — show don't tell
- **No nested logic** — flatten conditionals into separate prompts
- **No meta-reasoning** — "think step by step" wastes capacity; give the steps directly

</core_constraint>

<prompt_design_rules>

### 1. Lead with role, constrain immediately

```
You are a JSON extractor. You read text and output valid JSON. Nothing else.
```

NOT:
```
You are a helpful AI assistant that can extract structured data from unstructured text
and return it in various formats including JSON, YAML, or CSV depending on the user's needs.
```

### 2. Give the output format as a literal example

```
Output format:
{"name": "...", "age": ..., "city": "..."}
```

8B models copy patterns better than they follow abstract format descriptions.

### 3. Use separator tokens

Small models lose track of where instructions end and input begins. Use clear delimiters:

```
---INPUT---
{user_text}
---OUTPUT---
```

### 4. Avoid negations

Say what TO do, not what NOT to do. 8B models are bad at negation.

- Bad: "Don't include explanations"
- Good: "Output only the JSON object"

### 5. Keep vocabulary simple

Use common words. Avoid jargon, idioms, or complex sentence structures in system prompts. The model's instruction-following degrades with unusual phrasing.

</prompt_design_rules>

<sampling_params>

For 8B models:
- **One example** dramatically improves output quality
- **Zero examples** works for simple tasks with clear format specs
- **3+ examples** can confuse — the model may over-fit to example content

### 7. Temperature matters more than prompt engineering

For instruction following, low temperature is essential. A perfect prompt at temp=0.8 will underperform a decent prompt at temp=0.1.

### Instruction Following / Chat

```json
{
  "temperature": 0.3,
  "top_p": 0.9,
  "top_k": 40,
  "repeat_penalty": 1.1,
  "num_predict": 512
}
```

### Strict Extraction (JSON, data)

```json
{
  "temperature": 0.0,
  "top_p": 1.0,
  "top_k": 1,
  "repeat_penalty": 1.0,
  "num_predict": 256
}
```

### Creative / Conversational

```json
{
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 50,
  "repeat_penalty": 1.15,
  "num_predict": 1024
}
```

</sampling_params>

<llama_chat_template>

See `references/llama31-template.md` for the exact chat template format.

Key points:
- Uses `<|begin_of_text|>`, `<|start_header_id|>`, `<|end_header_id|>`, `<|eot_id|>` special tokens
- System message goes first, then alternating user/assistant turns
- Always end with `<|start_header_id|>assistant<|end_header_id|>\n\n` to prompt generation

</llama_chat_template>

<output_format>

When the user describes their task, produce a complete config block:

```yaml
# Task: {description}
# Model: llama3.1:8b

system: |
  {system_prompt}

parameters:
  temperature: {value}
  top_p: {value}
  top_k: {value}
  repeat_penalty: {value}
  num_predict: {value}
  stop: ["{stop_token}"]

example_input: |
  {example}

expected_output: |
  {example}
```

</output_format>

<workflow>

1. **Clarify task** — what exactly should the model do? One thing only.
2. **Pick task type** — instruction following, extraction, creative, classification
3. **Write system prompt** — role + constraint + format example, under 100 words
4. **Set sampling params** — use presets from above, tuned for task type
5. **Add one-shot example** — real input/output pair
6. **Output full config** — yaml block with everything needed to run

</workflow>

<common_patterns>

### Classification
```
You are a classifier. Read the text and output exactly one label.
Labels: positive, negative, neutral

---INPUT---
{text}
---LABEL---
```

### Extraction
```
You extract contact info from text. Output JSON only.
Format: {"name": "...", "email": "...", "phone": "..."}
Use null for missing fields.

---TEXT---
{text}
---JSON---
```

### Rewriting
```
You rewrite text to be {style}. Output only the rewritten text.

---ORIGINAL---
{text}
---REWRITTEN---
```

### Q&A with Context
```
Answer the question using only the provided context. If the answer is not in the context, say "Not found."

---CONTEXT---
{context}
---QUESTION---
{question}
---ANSWER---
```

</common_patterns>

<anti_patterns>

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Long system prompts (>300 words) | Instruction following degrades | Cut to essentials, move detail to one-shot example |
| "Think step by step" | Wastes tokens on rambling reasoning | Provide the steps explicitly |
| Multiple output formats | Model mixes them up | One format per prompt |
| Complex conditionals | "If X then Y, else if Z then W" | Split into separate prompts |
| Asking for self-evaluation | No capacity for meta-cognition | Evaluate externally |
| Markdown formatting instructions | Produces mangled markdown | Use plain text or strict JSON |

</anti_patterns>
