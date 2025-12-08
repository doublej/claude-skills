---
name: ultra-designer
description: Racing/tech design toolkit using numeric dials, coordinates, and structured language. Direct bold visual work through adjustable 0–5 scales, zone-based layouts, and precise motion notation. Produces complete design briefs for handoff to collaborators or generative tools. Includes 8 style presets from Premium Broadcast to Rally Chaos.
---

# Racing/Tech Design Toolkit

A skillset for directing bold visual work through numeric dials, spatial coordinates, and structured language.

---

## 1. Design Direction & Intent

You can:
- Define the visual "feel" of racing/tech content in 1–2 sentences
- Direct work using adjustable dials (0–5) instead of vague visual language
- Produce a complete, structured brief that a collaborator or generative tool can implement
- Commit to a bold aesthetic direction and execute with precision

**Before any design work, answer:**
- **Purpose:** What problem does this interface solve? Who uses it?
- **Tone:** Which style preset fits, or what extreme are you creating?
- **Differentiation:** What's the ONE thing someone will remember?

---

## 2. Spatial Mapping & Orientation

Your tools:

### Mental Canvas
- **Default:** Landscape 16:9
- **Zones:** 3×3 grid — TL, TC, TR, ML, MC, MR, BL, BC, BR
- **Precision:** Add percent coordinates (x%, y%) for exact placement
- **Origin:** Top-left = (0%, 0%); x% left→right, y% top→bottom

### Layout Description
- Define canvas ratio and safe margins in %
- Describe reading order and focal path (e.g., TL → MC → BR)
- Plan whitespace: where to keep areas empty and why (breathing room, emphasis, separation)

---

## 3. Visual Hierarchy & Separation

You can classify every element by:

| Property | Values |
|----------|--------|
| **Role** | hero / secondary / tertiary |
| **Size Rank** | 1–5 (1 = largest, 5 = smallest) |
| **Contrast** | low / medium / high |
| **Separation** | spacing, outline, shadow, texture, border |

You can make hierarchy explicit:
- Identify a single hero when needed
- Justify it via size, contrast, or position
- Control how clearly the hero dominates (Hierarchy dial)

---

## 4. Motion Design Notation

Your motion toolkit:

### Timings
Express durations in milliseconds: 220ms, 600ms, etc.

### Paths
Describe movement verbally:
- "from left off-screen to MC"
- "from BL to TR on a diagonal"
- "panels slide in from left, stagger 50ms"

### Easing
Use common names: ease-in, ease-out, linear, overshoot

### Rhythm & Safety
- Avoid bouncing, flashing, or jitter unless style demands it
- Limit to 3 motion events per second
- Label anything faster as "fast rhythm" explicitly

### Loop Behaviors
Describe: telemetry updates, scanlines, pulses, count-ups, repeat intervals

---

## 5. Typographic System Design

Build a type system by specifying:

| Parameter | Options |
|-----------|---------|
| **Role** | title / label / data |
| **Weight** | light / regular / bold |
| **Width** | normal / condensed |
| **Case** | uppercase / mixed |
| **Size Rank** | 1–5 |
| **Alignment** | left / center / right |

### Data Formatting
- Mono vs proportional for numbers
- Decimal alignment for telemetry and stats

### Typography Anti-Patterns (NEVER)
- Inter, Roboto, Arial, system fonts
- Generic sans-serif without character
- Same treatment for all text roles

---

## 6. Texture, Effects & Contrast Control

### Texture Scales

| Intensity | Feel |
|-----------|------|
| 0 | Smooth, clean |
| 1–2 | Soft grain, subtle |
| 3 | Moderate grit |
| 4–5 | Heavy grunge, noisy |

**Sources:** grain, vignette, glow, blur, grit, scanlines

**Glow types:**
- **Controlled:** subtle utility, legibility aid
- **Expressive:** noticeable flair, atmosphere

### Contrast & Accents
- **Overall contrast:** low / medium / high
- **Accent usage:** none / sparse / frequent
- For any visual emphasis, define its role:
  - "high-contrast highlight on key lap times"
  - "muted background panel for low-priority data"
  - "accent border on active selection"

---

## 7. Dial-Based Art Direction (0–5 Controls)

Steer any design using six numeric dials:

| Dial | 0 | 5 | Heuristic |
|------|---|---|-----------|
| **Density** | Empty | Crowded | Visible panels/labels per screen |
| **Energy** | Calm | Hyper | Cut frequency & motion amplitude |
| **Geometry** | Straight grids | Wild angles/curves | % non-orthogonal edges |
| **Texture** | Clean | Rough/noisy | Grain/overlay intensity |
| **Motion** | Slow ease | Violent snap | Avg transition time & overshoot |
| **Hierarchy** | Flat | One clear hero | Hero's size/contrast lead |

You can:
- Set and adjust these dials to define a look
- Communicate changes as simple numeric tweaks: "energy +1", "hierarchy −1"
- Compare designs by their dial signatures

---

## 8. Output Framework: Design Brief

Structure every project as a reusable brief:

```xml
<design_brief>

1) INTENT
   [1–2 sentences: purpose and mood]

2) DIAL SETTINGS
   {density: 0–5, energy: 0–5, geometry: 0–5, texture: 0–5, motion: 0–5, hierarchy: 0–5}

3) LAYOUT MAP
   - Canvas: [ratio, orientation, safe margins %]
   - Zones & flow: [reading order and focal path]
   - Whitespace: [where/why empty areas exist]

4) ELEMENTS
   [Repeat for each]
   - id: [unique identifier]
   - role: hero | secondary | tertiary
   - size_rank: 1–5
   - position: [zone + x%, y%]
   - alignment: [L/C/R, T/M/B]
   - separation: spacing | border | outline | shadow | texture
   - content: [what it communicates]

5) TYPOGRAPHY SYSTEM
   - Title: [weight, width, case, size rank, alignment]
   - Labels: [weight, width, size rank, casing]
   - Data: [mono/prop, alignment method]

6) TEXTURE & EFFECTS
   - Intensity: 0–5
   - Sources: [grain, vignette, glow, etc.]
   - Glow type: controlled | expressive

7) MOTION SCRIPT
   - Transitions: [element → timing ms → easing]
   - Paths: [start → end; overshoot/jitter if any]
   - Loops: [updates, scanlines, pulses, intervals]

8) CONTRAST & ACCENTS
   - Overall contrast: low | medium | high
   - Accent usage: none | sparse | frequent
   - Accent targets: [what gets emphasized and why]

9) QA CHECKLIST
   [ ] Every element named, ordered, role-assigned
   [ ] Hero identified with explicit justification
   [ ] Min body size rank ≥2; adequate spacing
   [ ] Motion safe (no flashes; >3Hz labeled "fast rhythm")
   [ ] Summary ≤120 words included

10) SUMMARY
    [≤120 words describing the composition for quick reference]

</design_brief>
```

---

## 9. Style Library (Presets)

Select and tweak style clusters by setting dials and rules:

### 1. Premium Broadcast
*F1 / Mercedes / Gran Turismo / Forza Motorsport*

**Dials:** density 2–3 | energy 2–3 | geometry 1 | texture 0–1 | motion 2–3 | hierarchy 4–5

| Aspect | Specification |
|--------|---------------|
| Feel | Metronome-clean, surgical clicks |
| Layout | Rigid grid; consistent margins; one hero; aligned secondaries |
| Shapes | Rectangles; thin rules; UI cards; consistent corners |
| Texture | Very smooth; minimal glow/metal hints |
| Type | Engineered sans; uppercase titles; condensed labels; decimal-aligned data |
| Motion | 150–300ms snaps; straight paths; subtle overshoot |

**Use when:** Premium, controlled, tool-like clarity

---

### 2. Futuristic HUD
*Formula E / Electric racing / AI interfaces*

**Dials:** density 3–4 | energy 3–4 | geometry 3 | texture 2–3 | motion 3–4 | hierarchy 3–4

| Aspect | Specification |
|--------|---------------|
| Feel | Synth arps, short glitch bursts |
| Layout | Layered HUD cards over wireframes; aligned overlaps |
| Shapes | Thin lines, brackets, arcs + rectangles |
| Texture | Glow/blur duplicates; scanlines; noise overlays |
| Type | Condensed/digital; thin + bold mix; kinetic reveals |
| Motion | Micro-glitches (1–4 frames); multi-direction slides; count-ups |

**Use when:** Future/AI/data-heavy modules

---

### 3. Cinematic Heritage
*WEC / Le Mans / Porsche Motorsport*

**Dials:** density 1–2 | energy 1–2 | geometry 1–2 | texture 2 | motion 1–2 | hierarchy 4

| Aspect | Specification |
|--------|---------------|
| Feel | Slow build, long notes |
| Layout | Wide letterbox; weight at center or lower third |
| Shapes | Large bars/blocks; few important elements |
| Texture | Soft gradients; subtle vignette; blur streaks |
| Type | Refined sans; optional serif titles; generous margins |
| Motion | 400–800ms fades/slides; slow pans; light parallax |

**Use when:** Epic intros, brand film moments

---

### 4. Rally Chaos
*WRC / Alpinestars / Hoonigan*

**Dials:** density 4 | energy 5 | geometry 4 | texture 4–5 | motion 4–5 | hierarchy 3

| Aspect | Specification |
|--------|---------------|
| Feel | Gravel hits, snare rattles |
| Layout | Broken grid; diagonals; dense clusters vs voids |
| Shapes | Jagged/torn/brush/splashes; rotated type |
| Texture | Heavy grit/splatter; slight mis-registration (1–2px) |
| Type | Bold/heavy; stencil/distressed edges |
| Motion | Impact cuts; 1–2 frame shakes; speed ramps; debris |

**Use when:** Wild enthusiast energy, impact

---

### 5. Hype Festival
*Red Bull Racing / Forza Horizon / Youth culture*

**Dials:** density 4 | energy 5 | geometry 3–4 | texture 3–4 | motion 4–5 | hierarchy 3

| Aspect | Specification |
|--------|---------------|
| Feel | Festival drops, crowd stabs |
| Layout | Sticker/poster layers; overlapping hooks around hero |
| Shapes | Clean blocks + hand-drawn accents; sweeping arcs |
| Texture | Noise; light leaks; lens flare; vignettes |
| Type | Punchy display + handwritten notes; short phrases |
| Motion | Frequent cuts; brush wipes; squash/stretch pops; beat-synced ("fast rhythm") |

**Use when:** Promos, community, youth appeal

---

### 6. Hardcore Sim
*iRacing / Assetto Corsa / ACC*

**Dials:** density 3–4 | energy 1–2 | geometry 1–2 | texture 0–1 | motion 1–2 | hierarchy 3–4

| Aspect | Specification |
|--------|---------------|
| Feel | Mission control beeps |
| Layout | Tables/lists; logical panel groups; clear separation |
| Shapes | Rectangular panels; minimal decoration |
| Texture | Flat; no glows or dirt |
| Type | Readable sans; condensed; monospaced numbers; decimal alignment |
| Motion | Understated fades; smooth realtime updates |

**Use when:** Configuration, telemetry, credibility

---

### 7. Equipment & Streetwear

**7a. Pro Equipment** *(Alpinestars / Sparco)*

**Dials:** density 2–3 | energy 2 | geometry 1–2 | texture 1 | motion 2 | hierarchy 4

| Aspect | Specification |
|--------|---------------|
| Feel | Wind-tunnel hush |
| Layout | Simple, symmetrical; product/spec/brand zones |
| Shapes | Rectangles + technical icons |
| Texture | Light brushed/grid; no grunge |
| Type | Slightly italic; clarity over flair |
| Motion | Smooth slides/fades; aerodynamic whoosh |

**7b. Streetwear Motorsport** *(PUMA Motorsports)*

**Dials:** density 3 | energy 3–4 | geometry 2–3 | texture 2–3 | motion 3 | hierarchy 3

| Aspect | Specification |
|--------|---------------|
| Feel | Editorial flips, camera shutters |
| Layout | Lookbook blocks; intentional asymmetry |
| Shapes | Sharp blocks + organic fabric accents |
| Texture | Tactile/photo-led; fabric feel |
| Type | Bold headlines + neat body; fashion contrast |
| Motion | Jump-cuts; slow-mo hero + quick detail pops |

---

### 8. Esports Overlays
*Veloce / WTF1 / F1 Sim Racing*

**Dials:** density 3 | energy 4 | geometry 2–3 | texture 2 | motion 4 | hierarchy 5

| Aspect | Specification |
|--------|---------------|
| Feel | Stream stingers, meme beats |
| Layout | Corner/edge bars; center reserved for gameplay |
| Shapes | Modular tabs/tags; replay labels |
| Texture | Moderate glow/shadow for legibility |
| Type | Bold short labels; outlines; frequent entrances/exits |
| Motion | <250ms transitions; geometric wipes; scale pops |

**Use when:** Livestreams, creator content

---

## 10. QA & Verification

Systematically verify:

- [ ] Every element named, ordered, role-assigned
- [ ] Hero identified with explicit justification (size/contrast/position)
- [ ] Minimum body size rank ≥2 with adequate spacing
- [ ] Data is legible with proper alignment
- [ ] Motion is safe: no rapid flashes
- [ ] Any >3Hz motion labeled "fast rhythm"
- [ ] Summary (≤120 words) accurately reflects layout and hierarchy

---

## 11. Handoff Communication

### To a Collaborator
> Implement the attached `<design_brief>`. Follow positions, sizes, contrast, and motion timings exactly.
>
> Choose any color palette that preserves specified contrast and accent usage.
>
> Return: (a) layered file, (b) alt-text per element, (c) list of deviations.

### To a Generative Tool
> Create visuals matching `<design_brief>`. Prioritize grid, hierarchy, contrast, and motion script.
>
> Do not add effects not listed.
>
> Output: stills plus motion preview per motion script.

---

## Example Brief

```xml
<design_brief>

1) INTENT
   Serious telemetry card for premium broadcast. Clean, surgical, authoritative.

2) DIAL SETTINGS
   {density: 3, energy: 2, geometry: 1, texture: 1, motion: 2, hierarchy: 5}

3) LAYOUT MAP
   - Canvas: 16:9 landscape; safe margin 4%
   - Zones & flow: TL → MC → MR → BR
   - Whitespace: generous margins around hero; breathing between data columns

4) ELEMENTS
   - id: driver_name
     role: hero
     size_rank: 1
     position: MC (50%, 40%)
     alignment: C, M
     separation: spacing + shadow
     content: Driver name in uppercase

   - id: lap_time
     role: secondary
     size_rank: 2
     position: MR (75%, 50%)
     alignment: R, M
     separation: border-left
     content: Current lap time, monospaced

   - id: position_indicator
     role: secondary
     size_rank: 3
     position: BR (85%, 80%)
     alignment: R, B
     separation: outline
     content: Race position (P1, P2, etc.)

5) TYPOGRAPHY SYSTEM
   - Title: bold, condensed, uppercase, rank 1, center
   - Labels: regular, normal, rank 3, uppercase, left
   - Data: mono, decimal-aligned, rank 2

6) TEXTURE & EFFECTS
   - Intensity: 1
   - Sources: subtle vignette, minimal glow on hero
   - Glow type: controlled

7) MOTION SCRIPT
   - Transitions: panels 220ms ease-out from left
   - Paths: numbers count-up 300ms linear from 0
   - Loops: 1px scanline pulse every 2s

8) CONTRAST & ACCENTS
   - Overall contrast: high
   - Accent usage: sparse
   - Accent targets: lap time delta highlight when faster

9) QA CHECKLIST
   [x] All elements named and ordered
   [x] Hero = driver_name (largest, centered, shadowed)
   [x] Min rank 3; adequate spacing
   [x] No flashes; scanline <3Hz
   [x] Summary included

10) SUMMARY
    Premium broadcast telemetry card. Center: driver name in large bold uppercase, the focal point. Right: current lap time in monospace. Bottom right: race position badge. Dark background with subtle vignette. Panels slide from left at 220ms. Numbers count up on reveal. Minimal decoration, maximum clarity. Accent highlights on faster lap deltas.

</design_brief>
```

---

## Workflow

1. **Pick a style preset** or define custom dials
2. **Set the six dials** (0–5) to match intent
3. **Map the layout** with zones and coordinates
4. **Define each element** with role, rank, position, separation
5. **Specify typography** by role and parameters
6. **Add texture and motion** with intensity and timing
7. **Run QA checklist** — revise until all pass
8. **Hand off** with structured brief

---

## Anti-Patterns (NEVER)

- Vague descriptions without coordinates or ranks
- Motion without timing specifications
- Elements without explicit positions
- Hierarchy without measurable justification
- Generic fonts (Inter, Roboto, Arial)
- Purple gradients on white (AI cliché)
- Texture without intensity rating
- Accents without defined targets

---

This toolkit means you can set, review, and art-direct complex racing/tech visuals entirely through numeric dials, roles, coordinates, and structured language.

**Bold vision. Precise specification. Consistent execution.**
