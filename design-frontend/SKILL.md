---
name: design-frontend
description: >
  Distinctive, polished web UIs that avoid generic AI aesthetics — builds
  production-grade frontends with bold typography, cohesive color, and
  purposeful motion. Use for any web UI/frontend design or restyling work;
  default choice; for an opinionated creative-director persona with
  interrogation ritual use design-director. Triggers on "design this page,"
  "make it look good," "not so generic," "frontend design," "landing page,"
  "polish this UI."
---

# Frontend Design

Creates distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implements real working code with exceptional attention to aesthetic details and creative choices.

<design_thinking>

**FIRST, check for an existing design system.** If the project already defines one (CSS variables/token files, an established font stack, set color palette, existing motion patterns), discover those constraints first and treat working cohesively within them AS the aesthetic direction — do NOT impose new fonts, palettes, or motion over an existing system. When a project-specific design-system skill already covers this app, prefer it over this skill rather than layering a bold new direction on top. The guidance below applies to greenfield work where you set the direction.

Before coding, understand context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme - brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian
- **Constraints**: Technical requirements (framework, performance, accessibility)
- **Differentiation**: What makes this UNFORGETTABLE?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.
</design_thinking>

<aesthetics_guidelines>

### Typography
Choose fonts that are beautiful, unique, and interesting. Opt for distinctive choices - unexpected, characterful font selections. Pair a distinctive display font with a refined body font.

**RESTRICTED FONTS** (do NOT use these):
- Plus Jakarta Sans (overused geometric)
- Inter (overused body font)
- JetBrains Mono (overused mono font)
- Arial, Roboto, system fonts

### Color & Theme
Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

### Motion
Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.

### Spatial Composition
Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.

### Backgrounds & Visual Details
Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic:
- Gradient meshes
- Noise textures
- Geometric patterns
- Layered transparencies
- Dramatic shadows
- Decorative borders
- Custom cursors
- Grain overlays

## What to AVOID

NEVER use generic AI-generated aesthetics:
- Overused font families (Plus Jakarta Sans, Inter, JetBrains Mono, Roboto, Arial, system fonts)
- Cliched color schemes (purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design lacking context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics.
</aesthetics_guidelines>

<implementation>

Match implementation complexity to the aesthetic vision:
- **Maximalist designs**: Elaborate code with extensive animations and effects
- **Minimalist designs**: Restraint, precision, careful attention to spacing, typography, and subtle details

Elegance comes from executing the vision well.

**File length**: Self-contained HTML demos (single file with inline styles/scripts for portability) are an expected exception to the global 150-line file cap. Keep them as one file and do not split unless the user asks — no need to justify the length.
</implementation>
