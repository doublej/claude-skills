# Troubleshooting

Work the list in order. Most "mod is broken" reports are one of the first three.

## Mod does not appear in the car list

1. **Wrong folder.** It goes in `%USERPROFILE%\Saved Games\ACE\mods\`. Not the Steam directory, not
   `content\cars`, not Documents. Create `mods\` if it is missing.
2. **Nested folder.** Archives usually extract to `SomeCar-v1.2\SomeCar\...`. The folder containing
   the actual mod data must sit directly under `mods\` — copy the *inner* folder, not the wrapper.
3. **Antivirus ate it.** Security software silently quarantines mod files. Kunos recommends adding
   the Steam folders and `Saved Games\ACE` as exceptions. Check the quarantine log before
   re-downloading.
4. **Incomplete extraction.** Verify the archive fully extracted, no zero-byte files.
5. **Stale export.** A mod built before EA 0.8.1 may need re-exporting through the SDK.

## Crashes / silent failures

- `%USERPROFILE%\Saved Games\ACE\log.txt` — read it first, it names the failing asset.
- `%USERPROFILE%\Saved Games\ACE\crashdumps\` — for hard crashes.
- Remove mods one at a time to isolate; a malformed mod can take the whole car list down.

## Multiplayer

- Modded cars online require **EA 0.8+**.
- The server does not push content. Every participant needs the byte-identical mod installed
  locally, or they cannot join / see the entry.
- Version mismatch between drivers behaves like a missing mod. Distribute one pinned archive.

## Dedicated server

- Mods live in `%USERPROFILE%\Saved Games\ACE-Server\mods\` (0.8.1+).
- Config lives in the server's `cfg\`: `settings.json`, `event.json`, `eventRules.json`,
  `entrylist.json`, `configuration.json`.
- Config files use **UTF-16 LE**. UTF-8 can appear to work and then fail silently on certain
  characters — a mystery parse error is usually this.
- A mod car must have the SDK-generated JSON from a 0.8.1-or-later export to be usable as server
  content. Re-export old mods.
- `entrylist.json` supports per-entry Steam ID, car model, ballast (kg) and restrictor (%).

## Things that will never work

- Content Manager, Custom Shaders Patch, AC1 apps, AC1 `.kn5`/`.acd` content — different game.
- Track mods — no pipeline exists (see `tracks-and-reverse-engineering.md`).
- Server-side mod downloading.
