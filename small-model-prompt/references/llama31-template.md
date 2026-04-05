# Llama 3.1 8B Chat Template

## Special Tokens

| Token | Purpose |
|---|---|
| `<\|begin_of_text\|>` | Start of sequence |
| `<\|end_of_text\|>` | End of sequence |
| `<\|start_header_id\|>` | Start of role header |
| `<\|end_header_id\|>` | End of role header |
| `<\|eot_id\|>` | End of turn |

## Template Structure

```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

```

Note: the double newline after each `<|end_header_id|>` is required.

## Multi-Turn

```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_message_1}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{assistant_response_1}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_message_2}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

```

## Ollama Modelfile

```dockerfile
FROM llama3.1:8b

SYSTEM """
{system_prompt}
"""

PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
PARAMETER num_predict 512
PARAMETER stop "<|eot_id|>"
PARAMETER stop "<|end_of_text|>"
```

## llama.cpp / llama-server

```bash
llama-server \
  -m models/llama-3.1-8b-instruct.gguf \
  --chat-template llama3 \
  --temp 0.3 \
  --top-p 0.9 \
  --top-k 40 \
  --repeat-penalty 1.1 \
  -n 512
```

## GGUF Quantization Notes

For 8B models, recommended quantizations by use case:

| Quant | Size | Quality | Use case |
|---|---|---|---|
| Q8_0 | ~8.5 GB | Best | When VRAM allows |
| Q6_K | ~6.6 GB | Great | Good default |
| Q5_K_M | ~5.7 GB | Good | Balanced |
| Q4_K_M | ~4.9 GB | Decent | Memory constrained |
| Q3_K_M | ~3.9 GB | Acceptable | Edge/mobile |
| Q2_K | ~3.2 GB | Poor | Last resort |

Instruction following degrades noticeably below Q4_K_M. Use Q5_K_M or higher for reliable structured output.
