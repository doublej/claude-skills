# Car pipeline — the official ACE SDK

## Getting the SDK

Steam → Library → filter **Tools** → the ACE SDK entry. Free with ownership of AC EVO.
Shipped with EA 0.7 (3 June 2026) as the "AC EVO Car Editor — first official release".

Kunos ships it as an *internal-grade* tool: the same production pipeline the studio uses, aimed at
"experienced and technically skilled users". It is not a click-to-mod app.

## Official documentation

One forum thread is the hub — read it before anything else, it is updated as material lands:

<https://www.assettocorsa.net/forum/index.php?threads/ace-sdk-documentation.83772/>

It links four Google Drive folders:

| Folder | Contents |
|---|---|
| **Car** | Car pipeline documentation |
| **Driver** | Driver model/animation documentation |
| **Sample** | Base project, sample FBX files, FMOD script — **the ground truth for naming, hierarchy, scale and material setup** |
| **Livery** | Livery tutorial and templates |

Also published: rendering debug tools. Dedicated sub-threads exist for **Audio**, **Physics** and
**Generic** SDK discussion — those threads are where Kunos devs answer format questions.

## What the editor does

- PBR material production pipeline (matches the in-game renderer, not AC1's shader set)
- Full LOD management
- Aftermarket components — visual *and* mechanical variants, applied as upgrades on a car
- Add / remove / adjust individual parts on an existing vehicle, or build one from scratch
- Export produces the mod folder that drops into `Saved Games\ACE\mods\`

## Workflow shape

```
3D app (Blender/Max/Maya)  →  FBX  →  ACE SDK Car Editor  →  export  →  Saved Games\ACE\mods\<car>
                                          ↑
                              materials (PBR), LODs, parts/upgrades,
                              physics, audio (FMOD), UI metadata
```

**Do not fill in the blanks from AC1 tutorials.** Dummy naming, hierarchy rules, unit scale, FBX
version, material slot names and physics file formats are all EVO-specific and are defined by the
Sample project. Open the sample, mirror it, and change one thing at a time.

## Physics and audio

- Physics: EVO's car data is not AC1's `data.acd` + `.ini` bundle. Shipped cars carry a
  `content\cars\<car_id>\data\cardata.car` (protobuf-encoded). Author physics through the SDK and
  its documentation, not by hand-editing binary files.
- Audio: FMOD, with an FMOD script provided in the Sample drive folder.

## Liveries

Livery documentation and templates are published in the Livery drive folder. Custom liveries in
multiplayer were still on the roadmap as of 0.8.x — verify current state before promising it.

## Testing a mod

1. Export from the SDK into `%USERPROFILE%\Saved Games\ACE\mods\<mod-folder>`.
2. Launch, pick the car in single player, drive it.
3. On failure, read `Saved Games\ACE\log.txt` first — see `troubleshooting.md`.

## Multiplayer / server distribution

- Modded cars are allowed online since EA 0.8.
- Servers do **not** distribute content. Every driver must already have the identical mod installed
  locally.
- Since 0.8.1 the server loads cars from `Saved Games\ACE-Server`. **Mods exported before 0.8.1
  must be re-exported through the SDK** — the newer export generates a JSON file that server-side
  configuration requires. An old mod folder will not register as valid server content.

## Known rough edges (0.7 era, may be fixed)

- Some UI resources (logos, description text) configured in the editor did not appear in-game.
- Package visibility issues against release builds.

Check the SDK documentation thread's issue list before debugging something that Kunos already knows about.
