# Visual quality → prompt language

Use when analysing a reference image or an intent, to turn "what I see / what I want" into words Midjourney acts on.

<principle>

Realism is assembled from **named physical components**, never from quality adjectives.
"photorealistic, 8k, ultra detailed" produces plastic skin and stock-photo defaults.
`Kodak Portra 400, 85mm f/1.4, overcast north light` produces a photograph.

Four components carry most of the weight: **light setup · film stock or sensor · lens · one concrete physical detail.**

</principle>

<lighting>

| What you see / want | Prompt language |
|---|---|
| Light from behind the subject | backlighting, rim light, silhouette |
| Soft shadows, even fill | soft diffused light, overcast, softbox |
| Hard shadows, crisp edges | harsh directional light, hard key |
| Warm low sun | golden hour, low warm sun, long shadows |
| Cool pre-dawn / dusk | blue hour, cool ambient, moonlight |
| One-sided modelling | side light, Rembrandt lighting, split lighting |
| Visible beams | volumetric light, god rays, haze in the air |
| Artificial glow in scene | practical lights, neon spill, LED glow |
| Flat, shadowless | flat even illumination, shadowless studio, overcast softbox |
| Harsh on-camera flash | direct flash, hard flash falloff, paparazzi flash |

**Dual-tone setups** — always name both colours *and* their directions:

| Look | Fragment |
|---|---|
| Purple + orange | cool purple key from left, warm orange rim from right |
| Cyan + magenta | cyan key, magenta accent, neon aesthetic |
| Blue + gold | cool blue ambient, warm gold highlights |
| Teal + coral | teal key, coral warm accents |
| Restrained | neutral grey lighting, single [colour] rim accent |

</lighting>

<photographic>

Reach for these instead of "cinematic" or "professional".

| Want | Name it |
|---|---|
| Warm forgiving skin | Kodak Portra 400 |
| Saturated punchy colour | Kodak Ektar 100, Fujifilm Velvia |
| Muted documentary | Kodak Gold 200, Fujifilm Superia |
| Grainy high-contrast B&W | Ilford HP5, Tri-X 400 pushed |
| Cool clinical digital | digital medium format, Phase One |
| Vintage instant | Polaroid 600, SX-70 |
| Compressed portrait | 85mm f/1.4, 135mm |
| Natural human view | 35mm, 50mm |
| Environmental, slight distortion | 24mm, 28mm wide |
| Voyeuristic compression | 200mm telephoto |
| Immersive distortion | 14mm ultra-wide, fisheye |

Aperture shorthand: `f/1.4` for shallow separation, `f/8` for everything sharp.

</photographic>

<mood>

| What you feel | Prompt language |
|---|---|
| Calm | serene, tranquil, still |
| Mysterious | enigmatic, shadowed, withholding |
| Intense | charged, confrontational, high tension |
| Dreamlike | ethereal, hazy, dissolving |
| Ominous | foreboding, brooding, oppressive |
| Bright, open | airy, sunlit, buoyant |
| Nostalgic | faded, sun-bleached, remembered |
| Cold and modern | clinical, sterile, institutional |

V7+ handles abstract mood compounds directly — "institutional melancholy", "expensive loneliness" land as written. Use them.

</mood>

<material>

| What you see | Prompt language |
|---|---|
| Light passes through | translucent, transparent, glass-like |
| Glows from inside | subsurface scattering, internal glow |
| Mirror finish | reflective, chrome, mirror polish |
| Non-shiny | matte, unfinished, non-reflective |
| Shiny but not mirror | glossy, satin, polished |
| Rough | textured, coarse, tactile |
| Rainbow sheen | iridescent, oil-slick, holographic |
| Distorts what's behind | refractive, caustics |
| Worn | patina, chipped, weathered, scuffed |

</material>

<composition>

| What you see / want | Prompt language |
|---|---|
| Subject fills the frame | close-up, macro, tight crop |
| Subject small in a large space | wide shot, figure dwarfed by, vast |
| Off-centre | rule of thirds, subject at the left third |
| Camera above | overhead, top-down, bird's eye |
| Camera below | low angle, worm's eye |
| Background falls away | shallow depth of field, bokeh, f/1.4 |
| Everything sharp | deep focus, f/8, sharp throughout |
| Room for type | large empty [colour] area at the top, unbroken sky above the subject |

`negative space` alone is unreliable — MJ reads it as an art term, not a layout instruction. Describe the empty region physically instead.

</composition>

<style>

| What you see | Prompt language |
|---|---|
| A photograph | photograph, 35mm, documentary frame |
| 3D software | 3D render, CGI, clay render |
| Painting | oil painting, gouache, visible brushwork |
| Digital illustration | digital illustration, vector, flat colour |
| Anime | anime, cel shaded (or switch to `--niji 7`) |
| Editorial print | editorial illustration, risograph, screen print |
| Minimal | reduced, two-colour, generous white space |
| Film stills | film still, anamorphic, 2.39:1 |

</style>

<weight_selection>

Choosing `--sw` from what the user actually asked for:

| They said | Start at |
|---|---|
| "match this exactly" | `--sw 400+` |
| "this style, different subject" | `--sw 200–250` |
| "make something like this" | `--sw 250–300` |
| "loosely inspired by this" | `--sw 100–150` |

Balance rule: high `--sw` + short prompt = the reference wins. Low `--sw` + detailed prompt = the words win. Medium `--sw` + detailed prompt = a genuine blend.

Same logic for `--ow` on subjects: 300+ to hold a face, 60–100 for a recognisable person in a new style, under 30 for a hint.

</weight_selection>

<attribution>

Lighting, material, composition, and style tables adapted from JustinPerea/midjourney-cc-skill (MIT), extended with photographic-component and dual-tone material.

</attribution>
