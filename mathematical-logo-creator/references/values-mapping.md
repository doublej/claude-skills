# Values → Parameters Mapping

Detailed guide for converting brand values into measurable construction parameters.

## Mapping Method

1. Choose 3-5 brand values with weights summing to 1.0
2. For each value, assign a target direction for 1-2 visual metrics (not 10)
3. Bind metrics to parameters of the chosen mathematical family

## Visual Metrics Reference

| Metric | Symbol | Range | What it measures |
|--------|--------|-------|------------------|
| Symmetry order | `n` | 1-12 | Rotational symmetry count (1 = no symmetry) |
| Curvature bound | `κ_max` | 0-∞ | Max sharpness of turns (lower = smoother) |
| Complexity | `C` | 1-20 | Feature count after simplification |
| Negative-space ratio | `NS` | 0-0.6 | Interior void / outer silhouette area |
| Stroke ratio | `SR` | 0.05-0.25 | Stroke width / mark diameter |
| Variance | `V` | 0-1 | Deviation from ideal symmetric shape |
| High-freq detail | `HF` | 0-1 | Amount of fine-grained features |

## Extended Value → Parameter Table

| Value | Visual objective | Parameter handles | Expected effect |
|-------|------------------|-------------------|-----------------|
| Precision | ordered, exact | `n↑`, `V↓`, `C↓`, `κ_max↓` | Regular silhouette, fewer surprises |
| Openness | breathable, inviting | `NS↑`, `g_min↑` | More interior space, better small-size legibility |
| Resilience | robust, stable | `SR↑`, `t_min↑`, loops `L≥1` | Survives scaling and production |
| Warmth | friendly, human | `κ_max↓`, corner exponent `p→2`, `HF↓` | Softer turns, no spiky features |
| Energy | dynamic, bold | `C↑`, amplitude `a↑`, asymmetry | More visual activity |
| Innovation | forward, unconventional | low `n` (2-3), higher `V`, unusual family | Unexpected silhouette |
| Trust | reliable, established | high `n` (4-8), `V↓`, `SR↑` | Stable, familiar geometry |
| Elegance | refined, minimal | `C↓`, thin `SR`, high contrast | Clean, spare silhouette |
| Playfulness | fun, approachable | `κ_max↓`, `NS↑`, bright palette | Rounded, open, inviting |
| Authority | commanding, strong | `SR↑`, angular `κ_max↑`, `V↓` | Bold, structured, imposing |

## Why These Parameters Express Values

- **Symmetry (`n`)**: measurable proxy for order and structure — reduces degrees of freedom, increases predictability
- **Negative space (`NS`) + min gap (`g_min`)**: directly quantifies openness — how much "air" the mark contains
- **Stroke ratio (`SR`) + min thickness (`t_min`)**: quantifies resilience — predicts survivability under lossy reproduction
- **Curvature bounds (`κ_max`) + high-freq removal (`HF`)**: quantifies warmth — prevents aggressive angles and spikes

## Worked Example

### Input values
- Precision (0.35)
- Openness (0.25)
- Resilience (0.25)
- Warmth (0.15)

### Filled mapping

| Value | w | Visual objective | Parameter handle | Target |
|-------|---|------------------|------------------|--------|
| Precision | 0.35 | high order, low variance | `n↑`, `V↓`, `C↓` | `n=6`, `V<0.05`, `C≤8` |
| Openness | 0.25 | breathable, inviting | `NS↑`, `g_min↑` | `NS≈0.38`, `g_min≥2px@16px` |
| Resilience | 0.25 | robust reproduction | `SR↑`, `t_min↑` | `SR=0.14`, `t_min≥1.6px@16px` |
| Warmth | 0.15 | friendly, non-aggressive | `κ_max↓`, `HF↓` | bounded curvature, 1 harmonic only |

### Chosen family: Polar Fourier with C6 symmetry

```
r(θ) = 1 + 0.18 × cos(6θ)
```

Parameters:
- Symmetry order: `n = 6` (precision)
- Amplitude: `a = 0.18` (distinctive but not spiky)
- Negative space target: `NS ≈ 0.38` (openness)
- Stroke ratio: `SR = 0.14` (resilience)
- Single harmonic only (warmth — no high-freq detail)

### Result description

Six-fold rotationally symmetric closed mark: smooth rosette silhouette with six gentle bulges, drawn as a single thick continuous ring. Large clean central void with no narrow pinch points. Curvature never spikes. Effect: ordered but welcoming.

### Validation

1. **Favicon (16px)**: central void stays open, silhouette distinct
2. **One-colour**: solid fill and knockout both legible
3. **Distance test**: identifiable at ~2m / ~1.5cm on screen
4. **Parameter stability**: ±5% on `a` and `SR` — mark remains recognisable
5. **Value traceability**: precision→n=6, openness→NS=0.38, resilience→SR=0.14, warmth→single harmonic
