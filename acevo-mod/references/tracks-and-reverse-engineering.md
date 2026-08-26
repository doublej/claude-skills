# Tracks, and looking inside the game

## Tracks: the honest answer

**Kunos ships no track editor** — the ACE SDK is a car editor, track tools are roadmapped and
undated as of EA 0.8.1 (August 2026). **But the track format itself is fully open**, and the
community authors tracks through it. Both halves matter; don't quote only the first.

Verified hands-on 2026-08-09 against the 0.8.1 install: every track file type is protobuf whose
schema is embedded in `AssettoCorsaEVO.exe`, and `ac-evo-data-tools` round-trips all 5 204 shipped
track files byte-exact. **EvoForge** (Patreon, Jésus Triste) converts AC1 tracks into EVO on top of
this. So "no pipeline" is wrong; "no official editor" is right.

### The track format

A track is a directory under `content\tracks\<name>\`:

| Path | Message / format | What it is |
|---|---|---|
| `<name>.track` | `TrackData` | tiny manifest — dynamic-track grip model, track centre, extent |
| `<name>.scene` + `containers\*.scene` | `SceneData` | the world: a flat `repeated SceneActorData` |
| `layouts\<layout>.scene` | `SceneData` | per-layout actor overlay (barriers etc.) |
| `layouts\*.track_layout` | in-house binary | track edges — `acevo_layout.py` |
| `layouts\*.aisplinedata` | `AISplineData` | AI racing line + pitlane |
| `layouts\*.trackcontrolpoints` | `TrackControlPoints` | sectors / corner definitions |
| `containers\<layout>.splinedata.json` | `SplineData` as **plain JSON** | the road centreline — position + rotation per node (~1.85 m spacing), plus road markers |
| `static_meshes\**\*.mesh` | `MeshData` | geometry: positions, normals, texcoords, tangents, indices, LODs, per-batch material |
| `materials\*.material` | `MaterialData` | shading |
| `terrain\`, `textures\`, `irradiance_volumes\`, `reflection_captures\`, `shadow_cache\` | | baked support data |

`SceneActorData` = name, guid, transform, bounds, tags + one `ActorData` oneof. The oneof is the
whole track vocabulary: `static_mesh`, `instanced_static_mesh`, `spline`, `surfaces`, `track_info`,
`track_layout`, `starting_position`, `zones`, `terrainnew`, `reflection_probe`,
`irradiance_volume`, decals, `light`, `camera`, `marshal`, `particle_emitter`, `traffic_vehicle`.

Key messages (all in `Scene.proto` unless noted):

- `SplineData.Node` — transform + anchors + `markers`. A `SplineData.Road` marker carries
  per-side `Widths` / `Elevations` / `Materials` for 11 lateral strips (inner shoulder, inner turn,
  lane1-3, outer turn, outer shoulder, gutter, sidewall, side, clearing) plus camber and
  `RoadPhysicsSurface`. **The road is generated from the spline** — you author a centreline and a
  cross-section, not road polygons.
- `SurfaceDefinitionData` (`LogicScene.proto`) — `surfaceId` → grip, damping, vibration, wear,
  rain friction, `SurfaceType` (Asphalt / Kerb / Grass / Sand / Flat_Kerb / ExtraTurf).
  `StaticMeshData.surface_id` binds a mesh to one.
- `SceneTrackInfo` — display name, `SceneTrackTypeEnum`, real-world coordinates, timezone.
- `StartingPositionData` — grid / pit / box / POI slots.
- `ZoneData` — pitlane entry/exit, pitboxes, grid, safety-car lines, and the open-world POI types.
- `MeshData` / `MeshLodData` (`Mesh.proto`) — raw vertex arrays. `ImportSettings.importPaths`
  shows Kunos' own editor imports FBX into `.mesh`; you can write `.mesh` directly instead.

### Conventions, verified against 0.8.1 content

Don't guess these — each was measured from shipped files.

- **Handedness.** Same as glTF: counter-clockwise front faces, right-handed.
  `cross(e1, e2) · normal > 0` on 880/880 triangles of
  `brands_hatch/static_meshes/pole_single2_kslayer3.mesh`. glTF geometry passes
  through unchanged.
- **Meshes store world coordinates.** Shipped `.mesh` bounds are absolute track
  positions and their actors carry identity transforms. Baking placements into
  vertices is a valid authoring strategy.
- **`TransformData.rotation` means two different things.** Spline nodes store a
  **unit direction vector** — `|rotation| = 1.0000` at every sampled monza node,
  equal to `normalize(node[i] - node[i+1])`, i.e. pointing back along node order.
  Actors instead look like **Euler degrees**: brands_hatch grid slots ramp from
  0.19 to 1.77 across the start straight, sane as ~1° of yaw and absurd as radians.
- **Materials.** The general-purpose type is `materialType: "UberBiplanarMaterial"`
  (`DynamicTrack` for the racing surface). Resources are looked up **by name, not
  slot** — every shipped `slot` is 0. A base colour map needs both the resource
  (`Base_BaseColorMap`, legacy alias `txDiffuse`) and the float flags
  `Base_HasBaseColorMap = 1.0` / `ksHasBaseColorMap = 1.0`; without them the
  shader samples nothing.
- **`MeshLodData`** carries flat float arrays, 4 floats per vertex for `tangents`
  and `colors`, one `MeshBatch` per material with the material as a
  `content\tracks\...` path. `materialId` is empty in practice.
- **`ActorBounds` is a 2D XZ footprint** (`Vector2Data`), not a box.
- **Textures are a `.texture` + `.texturemips` pair, and the layout is
  self-describing.** `.texture` is a `TextureMetadata` protobuf (`Renderer.proto`)
  carrying `tilingInfo` — tile size in texels, per-mip tile count and starting
  tile index, and a row pitch per tile. Tiles are the DX12 64 KB standard shape
  (256x256 at 8 bpp/BC7, 128x128 at 32 bpp), each mip starts on a tile boundary,
  rows inside a tile are linear. brands_hatch/fences2 (BC7 512x1024, 11 mips) is
  counts `[8,2,1,1,1,1,1,1,1,1,1]`, offsets `[0,8,10,...,18]`, 19 x 65536 bytes
  exactly. **`PixelFormat_R8G8B8A8UNormSrgb` is in the enum**, so authoring
  textures needs no BC7 encoder — write uncompressed and set
  `conversionSettings.compress = false`.

### Authoring path

1. Dump the schemas from your own exe (below), giving `acevo.desc`.
2. Extract a shipped track and read it as JSON — that is the spec.
3. Write geometry as `.mesh`, road as a `SplineData` centreline + road markers, physics as
   `SurfaceDefinitionData`, grid as `StartingPositionData`, and assemble a `SceneData`.
4. Encode with `acevo_pb.py encode` (byte-exact round-trip is the correctness check).
5. Load loose via the run-unpacked trick for iteration.

Open question, still unverified: whether the game will load a **new** track directory rather than
overriding an existing one, and whether it survives multiplayer content checks. Test single-player
loose-file first.

### Rules that still hold

- **Don't ship overrides of an official track.** Replacing a shipped track's assets breaks
  multiplayer content checks and is invalidated by every patch. Author a new track directory.
- Redistribution rules below still apply to anything extracted.

## Reading shipped content: kspkg

Game assets ship in **KSPackage** archives — `content.kspkg` is the main one.

### Format

- Payload = linear binary blobs, optionally XOR'd with key `0x9F9721A97D1135C1`.
- A fixed **file table** is appended after the blobs, then zero padding to EOF.
- Entries are `0x100` bytes each: path (`0xE0` bytes), alignment, info flags (directory / XOR'd),
  path length (u16), path hash (u64), size (u64), offset (u64).
- Most of the content *inside* is **protobuf**, and the full schemas are embedded in the exe —
  `extract_protos.py` recovers 90 `.proto` files / 2 115 messages, no `protodump` needed.

**Two things changed since the 2025-era write-ups** (verified 0.8.1, Steam build 24331595):

- The file table is **`0x4000000` (64 MB), not `0x2000000`** — capacity `0x40000` entries
  (120 696 used). Seeking `-0x2000000` from EOF lands in the trailing zero padding and yields an
  empty listing. Seek `size - 0x4000000`.
- The stored path hash is **no longer FNV1a-64 of the lowercased path**, so hash lookup for
  single-file extraction fails. Scan `file_path` instead.

### Tools

| Tool | Language | Notes |
|---|---|---|
| `Breakalien/ac-evo-data-tools` | Python | **the one that matters.** `extract_protos.py` pulls the schemas from the exe; `acevo_pb.py` decode/encode byte-exact; `acevo_decode.py` named JSON; `acevo_spline.py`, `acevo_layout.py`; web UI |
| `Nenkai/ACEvo.Package` | C# (.NET 10) | list / extract-all / extract-single by game path |
| `ntpopgetdope/ace-kspkg` | Python | `parse_kspkg.py --list`, `--all --run-unpacked`, `--path ...` — needs the two 0.8.1 patches above |
| `dSyncro/acevo-content-editor` | — | quick unpack utility |
| `sa413x/kspkg-viewer` | C++ | ImGui/DX11 GUI: browse, preview, extract and modify `.kspkg` without the CLI. Dormant since Feb 2025 (v0.4.0) — predates the 0.8.1 file-table change |
| `dSyncro/acevo-shared-memory` | — | live telemetry: speed, gear, RPM, tyre state, G-forces, ERS, damage |

```bash
python tools/extract_protos.py "<install>/AssettoCorsaEVO.exe" -o proto -d proto/acevo.desc
python tools/acevo_decode.py decode <file> -o out.json    # read
python tools/acevo_pb.py encode out.json -o <file>        # write, byte-exact
```

### Run-unpacked trick

Dumping the package contents to the game root and renaming the `.kspkg` makes the game load loose
files instead of the archive. Useful for inspection and debugging. Do this on a copy, expect patches
to break it, and never ship it.

### Rules

- Inspecting the format to learn it: fine.
- Redistributing extracted Kunos or licensed third-party assets: not fine. Kunos and Digital Bros
  disclaim responsibility for community content that infringes trademarks or brand policy — that
  disclaimer is a warning, not a permission.
