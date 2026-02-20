---
name: ascii-art
description: Generate ASCII art text banners, architectural diagrams, flowcharts, and decorative visuals using figlet and pure-text techniques. Use when user asks for ASCII art, text banners, architecture diagrams, flowcharts, system diagrams, network topology, sequence diagrams, tree structures, terminal art, or box-drawing.
---

# ASCII Art

Generate text banners with `figlet`, hand-craft box art, and compose decorative terminal visuals.

## Figlet Text Banners

```bash
figlet -f <font> "text"
```

### Recommended fonts by use case

| Use case | Font | Example command |
|----------|------|-----------------|
| Default / clean | `standard` | `figlet "Hello"` |
| Bold headers | `big` | `figlet -f big "Title"` |
| Retro terminal | `banner` | `figlet -f banner "RETRO"` |
| Slim / compact | `small` | `figlet -f small "Compact"` |
| Shadow effect | `shadow` | `figlet -f shadow "Shadow"` |
| Blocky | `block` | `figlet -f block "Block"` |
| Slanted | `slant` | `figlet -f slant "Slant"` |
| Doom game style | `doom` | `figlet -f doom "DOOM"` |
| Script / cursive | `script` | `figlet -f script "Fancy"` |
| Isometric 3D | `isometric1` | `figlet -f isometric1 "3D"` |
| Pixel / digital | `digital` | `figlet -f digital "PIXEL"` |
| Star Wars crawl | `starwars` | `figlet -f starwars "WARS"` |
| Speed / motion | `speed` | `figlet -f speed "FAST"` |
| Graffiti | `graffiti` | `figlet -f graffiti "URBAN"` |

### Figlet options

| Flag | Purpose | Example |
|------|---------|---------|
| `-w <cols>` | Set output width | `figlet -w 120 "Wide"` |
| `-c` | Centre output | `figlet -c "Centred"` |
| `-r` | Right-justify | `figlet -r "Right"` |
| `-k` | Kerning (no smushing) | `figlet -k "Spaced"` |
| `-W` | Full width (no overlap) | `figlet -W "Full"` |

List all fonts: `ls /opt/homebrew/Cellar/figlet/2.2.5/share/figlet/fonts/*.flf | xargs -I{} basename {} .flf | sort`

Preview a font: `figlet -f <font> "Preview"`

## Box Drawing

Use Unicode box-drawing characters for framed text:

```
┌─────────────────────┐
│  Boxed message here  │
└─────────────────────┘

╔═════════════════════╗
║  Double-line frame   ║
╚═════════════════════╝

┏━━━━━━━━━━━━━━━━━━━━━┓
┃  Heavy border frame   ┃
┗━━━━━━━━━━━━━━━━━━━━━┛
```

### Box character reference

| Style | TL | TR | BL | BR | H | V |
|-------|----|----|----|----|---|---|
| Light | `┌` | `┐` | `└` | `┘` | `─` | `│` |
| Heavy | `┏` | `┓` | `┗` | `┛` | `━` | `┃` |
| Double | `╔` | `╗` | `╚` | `╝` | `═` | `║` |
| Rounded | `╭` | `╮` | `╰` | `╯` | `─` | `│` |

## Architectural Diagrams

Hand-craft diagrams using box-drawing characters and ASCII connectors. Align all boxes on a grid; use consistent box widths per row.

### Flowchart / pipeline

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client   │────▶│  API GW   │────▶│  Service  │
└──────────┘     └──────────┘     └─────┬────┘
                                        │
                                   ┌────▼────┐
                                   │   DB     │
                                   └─────────┘
```

### Layered architecture

```
┌─────────────────────────────────────────┐
│              Presentation               │
├─────────────────────────────────────────┤
│              Application                │
├─────────────────────────────────────────┤
│               Domain                    │
├─────────────────────────────────────────┤
│            Infrastructure               │
└─────────────────────────────────────────┘
```

### Component diagram with bidirectional flow

```
┌────────────┐       ┌────────────┐       ┌────────────┐
│  Frontend   │◀─────▶│  Backend   │◀─────▶│  Database   │
└──────┬─────┘       └──────┬─────┘       └────────────┘
       │                    │
       │    ┌───────────┐   │
       └───▶│  CDN/Cache │◀──┘
            └───────────┘
```

### Microservices / network topology

```
                    ┌───────────┐
                    │  Load     │
                    │  Balancer │
                    └─────┬─────┘
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        ┌──────────┐┌──────────┐┌──────────┐
        │ Service A ││ Service B ││ Service C │
        └─────┬────┘└─────┬────┘└─────┬────┘
              │           │           │
              └───────────┼───────────┘
                          ▼
                    ┌──────────┐
                    │ Message  │
                    │ Queue    │
                    └──────────┘
```

### Sequence diagram

```
 Client          Server          DB
   │                │              │
   │──── GET /api ─▶│              │
   │                │── SELECT ──▶│
   │                │◀── rows ────│
   │◀── 200 JSON ──│              │
   │                │              │
```

### Tree / hierarchy

```
project/
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── utils/
│   │   └── helpers.ts
│   └── index.ts
├── tests/
│   └── app.test.ts
└── package.json
```

### Data flow / pipeline

```
┌────────┐    ┌─────────┐    ┌──────────┐    ┌────────┐
│ Ingest  │──▶│ Transform│──▶│ Validate  │──▶│ Store   │
└────────┘    └─────────┘    └──────────┘    └────────┘
                  │                              │
                  ▼                              ▼
             ┌─────────┐                   ┌────────┐
             │  Logs    │                   │ Notify  │
             └─────────┘                   └────────┘
```

### State machine

```
          start
            │
            ▼
      ┌──────────┐   submit    ┌───────────┐
      │   Draft   │───────────▶│  Pending   │
      └──────────┘             └─────┬─────┘
            ▲                approve │ reject
            │                   ┌────┴────┐
            │                   ▼         ▼
            │            ┌─────────┐┌──────────┐
            └────────────│Approved ││ Rejected  │
              revise     └─────────┘└──────────┘
```

### Connector reference

| Connector | Chars | Use |
|-----------|-------|-----|
| Horizontal arrow | `────▶` `◀────` | Left-right flow |
| Vertical arrow | `│` + `▼` or `▲` | Top-down flow |
| Bidirectional | `◀────▶` `◀─────▶` | Two-way communication |
| Corner down-right | `┌` then `─` | Route a line |
| Corner up-right | `└` then `─` | Route a line |
| Tee down | `┬` | Branch downward from horizontal |
| Tee right | `├` | Branch right from vertical |
| Cross | `┼` | Lines crossing |
| Dashed | `╌╌╌▶` or `- - -▶` | Optional / async flow |

### Diagram construction rules

1. **Grid alignment** — decide column positions first; all boxes in a column share the same x-offset
2. **Consistent sizing** — boxes in the same row should have equal width when possible
3. **Label inside boxes** — centre text, pad with 1 space each side
4. **Arrows between boxes** — use `────▶` for horizontal, `│` + `▼` for vertical
5. **Branching** — use `┬` / `├` tee connectors, never freehand splits
6. **Keep it readable** — max ~100 chars wide; break into sub-diagrams if wider
7. **Annotate arrows** — place short labels above/beside arrows when the relationship isn't obvious

## Pure ASCII Decorative Elements

### Dividers
```
========================================
----------------------------------------
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
****************************************
########################################
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
█████████████████████████████████████████
```

### Arrows and pointers
```
──►  ◄──  ──▶  ◀──  →  ←  ↑  ↓  ⇒  ⇐
```

### Badges / labels
```
【 IMPORTANT 】   〔 NOTE 〕   ⟦ WARNING ⟧
```

## Workflow

1. Determine what the user needs: text banner, diagram, or decorative element
2. **Text banners** → pick figlet font matching the mood, render with `figlet -f <font> "text"`
3. **Diagrams** → identify diagram type (flowchart, layered, sequence, tree, state machine, etc.), sketch the grid layout, then render with box-drawing characters
4. **Decorative** → wrap content with appropriate border characters or dividers
5. Show the result — offer alternatives if requested

## Tips

- Figlet fonts look best in monospace; keep text short to avoid wrapping
- Combine figlet output with box drawing for framed banners
- For diagrams: decide column positions first, then draw boxes, then connect
- Max diagram width ~100 chars; split into sub-diagrams if wider
- Use dashed arrows (`- - -▶` or `╌╌╌▶`) for optional/async flows
- Annotate arrows when the relationship isn't self-evident
