---
name: acevo-mod
description: Modding Assetto Corsa EVO (AC EVO / ACE) — official Car Editor SDK pipeline, mod install paths, dedicated-server mod setup, track-mod status, and reverse-engineering shipped content from kspkg packages. Use for AC EVO car mods, liveries, the ACE SDK, "Saved Games\ACE\mods", kspkg extraction, or when someone asks how to make/install AC EVO tracks and cars. NOT for original Assetto Corsa (AC1) / Content Manager / CSP — that is a different, incompatible pipeline.
---

# Assetto Corsa EVO modding

AC EVO is a **different game and a different pipeline** from Assetto Corsa (2014). Almost every
tutorial on the internet is AC1. Applying AC1 knowledge here is the #1 source of wasted afternoons.

<state>
Verified 2026-08-09. AC EVO is in Steam Early Access (appid 3058630, Windows-only), so this moves.

| Capability | Status |
|---|---|
| Car creation/editing | **Official** — ACE SDK "Car Editor", shipped in EA 0.7 (3 Jun 2026) |
| Custom liveries | Docs + templates published; full livery tooling still expanding |
| Modded cars in multiplayer | **Yes**, since EA 0.8 (9 Jul 2026) |
| Server-side mod cars | Yes, since 0.8.1 — `Saved Games\ACE-Server` |
| Track creation — official editor | **Not available.** Confirmed on roadmap, unscheduled |
| Track creation — via the file format | **Possible.** Schemas embedded in the exe, all shipped track files round-trip byte-exact (verified 0.8.1). See the tracks reference |
| Decorations / full circuits | No editor; authorable as `SceneData` actors |
| Third-party graphics ext. (a CSP equivalent) | Does not exist |

**Tracks — the AC1 library does NOT carry over.** Classic Assetto Corsa (AC1, 2014) has thousands
of community tracks built in ksEditor as `.kn5` and installed through Content Manager. **None of
them work in EVO.** Different engine, different format (protobuf inside `.kspkg`), no compatibility
layer, no drop-in path. If someone points at a large library of community "Assetto Corsa" tracks,
those are AC1 — assume AC1 until proven otherwise. EVO's own track scene is a handful of hand-built
or converted tracks (OverTake's ACE Tracks category was in single digits as of Aug 2026), and
converting an AC1 track (EvoForge) is a rebuild into EVO's format, not compatibility. Say this
before answering any "can I get track X in EVO" question — it is the single most common wrong
assumption about this game.

**Re-verify before answering version-sensitive questions** — fetch
<https://assettocorsa.gg/news/> or the Steam news feed for the current EA version and check
whether track tools have shipped. If the answer changed, say so instead of quoting this table.
</state>

<paths>
Windows paths. Everything user-facing lives in `Saved Games`, **not** in the Steam folder.

| What | Where |
|---|---|
| Installed mods (single player) | `%USERPROFILE%\Saved Games\ACE\mods\<mod-folder>` |
| Installed mods (dedicated server) | `%USERPROFILE%\Saved Games\ACE-Server\mods\` |
| Log | `%USERPROFILE%\Saved Games\ACE\log.txt` |
| Crash dumps | `%USERPROFILE%\Saved Games\ACE\crashdumps\` |
| Server config | server `cfg\` — `settings.json`, `event.json`, `eventRules.json`, `entrylist.json`, `configuration.json` |
| Game content archive | `<steam>\steamapps\common\...\content.kspkg` |
| The SDK itself | Steam → Library → **Tools** → ACE SDK (free with the game) |

If `mods\` does not exist, create it.
</paths>

<routing>
Read only the reference you need.

- Building or editing a car, installing/using the SDK, liveries, audio, physics, testing
  → `references/car-pipeline.md`
- Tracks, or inspecting/extracting shipped game content, kspkg tooling, telemetry
  → `references/tracks-and-reverse-engineering.md`
- Mod not showing up, crashes, multiplayer/server problems
  → `references/troubleshooting.md`
</routing>

<hard_rules>
1. **Never give AC1 instructions for EVO.** No `content\cars\` in the Steam directory, no Content
   Manager, no Custom Shaders Patch, no `data.acd`, no `ui_car.json`, no ksEditor. Those are AC1.
   If a source says to drop a car into `steamapps\common\...\content\cars`, that source is wrong
   about EVO.
2. **Do not invent SDK specifics.** The authoritative material is the ACE SDK documentation thread
   and its sample project (links in `references/car-pipeline.md`). When asked for exact export
   settings, dummy/hierarchy naming, material slots, or scale, point at the sample project rather
   than transferring AC1 numbers (0.01 scale, "FBX 2014/2015 only", etc. — those are AC1 lore and
   unverified for EVO).
3. **Tracks: no official editor, but the format is open.** Don't answer "impossible" — the track
   file format is fully recovered and round-trips byte-exact. Read the tracks reference and answer
   from the actual message definitions; don't improvise field names.
4. **Don't help redistribute Kunos assets.** Extracting shipped content to learn the format is
   fine; repackaging Kunos or third-party licensed models/liveries as a "mod" is not. Kunos
   explicitly disclaims responsibility for community content that infringes trademarks.
5. State the EA version a claim is tied to. "As of 0.8.1" beats an undated assertion.
</hard_rules>

<sources>
Official
- SDK documentation thread (Car / Driver / Sample / Livery drives, plus Audio, Physics and Generic
  discussion sub-threads): <https://www.assettocorsa.net/forum/index.php?threads/ace-sdk-documentation.83772/>
- Release notes: <https://assettocorsa.gg/> · Steam news for appid 3058630

Community
- Tooling: `Nenkai/ACEvo.Package`, `ntpopgetdope/ace-kspkg`, `dSyncro/acevo-content-editor`,
  `dSyncro/acevo-shared-memory`
- Mod hosting: OverTake.gg (AC EVO category), Modland
- Treat SEO mod-aggregator sites as unreliable — several still publish AC1 install instructions
  under an AC EVO headline.
- **These block WebFetch (HTTP 403): `overtake.gg`, `modland.net`, `assettocorsamods.net`,
  `patreon.com`.** Don't burn tool calls fetching them directly — use WebSearch snippets, or go to
  the GitHub repos above, which do fetch.
</sources>
