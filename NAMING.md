# Skill naming taxonomy

Goal: skills read as a **set**, not a pile. Principle:

> **Prefix where a real family of ≥2 exists and the prefix clarifies. Keep proper-noun
> tools and true singletons as-is.** Prefix = domain/tool. Suffix = specialization.

`family-thing` — the family is the first token, scannable in any alphabetical list.
Hub skills keep the bare family name (`pixijs`, `pdf`, `raycast`, `writer`, `prompt-crafter`).

---

## Families already consistent — KEEP

- `skill-*` — skill-creator, skill-overview, skill-usage-tracker, skill-feedback, skill-feedback-collector, skill-feedback-optimizer
- `raycast-*` — raycast (hub), raycast-extensions, raycast-scripts, raycast-snippets
- `shopify-*` — shopify-api, shopify-data, shopify-template
- `browser-*` — browser-automation, browser-router
- `*-api` (service integrations) — spotify-api, twilio-api, porkbun-api, enablebanking-api
- `claude-md-*` — claude-md-optimizer, claude-md-tree (+ fix below)

---

## Families to create / fix (old → new)

### `code-*` — codebase analysis & quality (anchor family)
| old | new |
|---|---|
| codebase-mapper | code-map |
| repomap-analyzer | code-audit |
| dev-refactor | code-refactor |
| codebase-simplify | code-simplify |
| modularize | code-modularize |
| prop-drilling | code-prop-drilling |
| logging-audit | code-logging |
| ubiquitous-language | code-glossary |
| *(new)* | code-arch-drift ✓ already created |

### `claude-md-*` — CLAUDE.md tooling (fix outlier)
| context-cascade | claude-md-cascade |

### `prompt-*` — prompt engineering (prompt-crafter stays hub)
| xml-prompt | prompt-xml |
| small-model-prompt | prompt-small-model |
| gpt51-prompt | prompt-gpt51 |
| gpt52-prompt | prompt-gpt52 |

### `pixijs-*` — fix the one outlier
| pixi-debug | pixijs-debug |

### `logo-*` — logo/mark generation
| logo-creator | logo-create |
| mathematical-logo-creator | logo-mathematical |
| systematic-logo-design | logo-systematic |

### `design-*` — design direction & systems
| frontend-design | design-frontend |
| tooling-design-system | design-tooling |
| creative-director-unhinged | design-director |
| seed-for-art | design-art-seed |

### `ui-*` — UI quality & patterns
| readable-ui | ui-readable |
| usability-fundamentals | ui-usability |
| mobile-web | ui-mobile |
| animation-easing | ui-animation |

### `xr-*` — VR/XR development (unify, kill the double-vr)
| vr-openxr-dev | xr-openxr-dev |
| vr-quest-vr-client | xr-quest-client |
| steamvr-driver | xr-steamvr-driver |
| *(xr-input-forwarding stays)* | — |

### `stream-*` — real-time media pipeline (remotevr/ALVR)
| low-latency-udp-streaming | stream-udp |
| realtime-audio-streaming | stream-audio |
| nvenc-amf-encoding | stream-encode |
| foveated-encoding | stream-foveated |
| video-decode-pipeline | stream-decode |
| gpu-color-correction | stream-color |

### `pdf-*` — PDF generation/processing (pdf stays hub)
| reportlab-pdf | pdf-reportlab |
| icc-color-pdf | pdf-icc |
| ghostscript | pdf-ghostscript |

### `adobe-*` — Adobe app automation
| lightroom | adobe-lightroom |
| *(adobe-illustrator, adobe-photoshop stay)* | — |

### `cms-*` — headless/content CMS
| directus | cms-directus |
| kirby-cms | cms-kirby |
| payload-cms | cms-payload |
| sheet-cms | cms-sheets |

### `diagram-*` — diagram/visualization generators
| mermaid-graphs | diagram-mermaid |
| erdantic | diagram-erd |
| font-family-tree | diagram-fonts |
| ascii-art | diagram-ascii |

### `term-*` — terminal emulators & multiplexers
| iterm2 | term-iterm2 |
| ghostty | term-ghostty |
| tmux | term-tmux |
| cmux | term-cmux |

### `tui-*` — building terminal UIs
| terminal-kit | tui-kit |
| monospace-conviction | tui-monospace |

### `proc-*` — process management
| process-cleanup | proc-cleanup |
| process-monitor | proc-monitor |

### `mcp-*` — MCP management
| mcpick-plus | mcp-pick |

### `codex-*` — Codex CLI (codex-launch stays)
| codex-generate-image | codex-image |

### `deploy-*` — deployment targets
| nas-deploy | deploy-nas |
| cloudflare | deploy-cloudflare |
| github-pages-generator | deploy-github-pages |

### `macos-*` — macOS native / desktop control
| build-macos-apps | macos-build |
| file-assoc | macos-file-assoc |
| iphone-mirroring | macos-iphone-mirror |
| swift | macos-swift |

### `py-*` — Python libraries
| pydantic-v2 | py-pydantic |
| pywebview | py-webview |

### `write-*` — writing (writer stays hub)
| human-email | write-email |
| social-promotion | write-social |

### `audio-*` — audio (audio-effects stays)
| sam-audio | audio-sam |

---

## Standalone — KEEP (proper nouns, unique tools, no family)

aeo-geo, agent-friendly-cli, agent-orchestrator, blender, chat-archive,
claude-agent-sdk, claude-skill, cookiecutter-templates, doublej-widget, epc-qr,
ezviz-protocol-analyzer, fastapi-docs-upgrade, fbx-interchange, full-optimize,
hiphop-culture, home-assistant, inkscape, justfile, lyric-video-maker, nextjs,
note-refiner, obsidian, ollama-local, openclaw, photoshop-api, pillow-drawing,
prompt-crafter, rename-project, rust-systems, screenshot-pipeline, session-search,
svelteflow, swarm, teams, telegram, theatre-js, threejs, transcript-capture,
tweakpane-builder, umami-tracking, update-scaffold, version-manager, vlc,
voice-assistant, wgpu-graphics, workremotely, writer, pdf, pixijs

---

## Known exceptions & risks

- **swarm / teams / agent-orchestrator** — left standalone. They're invoked by
  name and overlap with `/swarm` `/teams` plugin commands; an `agent-*` prefix
  would collide and break muscle memory. Flag, don't force.
- **photoshop-api** stays `*-api` (not `image-*`) — it's a library binding, fits
  the service-api pattern better.
- **claude-skill** (non-interactive automation mode) has a confusing name but a
  rename changes meaning — left as-is unless you want `claude-headless`.
- Every rename changes its **slash-command** and requires a **symlink refresh**
  (handled by the execution script: remove stale `~/.claude/skills/<old>` +
  `~/.codex/skills/<old>`, re-run install).

---

## Execution status (2026-05-28)

**Executed (conservative subset): 57 renames across 20 families.** All families
above were applied EXCEPT the proper-noun-tool prefixes, which were intentionally
deferred to keep those tools standalone:

- `term-*` — iterm2, ghostty, tmux, cmux stay as-is
- `macos-*` — build-macos-apps, file-assoc, iphone-mirroring, swift stay as-is
- `pdf-ghostscript` — ghostscript stays as-is (reportlab-pdf/icc-color-pdf still moved)
- `py-*` — pydantic-v2, pywebview stay as-is

Symlinks refreshed on Claude (146) and Codex; cross-references and frontmatter
fixed. To resume the deferred families later, apply only those four groups.

## Tally

57 renames executed · 4 families deferred · ~6 already-consistent families untouched.
