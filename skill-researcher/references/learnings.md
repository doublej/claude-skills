# Skill Research Learnings

Accumulated knowledge from skill research runs. Read this at the start of each research session.

---

## Run: 2026-05-01 - iPhone Mirroring Use

### What Worked
- `gh search repos "iphone mirroring macos"` found Technical-1/iPhone-Mirroring-Auto-Scripts (5⭐) — ONLY direct match for the macOS Sequoia iPhone Mirroring app
- `gh search repos "ios simulator automation"` surfaced 11 alternatives — useful to disambiguate
- Reading READMEs of low-star repos (5⭐, 2⭐) was critical — star count misleading for niche topics

### What Didn't
- mcp.so + smithery.ai both 403'd from WebFetch (auth-gated or anti-bot) — GitHub-only effectively
- "iphone mirroring skill claude", "iphone mirroring mcp", "iphone control applescript" — all empty
- Star-sorted search buried the 5⭐ relevant match under irrelevant high-star repos

### Pattern Updates
- **iPhone Mirroring (macOS app) ≠ iOS Simulator** — distinct platforms/tooling. Disambiguate first.
- iPhone Mirroring requires: AppleScript + cliclick + Accessibility/Screen Recording perms + calibration (window moves/scales)
- iOS Simulator MCPs (martingeidobler/ios-mcp-server) use native HID injection — no AX perms
- For Apple-only consumer features, search "<feature> applescript" and "<feature> macos" alongside skill/mcp queries

### Conclusion
No skill exists for iPhone Mirroring app automation. Only Auto-Scripts (5⭐) provides AppleScript+cliclick+calibration pattern. Building `iphone-mirroring` skill justified — clear gap, proven pattern to wrap.

---

## Run: 2026-04-26 - Monospace Design / Nerd Fonts TUI

### What Worked
- `gh search repos "awesome TUI design"` found cola-runner/awesome-tui-design (7⭐) — 16 DESIGN.md themes from real TUI source code (Claude Code, Lazygit, k9s, btop, Catppuccin, Dracula, etc.)
- Reading the README of niche repos early reveals design intent quickly
- Parallel 3-agent debate converged fast on "extend existing skill, don't create new one"

### What Didn't
- "nerd fonts TUI terminal UI", "monospace terminal design skill claude", "nerd font icon reference claude skill", "terminal typography nerd font icons", "powerline nerd font cli design" — all returned zero GitHub results
- mcp.so/Smithery searches skipped (clear signal from GitHub: no dedicated skill exists anywhere)

### Pattern Updates
- Terminal UI design skill searches: use "TUI design" not "terminal UI design"
- Nerd font glyphs (U+E000–U+F8FF) are distinct from emoji (U+1F300+): PUA range, terminal-targeted, capability-detected
- `monospace-conviction` is the canonical skill to extend for any terminal UI design work
- `awesome-tui-design` is a useful reference corpus for real-world glyph/theme patterns

### Conclusion
No standalone nerd font design skill exists. Correct action: add `<nerd_fonts>` section to `monospace-conviction` covering PUA ranges, capability detection, curated 20-glyph vocabulary, and ASCII fallbacks.

---

## Run: 2025-01-29 - Initial Setup / Three.js Research

### What Worked
- `gh search repos "<topic> skill claude" --sort stars` returns highly relevant results
- Searching for "self-improving" finds meta-skills with reflection patterns
- awesome-* repos are goldmines (ComposioHQ/awesome-claude-skills: 27k⭐)
- Fetching README via `gh api repos/.../readme --jq '.content' | base64 -d` works reliably

### What Didn't
- Direct "threejs skill claude" found nothing - too specific
- "3d claude skill" too broad, mostly portfolios
- "codex skill" returns Dimillian/Skills (1583⭐) which is personal, not reusable

### Pattern Updates
- For graphics/3D, search for related tech: "webgpu", "shader", "glsl" instead of library name
- Self-improving skills to reference:
  - haddock-development/claude-reflect-system (59⭐) - Correction-based learning
  - olliepro/Codex-Reflect-Skill (12⭐) - Session reflection
  - jennyzzt/dgm (1807⭐) - Darwin Gödel Machine self-modification pattern
- Key awesome lists:
  - ComposioHQ/awesome-claude-skills (27,710⭐)
  - travisvn/awesome-claude-skills (6,194⭐)
  - davepoon/buildwithclaude (2,329⭐)

### Notable Finds
- **dgreenheck/webgpu-claude-skill** (290⭐) - Best Three.js skill, focuses on WebGPU+TSL
- **huangserva/skill-prompt-generator** (954⭐) - Has auto-learning capability
- **VibeCodingWithPhil/agentwise** (43⭐) - Self-improving agents with token optimization

---

## Run: 2026-05-14 - Google Ads spending + keyword analysis

### What Worked
- `gh search repos "google ads mcp"` — 15 hits, clear winners by stars: official googleads/google-ads-mcp (501⭐), google-marketing-solutions/google_ads_mcp (203⭐, deprecated), gomarble-ai/google-ads-mcp-server (127⭐, has run_keyword_planner), TrueClicks/google-ads-mcp-js (48⭐, vendor proxy)
- `gh search repos "dataforseo mcp"` surfaced Skobyn/dataforseo-mcp-server (77⭐) — comprehensive SEO/keyword coverage
- `gh search repos "facebook ads mcp"` confirmed gomarble-ai also ships a Facebook Ads MCP (324⭐) — same vendor pattern
- Reading READMEs of top 3 catches deprecation notices (google-marketing-solutions README redirects to official)

### What Didn't
- mcp.so + smithery.ai both blocked (403/429) — same as iPhone Mirroring + Monospace runs. STOP trying these for skill research; GitHub-only is effective.
- `gh search repos "keyword research mcp"` → 0 results
- `gh search repos "ahrefs api mcp"`, `"semrush mcp"` → 0 results. No first-party MCPs for major SEO SaaS.
- `gh search repos "google ads api skill"` → 0 results. No CLAUDE SKILLS exist for Google Ads at all.

### Pattern Updates
- **Vendor-mediated MCPs (gomarble, TrueClicks)** insert their service in OAuth flow — flag as production risk in synthesis.
- **Google Ads developer token approval** is the blocker behind every Ads MCP. Always surface this upfront — user may not have one.
- **DataForSEO** is paid per-call — note cost model when recommending.
- For "ads spending + keyword" combo asks, only gomarble-ai bundles GAQL + Keyword Planner in one MCP.
- For "skill vs MCP" framing: when user asks for skills and only MCPs exist, flag the category drift in the synthesizer — they may want a skill that *wraps* an MCP install/auth flow, not the raw MCP.
- For ad-platform research, also check Facebook/Meta + TikTok MCPs (same vendor patterns likely apply).

### Conclusion
No skill exists. 3 MCPs are credible (official Google Ads, gomarble for Keyword Planner, DataForSEO for SERP/competitor). Synthesizer recommended deferring install unless recurring use case. CSV export from Ads UI is the right default for one-offs.

---

## Search Term Cheatsheet

| Domain | Effective Terms | Avoid |
|--------|-----------------|-------|
| 3D/Graphics | webgpu, shader, glsl, renderer | threejs, 3d, graphics |
| Self-improving | reflect, self-improving, continual learning | auto, smart |
| Skills general | skill claude, skill codex, awesome-* | agent (too broad) |
| Specific libs | Use lib name + claude/codex | Just lib name alone |

---

## Run: 2025-01-29 - Three.js Debate Evaluation

### Debate Results
- **Advocate**: webgpu-claude-skill fills critical gap, WebGPU is Three.js future
- **Critic**: 95% of projects use WebGL, no vanilla skill exists, TSL is experimental
- **Synthesizer**: MEDIUM confidence, adopt for WebGPU but create vanilla skill for gap

### Key Insight
The debate pattern revealed a blind spot: searching for "threejs" skills finds WebGPU-focused tools, but most developers need vanilla WebGL patterns. Future searches should include both renderer types.

### Evaluation Pattern Refinement
For framework/library research, ask:
1. What's the **mainstream** usage pattern? (vanilla Three.js/WebGL)
2. What's the **emerging** pattern? (WebGPU/TSL)
3. Does the skill cover both or just one?

### Action Generated
Create `threejs-webgl` skill covering:
- Scene/camera/renderer fundamentals
- GLTF/FBX loaders
- OrbitControls
- EffectComposer post-processing
- Performance (instancing, LOD, frustum culling)

---

## Run: 2026-02-03 - Documentation Creation & Framework Suggestions

### What Worked
- **Check environment first**: Context7 was already installed as plugin - saved research time
- `gh search repos "documentation mcp server"` highly effective (20 results)
- DevDocs (2021⭐) emerged as clear leader from GitHub search
- Debate pattern identified gap: "concept management" ≠ "documentation lookup"

### What Didn't Work
- `gh search repos "framework suggestions skill"` → 0 results (too specific)
- mcp.so returned 404 errors on search URLs
- Smithery rate-limited (429 error)
- "Concept knowledge mcp" search yielded nothing
- Web directories less reliable than GitHub search

### Pattern Updates
- **Documentation tools** → Search "documentation mcp" not "documentation creation"
- **Concept management** = different category (note-taking/knowledge base tools)
- **Framework suggestions** = documentation lookup tools (Context7, DevDocs pattern)
- **Always verify existing environment** before searching (Context7 was already present)
- Stars matter for trust: DevDocs (2021⭐) vs S3-Docs (7⭐) validation gap

### Key Findings
- **Context7 MCP**: Already installed via plugin, best for version-specific framework docs
- **DevDocs**: 2021⭐, smart crawling (depth 1-5), free, UI-based, MCP-ready
- **Awesome-docs**: 827⭐, meta-resource for building docs (not querying)
- **Gap identified**: Concept management requires separate tool category (Obsidian/Notion MCPs)

### Search Term Effectiveness
| Query | Results | Quality |
|-------|---------|---------|
| "documentation mcp server" | 20 | High ✅ |
| "framework suggestions skill" | 0 | Failed ❌ |
| "concept knowledge mcp" | 0 | Failed ❌ |
| "awesome documentation tools" | 5 | Medium (meta-resources) |
| "technical writing documentation" | 15 | Low (mostly portfolios) |

### Debate Insights
- Advocate correctly identified Context7 as already-installed win
- Critic raised valid concerns about MCP overhead vs browser search
- Synthesizer properly separated "documentation" from "concepts" as different problems
- Confidence scoring (92/100, 88/100) aligned with star counts

### Action Items
- For future "concept" queries, search "knowledge base mcp" or "note-taking mcp"
- Always run environment check before extensive searches
- Prioritize GitHub over web directories (more reliable)

---

## Run: 2026-03-04 - Svelte/SvelteKit Skills Research

### What Worked
- `gh search repos "svelte mcp" --sort stars` found the **official** `sveltejs/ai-tools` (173⭐) immediately
- Exploring repo structure via `gh api repos/.../contents` to find `.claude-plugin`, `plugins/`, `skills/` directories
- Broadening from "svelte skill claude" (0 results) to "svelte mcp" (14 results)
- mcp.so returned 404 (confirmed previous learning); Smithery returned 429 again

### What Didn't Work
- "svelte skill claude" → 0 results (too specific)
- "svelte skill codex" → 0 results
- "sveltekit skill claude" → 0 results
- mcp.so and Smithery continue to be unreliable (404/429)

### Key Findings
- **sveltejs/ai-tools** is the official Svelte AI tooling repo, not just an MCP — it's a full Claude Code plugin ecosystem
- Official repo name is `ai-tools` (not `mcp`), making direct name searches miss it
- Plugin format: `.claude-plugin/marketplace.json` + `plugins/claude/svelte/` containing skills, agents, .mcp.json
- MCP endpoint: `mcp.svelte.dev/mcp` (HTTP transport) with CLI fallback via `npx @sveltejs/mcp`
- Component library MCPs exist (shadcn-svelte: 38⭐, flowbite-svelte: 8⭐) but are niche

### Pattern Updates
- For framework-specific skills, search `<framework> mcp` broadly — official tools may not use "skill" or "claude" in name
- Official orgs (sveltejs, vuejs, etc.) may ship AI tools under unexpected repo names like `ai-tools`
- Claude Code plugin ecosystem is emerging: check for `.claude-plugin` directories in official repos
- Component library MCPs are a pattern: `<component-lib>-mcp` for docs lookup

### Debate Insights
- Advocate: official backing + plugin format makes adoption frictionless
- Critic: autofixer limited (1 rule), remote dependency, Context7 overlap for docs
- Synthesizer: HIGH confidence on official MCP (42/50), fills autofixer gap Context7 can't
- Key tension: remote MCP vs local CLI fallback — recommend both for resilience

---

## Run: 2026-03-24 - Shopify Template Development

### What Worked
- `gh search repos "shopify mcp server" --sort stars` found 20 results immediately
- `gh search repos "awesome shopify" --sort stars` found curated list (1196⭐)
- `gh search repos "shopify liquid theme" --sort stars` found TeamDijon/shopify-rules (8⭐) — only Claude skill in this space
- Exploring Shopify/horizon's .cursor/rules/ revealed 43 high-quality .mdc rules — goldmine for skill creation
- Checking repo contents before README gives quick signal on maturity

### What Didn't Work
- "shopify skill claude" → 0 results
- "shopify skill codex" → 0 results
- "shopify liquid claude" → 0 results
- "shopify theme dawn template" → 0 results (too specific combo)
- mcp.so → 404 (confirmed pattern from previous runs)
- Smithery → 429 rate limit (confirmed pattern)

### Key Findings
- **No mature Shopify template skill exists** — clear gap in the ecosystem
- **Shopify/horizon** is the best source material: 43 official cursor rules covering liquid, sections, schemas, blocks, accessibility, CSS/JS/HTML standards
- **TeamDijon/shopify-rules** has the right idea (AI-consumable rules + skill pipeline) but empty rules index — framework without content
- **Shopify/theme-check** (357⭐) is the official Liquid linter — useful as quality gate script
- **shopify-mcp-server** (15⭐) is Admin API only, no template coverage

### Pattern Updates
- For Shopify template dev, search "shopify liquid theme" not "shopify template"
- Official theme repos (.cursor/rules/) are better source material than community skills
- Cursor .mdc format converts cleanly to SKILL.md references
- "awesome-*" repos confirm ecosystem gaps when no skills/MCPs surface

### Debate Insights
- Advocate: Horizon's 43 rules are the clear foundation — official, comprehensive, battle-tested
- Critic: Empty ecosystem means building from scratch; Horizon rules are theme-specific opinions
- Synthesizer: HIGH confidence on adapting Horizon rules into Claude skill; no reason to build from scratch when official content exists
- Key tension: Horizon rules encode one theme's opinions vs general Liquid best practices — need selective extraction

---

## Run: 2026-03-31 - Home Assistant MCP/Skills

### What Worked
- `gh search repos "home assistant mcp server" --sort stars` found 17 results including clear winner (1842⭐)
- Searching multiple name variants in parallel: "homeassistant mcp", "hass mcp server", "home assistant skill claude"
- Checking for companion repos: ha-mcp README led to homeassistant-ai/skills (211⭐) — pure knowledge pack
- mcp.so returned 403; Smithery returned 403 (both web directories still unreliable)

### What Didn't Work
- "home assistant skill claude" → 0 results
- "home assistant skill codex" → 0 results
- mcp.so and Smithery web directories both 403 (worse than before — was 404/429)

### Key Findings
- **homeassistant-ai/ha-mcp** (1842⭐) is the dominant HA MCP server — 93 tools, OAuth, setup wizard, E2E tests
- **homeassistant-ai/skills** (211⭐) is a companion knowledge pack following agentskills.io standard — bundled inside ha-mcp as MCP resources
- **Coolver/home-assistant-vibecode-agent** (506⭐) has novel 2-module design (agent inside HA + local MCP) with git versioning
- **tevonsb/homeassistant-mcp** (562⭐) is TypeScript-based with SSE, but wrong runtime for Python-native HA ecosystem
- **voska/hass-mcp** (283⭐) is the simpler/focused alternative

### Pattern Updates
- For IoT/smart home MCPs, search both hyphenated and concatenated forms: "home assistant" + "homeassistant" + "hass"
- Companion repos matter: check README for linked skills/knowledge packs
- agentskills.io is an emerging standard for portable AI agent skills — watch for `npx skills add` pattern
- Web directories (mcp.so, Smithery) may be deprecated or rate-limiting harder — GitHub is the reliable source

### Debate Insights
- Advocate: ha-mcp's star count + tool coverage + bundled skills make it the clear winner
- Critic: 93 tools is context bloat; physical-device security risk; suggested building minimal REST wrapper instead
- Synthesizer: Recommended ha-mcp MCP server (78/100) + thin companion skill for safety guardrails
- Key tension: tool count bloat vs completeness — 93 tools is heavy but alternatives cover only 10-20% of HA API

---

## Run: 2026-04-06 - Directus Skill Research

### What Worked
- `gh search repos "directus mcp"` returned 13 results with the official `directus/mcp` (76⭐) findable via the deprecation pointer in `rijkvanzanten/directus-mcp-server` (27⭐)
- Reading the top result's README revealed it was deprecated and pointed to `directus/mcp` as the official successor — saved time vs evaluating each fork
- Direct `gh api repos/directus/mcp` confirmed official status and active maintenance

### What Didn't Work
- "directus skill claude" / "directus skill codex" → 0 results (no skill bundles published)
- mcp.so returned 403 this time (was 404 in past runs — directory continues to degrade)
- Smithery returned 403 (previously 429 — likely harder rate-limiting or geo-blocking)

### Pattern Updates
- **Always check the top result's README for deprecation notices** — they often point to the canonical/official version, saving evaluation cycles
- For CMS/headless tools, search "<name> mcp" not "<name> skill" — vendors ship MCPs, community ships skills
- mcp.so and Smithery directories are unreliable across multiple runs (404, 429, 403) — treat GitHub as primary, web directories as optional supplements

### Key Findings
- **directus/mcp** (76⭐, npm: `@directus/content-mcp`) — official, 20 tools, built-in safety guardrails (no destructive schema ops), system prompt, dynamic prompt collection support
- **awesome-directus** (directus-labs, 630⭐) — meta-resource for ecosystem discovery
- No published Claude/Codex skill bundles exist for Directus — gap for a thin convention-wrapper skill if user wants project-specific patterns on top of the MCP

---

## Run: 2026-04-08 - Ableton Live MCP/Skills

### What Worked
- `gh search repos "ableton mcp" --sort stars` immediately surfaced the dominant repo (ahujasid/ableton-mcp, 2,379⭐)
- Checking the deferred-tools list in the session revealed 40+ AbletonMCP tools already loaded — environment check before searching saved scope creep
- `gh search repos "ableton live api python"` found cylab/AbletonLive-API-Stub (24⭐) — useful as skill reference material
- Comparing tool surface in session vs. ahujasid README identified that the user is running an extended fork (uisato or similar), not the original

### What Didn't Work
- "ableton skill claude" → 0 results (consistent with all framework-specific skill searches)
- "ableton skill codex" → 0 results
- "max for live ai" → 0 results (too narrow)
- Did not query mcp.so/Smithery — pattern from last 4 runs shows 403/404/429, not worth the time

### Key Findings
- **ahujasid/ableton-mcp** (2,379⭐, MIT, active) — canonical, Smithery-installable via `npx -y @smithery/cli install @ahujasid/ableton-mcp --client claude`. Basic feature set: tracks, MIDI clips, transport, instruments, tempo
- **uisato/ableton-mcp-extended** (156⭐, MIT, active) — adds scenes, batch note edits, automation envelopes, browser navigation by URI, normalized parameters, ElevenLabs TTS, XY mouse controller. Tool surface matches what's in the user's session
- **cylab/AbletonLive-API-Stub** (24⭐) — Python stubs of the Live API, ideal as `references/live-api.md` material in a skill
- **chasewhughes/AbletonComposer** (6⭐) — niche, MCP-based composition, low signal

### Pattern Updates
- **DAW/music tooling**: search "<daw> mcp" not "<daw> skill claude". The MCP layer is mature; the skill layer is non-existent across DAWs
- **Tool-surface matching**: when an MCP is already installed in the session, count and categorize the deferred tools to identify which fork/version is active. Saves needing to run install commands or check configs
- **Skill gap signal**: when 4+ consecutive framework searches return 0 skills but rich MCP results, the universal pattern is "MCPs ship, skills don't" — and the value-add for a skill is the knowledge/conventions layer, not the mechanism layer

### Debate Skipped
- Findings were unambiguous (dominant repo, already installed, no competing skills) — no productive tension to surface
- Better use of time was identifying the real gap: an Ableton skill that wraps the MCP with musical knowledge (tool selection guidance, browser path cookbook, composition recipes, Live API reference)

---

## Run: 2026-04-12 - OpenClaw Skill Research

### What Worked
- `gh search repos "openclaw"` + `"openclaw mcp"` + `"openclaw skill claude"` in parallel — immediately surfaced the full ecosystem (canonical repo, awesome list, MCP bridges, bridge skills)
- Disambiguation via parallel `"captain claw"` search — confirmed OpenClaw (AI assistant, 354k⭐) is distinct from pjasicek/OpenClaw (Captain Claw 1997 game remake, 469⭐). Same name, completely different projects.
- Listing `/contents/skills` directly on the canonical repo revealed bundled skills (coding-agent, github, notion, obsidian, canvas, clawhub, apple-notes, etc.) without needing to read READMEs
- Skipped mcp.so/Smithery entirely — pattern from last 5 runs shows 403/404/429 consistently

### What Didn't Work
- None significant — ecosystem is well-indexed by GitHub search

### Key Findings (ecosystem-level)
- **OpenClaw** = TypeScript personal AI assistant, MIT, runs local gateway daemon, multi-channel (WhatsApp/Telegram/Slack/Discord/iMessage/Matrix/…), `openclaw onboard --install-daemon`, Node 24
- **Skills system**: native first-class, not MCP. Install paths: `~/.openclaw/skills/` (global) or `<project>/skills/` (workspace). Priority: workspace > local > bundled. CLI: `clawhub install <slug>`
- **ClawHub** = public skills registry, 13,729 skills as of Feb 2026
- **VoltAgent/awesome-openclaw-skills** (45,587⭐) — curated 5,211 skills; filtered out 4065 spam + 1040 dupes + 851 low-quality + 886 crypto + 373 malicious
- **Bridge skills** (for Claude Code users):
  - `VsevolodUstinov/openclaw-skill-claude-code` — async delegate OpenClaw → Claude Code CLI via nohup + heartbeat + `sessions_send` callback. Max sub = $0 per task. Multiple forks exist.
  - `freema/openclaw-mcp` (136⭐) — reverse direction, MCP exposing OpenClaw → Claude.ai w/ OAuth2
  - `ourmem/omem` (186⭐) — shared memory across OpenClaw + Claude Code + OpenCode

### Pattern Updates
- **Name-collision check**: when a single-word topic returns 2+ high-star repos with radically different descriptions, run a disambiguation query early. Saves writing an answer about the wrong project.
- **Skill ecosystems are multi-format**: OpenClaw skills ≠ Claude Code skills ≠ Codex skills. Different runtimes, different manifests, different install paths. A "skill" match doesn't mean reusable across harnesses — flag this in the recommendation.
- **Registry + awesome-list pattern**: OpenClaw uses ClawHub (registry) + VoltAgent awesome-list (curated) pattern. This mirrors npm/awesome-npm. Watch for this duo as a maturity signal for any skill ecosystem.
- **Bridge skills are the high-value finds** when user's home harness (Claude Code) differs from the researched ecosystem (OpenClaw) — they're the only directly actionable result
- **Top-result description disambiguates fast**: OpenClaw's "Your own personal AI assistant. Any OS. Any Platform. The lobster way. 🦞" immediately ruled out the Captain Claw game interpretation

---

## Run: 2026-04-24 - cmux ecosystem research

### What Worked
- Plain `gh search repos "cmux"` immediately surfaced both meanings (manaflow-ai terminal vs soheilhy Go mux) + skill ecosystem in same query
- `awesome-cmux` (yigitkonur, 33⭐) is the gold-standard ecosystem map — 170+ projects organized by feature dimension AND by agent (Claude Code/Pi/OpenCode). Read this BEFORE searching individual repos
- README-first approach (gh api .../readme) caught architecture diffs between competing skills (using-cmux vs cmux-claude-skills do different things)

### What Didn't
- Skipped mcp.so/Smithery — GitHub already had MCP server (cmuxlayer). For terminal-tooling ecosystems, mcp directories add noise
- Didn't dedupe variants like `cmux-windows`, `cmux-linux`, `wmux` — cross-platform ports are NOT the same as the macOS original

### Pattern Updates
- **Ecosystem with awesome list** → Read awesome list FIRST. Skip parallel debate if taxonomy is already curated by community
- **Name collisions** → cmux has 5+ unrelated projects (Ghostty terminal, Go connection mux, GSM 0710 mux, Cloudera tool, Korean multiplexer). Always check star counts AND descriptions before picking
- **Three-skill rule for cmux ecosystem**: usage skill (using-cmux), layout/session skill (cmux-claude-skills), MCP server (cmuxlayer). Pick based on workflow depth

### Key Findings
- **manaflow-ai/cmux** (15,228⭐) — THE cmux. Ghostty-based macOS terminal for AI agents. `brew install --cask cmux`. Auto-exposes `CMUX_WORKSPACE_ID`, `CMUX_SURFACE_ID`, `CMUX_SOCKET_PATH`
- **hummer98/using-cmux** (33⭐) — Best general skill. Plugin install: `/plugin marketplace add hummer98/using-cmux`. Auto-loads when CMUX_SOCKET_PATH detected
- **sanghun0724/cmux-claude-skills** (20⭐) — Workspace layouts + snapshot/restore + day-start. Complements using-cmux
- **EtanHey/cmuxlayer** (4⭐) — MCP server, 26 tools. `npm install -g cmuxlayer`. Cross-agent (Claude/Codex/Gemini/Cursor)
- **yigitkonur/cmux-claude-pro** — most complete Claude Code plugin (16 hooks, status pills + progress + git metadata)

---

## Run: 2026-04-29 - AEO/GEO (Answer/Generative Engine Optimization)

### What Worked
- `gh search repos "generative engine optimization"` outperformed `"answer engine optimization"` — GEO term has more skill-format hits
- Reading top 3 READMEs in parallel before debate gave concrete substance to weigh
- Debate caught a nuance: 911⭐ skill chain (gtm-engineer-skills) is mostly content-marketing wrappers; only 1/11 sub-skills (`improve-aeo-geo`) is differentiated

### What Didn't
- mcp.so blocked (403), Smithery rate-limited (429) — fall back to GitHub `mcp` query
- Direct "AEO MCP" search returned 0 — too narrow

### Key Findings
- **Auriti-Labs/geo-optimizer-skill** (305⭐) — pip CLI, MCP-ready, Princeton-backed, has SKILL.md. The technical engine.
- **onvoyage-ai/gtm-engineer-skills** (911⭐) — 11-skill Claude Code chain. Vendor selectively, not wholesale.
- **amplifying-ai/awesome-generative-engine-optimization** (331⭐) — best curated index
- **alexpospekhov/searchstack-aeo** (70⭐) — citation monitoring, costs API $$$
- **AutoGEO** (134⭐, ICLR 2026) — academic, requires GPU+conda. Reference findings, don't install.

### Pattern Updates
- For ranking/search optimization domains, the high-star repos are often marketing wrappers. **Read sub-skill READMEs**, not parent README, before recommending.
- "47 research-backed methods" / round-number rubric = tell that some scoring weights are arbitrary. Treat scores as directional.
- AEO/GEO has 4-12 month half-life — pin tools loosely, refresh awesome-list quarterly.
- Princeton GEO (KDD 2024) + AutoGEO (ICLR 2026) are the canonical research anchors. 8-method priority table lifted ~30-115% per method.

### Conclusion
Built single thin orchestrator skill `aeo-geo` (~180-line SKILL.md + 7 references). Wraps `geo-optimizer-skill` CLI as the engine; embeds Princeton 8-method table; provides framework integration snippets (SvelteKit/Astro/Next/Nuxt/Vite); flags citation-monitoring as opt-in (cost concerns).

---

## Run: 2026-04-30 - Airgapped programming / first-try correctness

### What Worked
- Single-keyword `gh search repos airgap` immediately surfaced the entire airgap ecosystem (claude-code-local 2366⭐, zarf 1879⭐, hauler 212⭐) — beat all multi-word phrase queries which returned 0
- Splitting the user request into 3 distinct problem-statements before searching (run-Claude-airgapped vs first-try methodology vs airgap delivery infra) made each subsearch productive
- README-first on the top 2 hits (claude-code-local, zarf) gave enough substance to skip a 3-agent debate
- `gh search repos "preflight check"` returned the gold MCP server — `preflight-dev/preflight` (24-tool prompt-discipline MCP)

### What Didn't
- All multi-word phrase queries returned 0: `"airgapped offline development"`, `"deterministic build offline mirror"`, `"preflight validation dry-run claude skill"`, `"vendored dependencies offline first"`, `"airgap kubernetes registry"`, `"claude skill defensive verification"`, `"deterministic execution skill"`, `"fallback retry circuit breaker"`, `"verify before run plan apply"`
- `"air-gapped"` (with hyphen) returned 0 vs `airgap` (single word) returned 20 — tokenization matters
- mcp.so/Smithery skipped per established pattern (403/429 across last 7 runs)

### Pattern Updates
- **For methodology-style topics** (airgap, first-try, deterministic, fallback): the dedicated Claude skill almost certainly does not exist. Confirm with 2-3 single-keyword queries, then pivot to recommending a custom skill that combines adjacent tools.
- **Single-keyword > multi-word phrase**: `airgap` (20 results) beat every multi-word phrase variant. GitHub repo descriptions are short — phrases rarely match.
- **Three-bucket framing**: when a topic has a tooling layer + a methodology layer + an infra layer, search and present them as separate buckets. Don't conflate.
- **`preflight-dev/preflight` MCP is the closest existing skill-shaped artifact**: built from analyzing 512 real Claude Code sessions; 41% prompts <50 chars, 30-40% tokens wasted on back-and-forth. Worth knowing about for any "first-try correctness" pitch.

### Key Findings
- **Tooling (run Claude Code airgapped)**:
  - `nicedreamzapp/claude-code-local` (2366⭐) — Apple Silicon, MLX, Qwen 3.5/Llama 3.3/Gemma 4. Wi-Fi-OFF demo with `lsof`. Mac only.
  - `delibae/claude-prism` (1332⭐) — Tauri desktop, offline LaTeX (Tectonic) + Python (uv) + 100+ scientific skills bundled. Files local, AI inference still hits API.
  - `zcimon57-svj/claude-code-offline` (0⭐) — Linux x86_64 air-gapped install package
  - `nancheung/cc-releases` (6⭐) — auto-mirror of Claude Code installers w/ SHA256
- **First-try correctness (methodology)**:
  - `preflight-dev/preflight` MCP (4⭐) — prompt triage, cross-service contracts, correction-pattern learning, cost estimator. `claude mcp add preflight -- npx -y preflight-dev-serve`. Built from real session-data analysis.
  - No dedicated Claude skill exists for the methodology layer.
- **Airgap delivery infra**:
  - `zarf-dev/zarf` (1879⭐) — K8s airgap packager, OCI artifacts, cosign-signed, SBOMs
  - `hauler-dev/hauler` (212⭐) — airgap swiss army knife
  - `local-npm/local-npm` (1170⭐) — offline npm mirror
  - `JuliaComputing/DepotDelivery.jl` (32⭐) — Julia standalone depot

### Recommendation
Build new skill `airgap-dev` covering: pre-flight gates, plan-apply pattern, fallback flows, determinism rules (pinned versions, hashed inputs, fixed seeds), dry-run by default. Bundle `preflight-dev/preflight` MCP install + `claude-code-local` link as adjacent tooling. Reference `zarf` declarative pattern.

### Debate Skipped
Findings unambiguous: airgap tooling dominated by claude-code-local + zarf; methodology layer has no canonical skill. Time better spent giving user the three-bucket framework (tooling vs methodology vs infra) than running advocate/critic/synthesizer agents.

---

## Run: 2026-05-07 - Adobe Lightroom Automation

### What Worked
- `gh search repos "adobe lightroom" --sort stars` found the only MCP server (Automaat/lightroom-mcp, 12⭐) at position 18 — it would have been missed by higher-specificity queries
- `gh search repos "lightroom catalog"` found the highest-star adjacent tool (fdenivac/Lightroom-SQL-tools, 41⭐) — useful for read-only analytics angle
- Reading lightroom-mcp README revealed it ships its own CLAUDE.md, strong integration signal

### What Didn't Work
- "lightroom mcp server" → 0 results (name doesn't have "mcp" in it)
- "lightroom skill claude" → 0 results
- "lightroom automation python" → 0 results
- "adobe lightroom sdk" → 0 results
- "awesome lightroom" → preset collections only, no tooling
- mcp.so/Smithery skipped per pattern (would have been 403/429)

### Key Findings
- **Automaat/lightroom-mcp** (12⭐, npm: `@mskalski/lightroom-mcp`) — the ONLY MCP for LR Classic. TypeScript Node server + Lua plugin bridge. 14 tools: search, rate, keyword, import, export, collections, develop presets, copy/set develop settings. `claude mcp add lightroom -- npx -y @mskalski/lightroom-mcp`. MIT, active.
- **Adobe Lightroom Cloud REST API** (AdobeDocs/lightroom-api-docs, 31⭐) — OAuth2, Lightroom CC (cloud), Python bindings incomplete/unmaintained
- **Lightroom Classic Lua SDK** (Jaid/lightroom-sdk-8-examples, 24⭐) — the mechanism lightroom-mcp wraps; useful reference for dev settings keys
- **fdenivac/Lightroom-SQL-tools** (41⭐) — direct SQLite access to .lrcat for read-only analytics; highest-star in space
- **FUTC-Coding/preset-generator** (24⭐) — GPT-4o generates XMP preset files; one-trick but signals demand

### Pattern Updates
- **Creative software MCPs**: search `"adobe <product>"` broadly (not `"<product> mcp"`) — the repo name often doesn't include "mcp". The LR server appears at rank 18 in the broad search.
- **12-star MCP ≠ low quality**: in niche creative software automation, 12⭐ may be the ONLY option. Evaluate on tooling completeness, not just stars.
- **Lua SDK as sub-surface**: when an MCP wraps a Lua/AppleScript SDK, the SDK reference is valuable skill content even though users won't write Lua directly — used for key names, constants, and capability mapping.
- **Two tracks for Adobe tools**: (1) Classic/desktop → Lua SDK via MCP; (2) Cloud/CC → REST API via OAuth2. They're separate architectures.

### Debate Results
- Advocate: adopt lightroom-mcp immediately — production-ready, right tool surface, 80% of repetitive LR workflows covered
- Critic: bus-factor-one maintainer, IPC bridge fragility, setup friction (two components must both be running)
- Synthesizer: build skill wrapper (82% confidence). MCP exposes raw tools; skill adds develop-settings key reference, tool-selection guidance, workflow recipes (cull→rate→export, batch tone), SQL analytics pointer

### Recommendation
Build `lightroom` skill: install + plugin-start checklist, develop-settings key reference, 3-4 batch workflow recipes, SQL analytics pointer. Skip Cloud REST API (OAuth complexity, bindings incomplete).


---

## Run: 2026-05-28 - Domain Drift / Codebase Review

### What Worked
- `gh search repos "architecture drift detection"` was the productive query — surfaced archlint (Claude Code hook), archtest (npm, LLM-writes-rules/grep-enforces), inDriver/architecture-drift-checker (Claude Agent SDK)
- `gh search repos "claude code review skill"` returned 17 repos — confirmed the code-review-skill space is saturated/low-signal (mostly 0⭐ CodeRabbit clones)
- Reading 3 READMEs in one parallel batch gave enough to synthesize without spawning debate agents

### What Didn't
- EMPTY results: "domain drift codebase", "code naming consistency review", "ubiquitous language domain model", "documentation drift code sync", "codebase consistency audit agent" — abstract/semantic phrasings return nothing on GitHub
- Smithery 429'd again; mcp.so had no relevant category — directory sites still effectively unusable (3rd run confirming)

### Pattern Updates
- **"Domain drift" is ambiguous** — splits into (a) ARCHITECTURAL drift (layer/dep boundaries → archlint/archtest) and (b) DOMAIN-LANGUAGE/semantic drift (vocabulary → already covered by user's `ubiquitous-language` skill). Disambiguate first.
- Search CONCRETE mechanism terms ("architecture drift detection", "import boundary"), NOT abstract goals ("consistency audit", "naming review") — GitHub indexes the former.
- Recurring winning pattern across niches: LLM/human authors declarative rules → deterministic checker enforces (no LLM in hot path). archtest + archlint both embody it.
- Always cross-check finds against the user's EXISTING installed skills before recommending — the highest-value output here was "you already own the domain-language half."

### Conclusion
Gap exists only for ARCHITECTURAL drift. Recommend building a small `architecture-drift` skill wrapping the archlint hook pattern (CLAUDE.md `## Architecture` block + import-boundary check), optionally shelling to archtest for CI. Domain-language drift already served by `ubiquitous-language`.

---

## Run: 2026-07-01 - Deep Research skill

### What Worked
- `gh search repos "deep research agent"` (20 hits) + `"deep research mcp server"` + `"deep research claude code"` in parallel cleanly separated the 3 categories: standalone frameworks vs MCP servers vs actual Claude Code skills
- `gh search repos "deep research claude code"` was the ONLY query that surfaced real skill-format artifacts (jamoeight v1/v2) — the generic "agent" query buried them under academic frameworks
- README-first on the 3 skill candidates (DResearch-Skill, jamoeight v2, stock agent) characterized them fast; jamoeight v2 README is itself a research-cited upgrade spec

### What Didn't
- "deep research agent" returns a wall of academic/benchmark repos (Tongyi 19.6k, dzhng 19.2k, MiroThinker, benchmarks) — high stars, but NONE are Claude Code skills. Category drift is severe for this topic.
- "research agent skill claude" → 0 results
- Skipped mcp.so/Smithery per established 403/429 pattern (8th+ run confirming)

### Key Findings
- **User already owns a `deep-research` skill** (installed, `/deep-research`) — always check installed skills first; this reframes the whole task from "find one" to "compare/upgrade".
- **jamoeight/claude-code-deep-research-v2** (2⭐, MIT) — the standout SKILL online. Multi-agent, AggAgent synthesis (+10.3pp deep-research benchmark), 3 auto-selected modes (STANDARD/DISCOVERY/GENERATOR-EVALUATOR), 30 research-cited edits, -85–98% context-token cost via ToolSearch+Code-Exec+compaction. Drop-in `/deep-research`. README doubles as an upgrade spec with 105 citations. v1 baseline = jamoeight/deep-research-claude-code (1⭐, Nov-2025 Anthropic orchestrator-worker pattern).
- **azagreev/DResearch-Skill** (0⭐, MIT, v1.5.0) — mature plugin+skill, 7-phase, cost-first 4-tier tool hierarchy, FactCheck anti-hallucination veto, confidence 1–5 scoring, 247 tests, checkpoint recovery. But Russian-first (reports ru/en). Plugin: `/plugin marketplace add azagreev/DResearch-Skill`.
- **MCP option**: OctagonAI/octagon-deep-research-mcp (91⭐), ssdeanx/deep-research-mcp-server (Gemini, 70⭐), fbettag/openai-deep-research-mcp (7⭐) — mostly paid-API wrappers.
- **Frameworks (NOT skills, reference only)**: Alibaba-NLP/DeepResearch/Tongyi (19.6k⭐), dzhng/deep-research (19.2k⭐, simplest impl), SkyworkAI/DeepResearchAgent (3.5k⭐).
- **Awesome lists**: DavidZWZ/Awesome-Deep-Research (782⭐, ACL 2026), ai-agents-2030/awesome-deep-research-agent (621⭐).

### Pattern Updates
- **"deep research" is a saturated academic term** — 90% of high-star hits are RL-trained agent models / benchmarks, not installable harness skills. Filter by "claude code" to find skills; ignore star count (real skills are all <3⭐).
- **Check installed skills BEFORE researching** (repeat of documentation-run lesson): user had `deep-research` already — the useful output is an upgrade path, not a fresh recommendation.
- **jamoeight v2's README-as-upgrade-spec** is a reusable asset: mine AggAgent synthesis + 3-mode routing to extend any existing deep-research skill rather than replace it.

### Conclusion
No need to install anything — user owns a working skill. Highest-value action is mining jamoeight v2 (AggAgent synthesis, mode routing) + DResearch-Skill (cost-first tiering, FactCheck veto, confidence scoring) as upgrade material for the existing skill.

---

## Run: 2026-07-14 - English Writing / Copywriting Skills

### What Worked
- `gh search repos "copywriting skill" --sort stars` is the single highest-signal query — returned 20 dedicated copywriting skills, most 2026-fresh
- Inspecting `repos/<r>/contents` + first 45 README lines separated legit (multi-skill, references/, quality gates) from thin single-file repos fast
- `gh search repos "writing skill"` surfaces the general-writing tier but is dominated by Chinese academic-paper packages (5k+⭐) — filter by language/description

### What Didn't
- "editing prose skill claude", "technical writing skill claude", "brand voice writing claude skill" — all ZERO results. Compound queries too specific.
- Star count is a weak legitimacy signal here: the 415⭐ top copywriting hit (feichanggege) is Chinese e-commerce; best English one (robpalmer99) had only 11⭐

### Pattern Updates
- Copywriting is a CROWDED niche (Oct 2025 Skills launch spawned dozens). Frameworks cluster around named copywriters: Schwartz/Halbert/Ogilvy/Hormozi/Stefan Georgi (RMBC).
- Two distinct tiers: (1) direct-response/marketing COPYwriting, (2) general PROSE writing (plain-language, anti-AI-slop, creative fiction). Search both; user usually means one.
- Legit English copywriting: robpalmer99/claude-code-copywriting-skills, coleschaffer/dtc-copywriting-skills (RMBC, npm, A/B evidence), igoroliveirg/claude-copy
- Legit English prose: shreyashankar/plain-writing-skill (241⭐, self-revision HTML diff), jalaalrd/anti-ai-slop-writing (201⭐, research-cited banned-word lists), haowjy/creative-writing-skills (321⭐, fiction, CI)
- For "avoid AI slop": jalaalrd repo has the best curated banned-words/phrases/openers lists to mine

---

## Run: 2026-07-27 - Midjourney Prompting

### What Worked
- `gh search repos "midjourney prompt" --sort stars --limit 25` — the ONE productive query. The single real Claude skill (JustinPerea/midjourney-cc-skill, 5⭐) sat at rank ~25, below 24 web-app prompt generators. Do not cap this query at 10-15.
- `gh search repos "midjourney v8" --sort updated` (NOT --sort stars) surfaced the 2026-era artifacts: omelyanchuk2593/ai-prompt-architect, NeonSoung98/image-prompt-patterns. Version-number queries need date sort — every V8 repo is 0-1⭐.
- `gh api repos/<r>/contents/<dir>` on `knowledge/` + `rules/` gave file sizes → instant depth signal (165KB knowledge, 12 rule modules) without reading anything.
- **Cross-checking a candidate's parameter claims against the vendor's live docs caught a hard factual error** (see below). For any fast-moving-API skill, verify 2-3 concrete params before recommending.

### What Didn't
- ZERO results: "midjourney skill claude", "midjourney sref style reference", "image generation prompt skill claude", "nano banana claude skill", "ai image prompting playbook"
- `docs.midjourney.com` 403s to WebFetch (same as mcp.so/Smithery). `updates.midjourney.com/<post>` DOES fetch — use the changelog host, not the docs host.
- Skipped mcp.so/Smithery per the 10-run 403/429 pattern.

### Version reality (July 2026) — the whole story here
- V8.0 alpha 2026-03-17 → V8.1 2026-04-14 (default 2026-06-10) → **V8.2 default 2026-07-24**
- `--hd` real; HD is DEFAULT in V8.1 (2K native, no upscale step; SD ~4s / HD ~12s). AR capped 4:1 in HD.
- `--sref random` is new in V8.1 (different style per draft image). sref drift from V7 fixed.
- `--oref` (Omni Reference) is still **V7-only** — V8 version in training. `--cref` dead since V7.
- `--q 4` is V7-era and **NOT supported on V8.1**. Multi-prompt `::` broke in V7.

### Key Findings
- **JustinPerea/midjourney-cc-skill** (5⭐, MIT, pushed 2026-02-09) — the only genuine Claude Code skill. Excellent architecture: 7-dimension visual analysis → approach choice (prompt-only / sref / style-codes / hybrid) → 7-dimension scoring → gap-driven action decision → pattern extraction into SQLite. 165KB knowledge (v7-parameters 24KB, keyword-effectiveness 45KB w/ Excellent→Counterproductive tiers, learned-patterns 59KB, failure-modes 22KB) from 19 real sessions. **Entirely pre-V8** — knowledge stamped Feb 2026. Needs sqlite-simple + playwright MCPs for the learning/automation tiers; core tier is MCP-free.
- **omelyanchuk2593/ai-prompt-architect** (1⭐, NOASSERTION, single commit 2026-06-23) — only V8-aware skill; 24 files, good taxonomy (anti-patterns, film stocks, SAECS video framework, skin/faces). But NotebookLM-synthesized and **demonstrably wrong**: labels `--q 4` a "New quality level for V8.1". Mine the taxonomy, trust no parameter.
- **NeonSoung98/image-prompt-patterns** (0⭐, **no license**, 2026-06-10) — 25KB `references/midjourney-v8.md` + 126 real GPT-Image-2 cases + 5 prompt-school structures. Chinese-first. Unlicensed → reference only, cannot vendor.
- **Midgard-Public/Midgard-Theory-Of-Layer-Separated-Midjourney-Prompting** (114⭐) — highest-star *methodology* repo but built on `::X` multiprompts, which V7 killed. Dead.
- MCPs are all third-party paid-API relays (runapi-ai/midjourney-mcp 0⭐, Lala-0x3f/mj-mcp 10⭐, EvoLink). No official MJ API. erictik/midjourney-api (1870⭐) = unofficial Discord client.
- Best web references for skill-building: blakecrosley.com/guides/midjourney (V8.1 guide), ud.hk V8.1 practitioner guide, updates.midjourney.com changelog.

### Pattern Updates
- **Consumer-creative-tool prompting = 0 stars everywhere.** Ignore star count entirely; rank by (a) does it name the CURRENT model version, (b) is there a license, (c) file sizes in knowledge/references.
- **Star-sorted search actively hides skills in this niche** — prompt-generator web apps from 2023 accumulated 100-500⭐ and bury 2026 skills. Always run a `--sort updated` pass on version-numbered queries.
- **Vendor-doc-verify step is now mandatory** for any skill wrapping a fast-moving product API. One live-doc check invalidated the only V8-era candidate's parameter table.
- **Distilled-docs skills rot on a ~3-month clock here** (MJ shipped 3 minor versions in 4 months). Any MJ skill must cite `updates.midjourney.com` and treat its own parameter file as cache, not truth.
- JJ's `design-art-seed` covers the upstream half (data → philosophy → motif → brief) and explicitly hands off at the MJ boundary. The gap is MJ-native syntax/parameters/iteration — a downstream skill, not an overlap.

### Debate Skipped
Replaced by direct file inspection + live vendor-doc verification. Only one candidate had real depth, and the decisive fact (V7-only vs V8.2 current) was a verifiable date, not a judgment call — an advocate/critic pair would have argued over metadata while missing it.

### Conclusion
Build `image-midjourney` (or extend nothing — no local overlap). Vendor JustinPerea's *architecture* (7-dim analysis, scoring, gap→action table, approach selection) and his keyword-effectiveness tiering method; rewrite the parameter layer from scratch against V8.2. Skip the SQLite learning tier unless JJ wants cross-session compounding; skip playwright automation (MJ web UI selectors rot). Cite updates.midjourney.com as the freshness anchor.

---

## Run: 2026-07-28 - Humor / Comedy Skills

### What Worked
- `gh search repos "humor skill" --sort updated` — the ONLY query that found the flagship (caicai688/humor.skill, 7⭐). `--sort stars` returned it nowhere; star-sort surfaces joke DATASETS and dad-joke CLIs instead.
- `gh search repos "standup comedy" --sort updated` found all 3 real craft skills. Every one is 0-2⭐.
- **Grepping the awesome-lists directly** (`gh api repos/<r>/readme | base64 -d | grep -iE "humor|comed|joke"`) proved the gap in one shot: ZERO humor entries across ComposioHQ (71k⭐), travisvn (14k⭐), BehiSecc (9.8k⭐). Faster and more conclusive than any repo query.
- License check as a separate `gh api repos/<r> --jq '.license.spdx_id'` pass — 2 of 3 candidates are unlicensed, which decides vendor-vs-reference before reading a line.

### What Didn't
- ZERO results: "humor skill claude", "comedy skill claude", "joke skill claude", "humor claude code", "comedy writing claude", "satire skill", "roast skill claude", "witty writing skill", "improv comedy ai", "comedy writer agent", "funny writing style prompt"
- Chinese-term queries `"脱口秀 skill"` / `"幽默 skill"` → 0. GitHub does NOT index CJK repo descriptions for these terms — the Chinese skills are only findable via ENGLISH queries ("humor skill", "standup comedy"). Do not bother with CJK search strings.
- Bare `humor` / `comedy` are junk queries: `comedy` top hit is a Node.js actor framework; `humor` top hits are lolcommits, a CVPR pose-estimation paper named HuMoR, and joke datasets. Name collisions are severe.
- Skipped mcp.so/Smithery (11th+ run confirming 403/429).

### Key Findings
- **caicai688/humor.skill** (7⭐, v3.0, **NO LICENSE**, 2026-07-25) — only "make the AI itself funny" persona skill. 254k words transcribed from real Chinese performances, 9 acts (李诞/徐志胜/郭德纲/…), 4 genres. refs: 脱口秀 13KB, 相声 6.7KB, **sketch 32KB**, 综艺即兴 5.9KB, 通用喜剧原理 10KB. Two genuinely reusable mechanisms: (1) **humor-density adaptation table** (chat=heavy → coding=light → user-anxious=off), (2) **safety-word hard switch** (`认真点` kills humor, highest priority above all layers). Targets `~/.workbuddy/skills/`, not Claude Code.
- **717281250-lgtm/standup-comedy-writing** (1⭐, **NO LICENSE**, Codex skill, 2026-06-29) — best-structured craft skill, English SKILL.md. 8 chapters (~3KB each), patterns.md, cheatsheet.md, glossary.md, agents/. Sources: Greg Dean joke system, Judy Carter drills, 李诞脱口秀工作手册, 单立人《单口喜剧表演手册 V1.1》. Explicit "workshop, not joke vending machine" stance; mines the user's own material first.
- **kioup2008/standup-comedy-skill** (0⭐, **MIT** ✅) — only vendorable one. 6 named techniques (personality contrast, environment mismatch, expectation violation, callback, detail stacking, social observation), RIA-TV++ format, `test-prompts.json` per skill, 36 test cases / 83% pass. Thin but licensed.
- **Research anchors**: sail-sg/CLoT (324⭐, CVPR'24 Leap-of-Thought creative humor generation), orionw/rJokesData (550k rated jokes, LREC'20), ROC-HCI/UR-FUNNY (multimodal humor), Moradnejad/ColBERT (200k humor-detection).
- **Ecosystem gap confirmed**: no English-language comedy-craft skill exists anywhere.

### Pattern Updates
- **Awesome-list grep is the fastest gap test.** For "does a skill exist for X", grep the top 3 awesome-claude-skills READMEs BEFORE running repo queries. Zero hits across 95k combined stars = real gap, no further search needed.
- **CJK-authored skills are English-discoverable only.** The Chinese comedy skills all carry English repo names/topics; searching in Chinese finds nothing. Same likely applies to other CJK-dominated niches.
- **Humor is a 2026 Chinese-ecosystem niche.** All 3 craft skills are Chinese-first (脱口秀 boom). English side is empty. Distillation pipelines (cangjie-skill → RIA-TV++, darwin-skill evolution, nuwa-skill) are a Chinese meta-skill ecosystem worth knowing — they auto-distill skills from books/videos.
- **Persona-humor ≠ craft-humor.** Two distinct product shapes: (a) make the assistant funny in every reply (humor.skill, JJ's drunk-claude), (b) help the USER write jokes (standup-comedy-*). Disambiguate before recommending — they share almost no content.
- The **safety-word hard switch** is a transferable pattern for ANY persona skill: a single highest-priority keyword that overrides every other layer. JJ's drunk-claude has intensity but no kill switch.

### Debate Skipped
Replaced by direct file inspection + license verification + awesome-list gap proof. Only 3 candidates, all inspected at file level; the deciding facts (language, license, persona-vs-craft) are verifiable attributes, not judgment calls.

### Conclusion
Real gap for English comedy craft. JJ owns `drunk-claude` (persona/ideation: intensity 0.0-1.0, 5 moods, 8 techniques) — that covers the persona half, NOT joke construction. Recommend building `write-humor` (fits write-* family alongside write-deslop, write-social): vendor kioup2008's 6 techniques (MIT), mine 717281250's chapter structure + Greg Dean/Judy Carter mechanics, lift humor.skill's density table + safety-word switch as the governance layer.

---

## Run: 2026-08-02 - Autonomy skills / "short prompt, no process explanation"

### What Worked
- The domain has a NAME as of 2026: **"loop engineering"**. Searching `agent loop claude code` and `"claude code overnight"` was 10x more productive than any query containing "autonomous".
- `gh search repos "claude code overnight"` was the single best query — surfaced loop-maker, NightShift, designing-loops, Ship-loop in one shot even though none has "overnight" as its primary framing.
- `gh search repos "ralph-skill"` (bare repo-name-shaped query) surfaced the whole Ralph-loop skill family (ralph-vault-skill 69⭐, sensei 53⭐, loopgen 24⭐, ralph-zero 11⭐) that no topical query found.
- Awesome-list grep (`grep -iE "autonom|autopilot|unattended|ralph|overnight|loop"`) over ComposioHQ + travisvn READMEs returned ~4 weak hits → confirmed the awesome lists have NOT caught up with the loop-engineering wave. Do not trust awesome-list absence as a gap signal for topics <6 months old.

### What Didn't
- ZERO results: "yolo mode claude code", "self-directed agent skill claude", "prompt expansion skill claude", "intent clarification agent skill", "vague prompt agent", "requirements elicitation claude skill", "brainstorm plan implement skill", "superpowers claude skills", "autonomous skill claude", "agent autonomy skill"
- `"autonomous claude code"` returns orchestration PLATFORMS (fleet dashboards, Discord bridges, container swarms), not skills. Category drift is severe — filter hard.
- Bare `"superpowers claude skills"` → 0 despite obra/superpowers having 265k⭐. Search the org/repo name directly (`gh api repos/obra/superpowers`) when you already know it exists.

### Key Findings
- **cobusgreyling/loop-engineering** (9,760⭐, MIT, active daily) — the canonical corpus. npm front door `npx @cobusgreyling/loop init . --pattern <p> --tool claude`, "Loop Ready" score, 7 skills (loop-triage, loop-verifier, loop-budget, loop-constraints, budget-negotiator, minimal-fix, install-loop), 8 patterns (pr-babysitter, ci-sweeper, daily-triage, issue-triage, dependency-sweeper, post-merge-cleanup, changelog-drafter), per-tool starters for claude/codex/opencode. Endorsed by Addy Osmani.
- **jbrazy480/loop-maker** (25⭐, MIT) — closest match to "short prompt, full process". Type `loop` + plain English → scans repo first, drafts mission prompt, scores **Mission Strength /10**, asks max 3 questions ONE at a time, "just send it" escape hatch, emits Mission Card + launch line. Generates MISSION.md, feature_list.json (`"passes": false` per feature), loop/PROGRESS.md honesty buckets, AGENTS.md.
- **pro-vi/loopgen** (24⭐, **NO LICENSE**) — "prompt compiler". `/loopgen "<intent>"` → classifies loop archetype, resolves stall-decisions up front, writes `.loop/<id>/{PROMPT,STATE,PRESSURE}.md` (+ FRONTIER.json/CANDIDATES.jsonl for benchmark track), hands back ONE `/goal` line. Purest expression of "quick prompt, no process explanation".
- **edwluo/designing-loops** (7⭐, MIT) — smallest, best-reasoned. 4-type taxonomy (turn/goal/time/proactive) from the Claude Code team's *Getting started with loops*. Rules: write the stop condition first, dual stop (success OR bounded failure), guard against goal redefinition, runbook file for heavy tier, audit the loop's own final report. Knows when to say "that's not a loop".
- **GodModeAI2025/NightShift** (13⭐, Apache-2.0) — 4-layer safety architecture around `--dangerously-skip-permissions`: runbook-as-external-memory + PreToolUse destructive-command blocker + PostToolUse heartbeat + SessionStart(compact) "re-read the runbook" injection + Stop-hook autonomy reminder. The best documented answer to "why does unattended Claude die after ~20 min".
- **obra/superpowers** (264,956⭐, MIT) — 14 skills; `using-superpowers` enforces skill-invocation BEFORE any response including clarifying questions; `brainstorming` runs before plan mode. This is the "don't explain the process, the skill knows it" pattern at ecosystem scale.
- **valkor-ai/loom** (711⭐, Apache-2.0) — Rust MCP runtime + Python algorithms delivery harness, context routing, cross-agent.
- **SantanderAI/ralph-vault-skill** (69⭐, Apache-2.0) — enterprise-grade: tiered knowledge vault as the loop's knowledge source. Deterministic CLI (`scripts/gv.py`, stdlib only) + FIXED immutable prompts in `assets/prompts/`. Best example of the "deterministic script owns everything mechanical, prompts own only the writing" split.
- **spboyer/sensei** (53⭐, MIT) — Ralph loop applied to SKILL.md frontmatter compliance. Directly relevant to a skills repo.
- Others: jasontang-ai/ralph-zero (11⭐, NOASSERTION), vercel-labs/ralph-loop-agent (823⭐, AI SDK not Claude Code), dev1928/governed-agent-autonomy-skills (0⭐, enterprise governance), TheBitcoinBreakdown-95/claude-relay-autopilot (0⭐, /autopilot watched + /relay headless).

### Pattern Updates
- **"Loop engineering" is the 2026 term of art** for this whole space (Ralph loop → loop engineering). Any future autonomy/unattended/overnight query should lead with it.
- **Three distinct product shapes — disambiguate before recommending**: (a) *prompt compilers* that turn a one-liner into a full run contract (loopgen, loop-maker), (b) *loop-design advisors* that pick loop type + stop conditions (designing-loops, loop-triage), (c) *safety harnesses* for unattended execution (NightShift hooks, AgentManager, devforensics). Users asking for "autonomous" usually want (a); they need (c) to not get burned.
- **Universal convergent design across every credible repo**: spec/mission file + verifier that is NOT the writer + provable stop condition + external-memory runbook surviving compaction + decision log instead of asking questions. Five elements, independently reinvented — treat as the reference architecture.
- **Star counts are meaningless in this niche except at the extremes** — the best-reasoned skill (designing-loops) has 7⭐; the 9,760⭐ leader is a corpus/CLI, not a skill.
- **License check matters here**: loopgen (the best-fitting artifact) is UNLICENSED → reference only, cannot vendor.

### Conclusion
Claude Code already ships `/loop` + `/schedule` natively (both installed for JJ). The ecosystem gap is the *front end*: nothing installed turns a one-line intent into a run contract. Recommend building a `loop-brief` / `agent-autopilot` skill that vendors designing-loops' taxonomy + stop-condition rules (MIT), loop-maker's Mission-Strength scoring + "just send it" escape + max-3-questions protocol (MIT), and NightShift's 4-layer hook safety (Apache-2.0). Mine loopgen's archetype classification as reference only (no license).

### Debate Skipped
Replaced by direct README + contents + license inspection on 9 candidates. Deciding facts (license, harness target, product shape) are verifiable attributes, not judgment calls.

---

## Run: 2026-08-19 - macOS permissions (TCC)

### What Worked
- `gh search repos "macos permissions" --sort stars` AND `--sort updated` — the two sorts return almost disjoint sets here. Stars → Swift/Tauri SDK wrappers; updated → the 2026 Claude-Code-adjacent junk. Run both.
- `gh search repos "privacy preferences policy control"` — the ONLY query that found the enterprise half (jamf/PPPC-Utility 873⭐, rtrouton profiles 93⭐, usnistgov/macos_security 2447⭐). "PPPC" spelled out is the MDM world's term of art; "TCC" is the hacker world's.
- Probing the actual machine beat any repo read: `csrutil status`, `sqlite3 ~/Library/Application Support/com.apple.TCC/TCC.db ".schema access"`, service histograms. Settled feasibility in 3 commands.
- Awesome-list grep (ComposioHQ/travisvn/BehiSecc) → ZERO macOS-TCC entries. Confirmed gap.

### What Didn't
- ZERO results: "macos permissions skill claude", "macos tcc mcp server", "macos permissions mcp server", "TCC macos", "screen recording permission macos", "accessibility permission macos swift", "TCC.db reverse engineering". GitHub's search drops multi-word queries hard — 2-word queries only.
- **Severe name collision**: "macos permission" now overwhelmingly means *Claude Code's own tool-approval dialog* (claude-permission-popup 15⭐, LazyClaude, dialog-code, codex-permission-popup, allow-clicker). Filter these out first or the whole result set is noise.
- Skipped mcp.so/Smithery (403/429 pattern, 12+ runs).

### Key Findings
- **Apple's `/usr/bin/tccutil` is reset-only** — `tccutil reset SERVICE [BUNDLE_ID]`. No grant, no list, no query. Every "grant it programmatically" tool is a TCC.db write and needs SIP off.
- **JJ's machine: SIP is DISABLED** and both TCC.db files are readable (user 660 rows, system 163 rows) → direct grant/revoke is actually feasible here, unlike a stock Mac. Do not generalize this to a shipped skill without a SIP guard.
- macOS 26.6 schema confirmed: `access(service, client, client_type, auth_value, auth_reason, auth_version, csreq, policy_id, indirect_object_identifier, flags, last_modified, pid, boot_uuid, last_reminded)`. PK = (service, client, client_type, indirect_object_identifier). `auth_value`: 0=denied, 2=allowed. `client_type`: 0=bundle id, 1=absolute path.
- **DB split matters**: Accessibility / ScreenCapture / SystemPolicyAllFiles / PostEvent / ListenEvent / DeveloperTool live in the SYSTEM db (`/Library/…`, needs sudo). AppleEvents, Microphone, Camera, folder-scoped SystemPolicy*, Photos, AddressBook live in the USER db (`~/Library/…`, no sudo).
- Repos: jacobsalmela/tccutil (545⭐, **GPL-2.0** — viral, do not vendor into MIT skill; SIP off required, `--user` flag for user db), DocSystem/tccutil (72⭐, **no license**), jslegendre/tccplus (284⭐, MIT, **archived 2024**), MacPaw/PermissionsKit (312⭐, MIT, active — Swift/ObjC preflight+request incl. Full Disk Access), ayangweb/tauri-plugin-macos-permissions (173⭐, MIT).
- Enterprise/no-SIP-off path: **jamf/PPPC-Utility** (873⭐, MIT, active) builds PPPC configuration profiles; rtrouton/privacy_preferences_control_profiles (93⭐) is the ready-made profile library; usnistgov/macos_security (2447⭐) the compliance baseline. Profiles CANNOT grant Accessibility/ScreenCapture without MDM supervision — only Automation/AppleEvents + Full Disk Access are MDM-grantable.
- **No MCP server anywhere exposes TCC state.** steipete/macos-automator-mcp (869⭐, MIT, active) explicitly documents "the server cannot grant these permissions itself" and maps error codes -1743 / -10004. That doc is the best prior art for the diagnosis half.

### Pattern Updates
- **Two vocabularies, two ecosystems**: search BOTH "TCC" (hacker/red-team/CLI) and "PPPC" (Mac-admin/MDM). Neither query finds the other's repos.
- **Agent-facing permission tooling is a genuine 2026 gap** — every artifact is either an app-developer SDK (check-and-prompt inside your own app) or an MDM profile builder. Nothing answers "I am an agent in a terminal, which grants do I have and how do I fix the missing one".
- For any macOS-system-state question, probe the live machine before reading repos. Three sqlite/csrutil commands settled what 6 searches could not.

### Debate Skipped
Replaced by direct repo metadata + license inspection + live-machine verification. Deciding facts (license, archived, reset-only vs grant, SIP requirement, which db) are all verifiable attributes.

### Conclusion
Real gap. JJ already owns the domain knowledge scattered across `iphone-mirroring/references/permissions.md` (best single artifact: grant table, smoke tests, failure-mode table), `codex-launch` (Accessibility), `ghostty` (global keybind Accessibility). Recommend consolidating into `macos-permissions` in the planned `macos-*` family (NAMING.md line 125): sqlite-backed audit of both TCC.dbs → per-binary/bundle grant report → runnable smoke tests → repair path (tccutil reset + System Settings URL scheme, and direct db write ONLY behind an explicit `csrutil status` check). Vendor nothing GPL; mine steipete's error-code table (MIT) and MacPaw's preflight API list (MIT).
