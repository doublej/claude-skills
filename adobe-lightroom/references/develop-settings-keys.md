# Develop Settings — SDK Key Reference

Used by `set_develop_settings` (single photo, key→value object) and the optional `settings` whitelist of `copy_develop_settings` (array of key strings).

Source: Adobe Lightroom Classic SDK 8.0 (`Jaid/lightroom-sdk-8-examples`) and Lightroom develop preset XMP attributes (`crs:` namespace stripped).

## Process version

The `2012` suffix marks Process Version 2012 (Lightroom 4+). Modern process versions are PV2012, PV4 (LR Classic 7.4+), PV5 (LR Classic 11+). Legacy (un-suffixed) tone keys silently no-op on PV2012+.

| Key | Type | Notes |
|---|---|---|
| `ProcessVersion` | string | `"6.7"` (PV2012), `"11.0"` (PV4), `"15.4"` (PV5). Read-only in practice — apply via preset. |

## Basic panel

| Key | Range | Notes |
|---|---|---|
| `WhiteBalance` | enum string | `"As Shot"`, `"Auto"`, `"Daylight"`, `"Cloudy"`, `"Shade"`, `"Tungsten"`, `"Fluorescent"`, `"Flash"`, `"Custom"` |
| `Temperature` | 2000 … 50000 | Kelvin. Setting forces `WhiteBalance: "Custom"`. |
| `Tint` | -150 … +150 | Green ↔ Magenta. Setting forces `WhiteBalance: "Custom"`. |
| `Exposure2012` | -5.0 … +5.0 | Stops (float). |
| `Contrast2012` | -100 … +100 | |
| `Highlights2012` | -100 … +100 | |
| `Shadows2012` | -100 … +100 | |
| `Whites2012` | -100 … +100 | |
| `Blacks2012` | -100 … +100 | |
| `Texture` | -100 … +100 | LR Classic 8.4+ |
| `Clarity2012` | -100 … +100 | |
| `Dehaze` | -100 … +100 | |
| `Vibrance` | -100 … +100 | **No `2012` suffix.** |
| `Saturation` | -100 … +100 | **No `2012` suffix.** |

## Tone curve

Curves are stored as point arrays. Easier to apply via preset than to script directly.

| Key | Type | Notes |
|---|---|---|
| `ParametricShadows` | -100 … +100 | |
| `ParametricDarks` | -100 … +100 | |
| `ParametricLights` | -100 … +100 | |
| `ParametricHighlights` | -100 … +100 | |
| `ParametricShadowSplit` | 0 … 100 | Default 25. |
| `ParametricMidtoneSplit` | 0 … 100 | Default 50. |
| `ParametricHighlightSplit` | 0 … 100 | Default 75. |
| `ToneCurveName2012` | string | `"Linear"`, `"Medium Contrast"`, `"Strong Contrast"`, `"Custom"` |
| `ToneCurvePV2012` | array | Point-pair flat array `{x1,y1,x2,y2,...}` |
| `ToneCurvePV2012Red` | array | Per-channel curves |
| `ToneCurvePV2012Green` | array | |
| `ToneCurvePV2012Blue` | array | |

## HSL / Color (per-channel)

Each channel × hue/saturation/luminance triple. Channels: `Red`, `Orange`, `Yellow`, `Green`, `Aqua`, `Blue`, `Purple`, `Magenta`.

Pattern: `Hue<Channel>`, `Saturation<Channel>`, `Luminance<Channel>` — each -100…+100.

Examples:
- `HueRed`, `SaturationRed`, `LuminanceRed`
- `HueOrange`, `SaturationOrange`, `LuminanceOrange`
- … through `LuminanceMagenta` (24 keys total)

Black & white mix uses `GrayMixer<Channel>` instead, same 8 channels:
- `GrayMixerRed`, `GrayMixerOrange`, … `GrayMixerMagenta`

`ConvertToGrayscale` (boolean) toggles B&W mode.

## Color grading (PV4+)

Replaces the older Split Toning panel.

| Key | Range | Notes |
|---|---|---|
| `ColorGradeShadowHue` | 0 … 360 | |
| `ColorGradeShadowSat` | 0 … 100 | |
| `ColorGradeShadowLum` | -100 … +100 | |
| `ColorGradeMidtoneHue` | 0 … 360 | |
| `ColorGradeMidtoneSat` | 0 … 100 | |
| `ColorGradeMidtoneLum` | -100 … +100 | |
| `ColorGradeHighlightHue` | 0 … 360 | |
| `ColorGradeHighlightSat` | 0 … 100 | |
| `ColorGradeHighlightLum` | -100 … +100 | |
| `ColorGradeGlobalHue` | 0 … 360 | |
| `ColorGradeGlobalSat` | 0 … 100 | |
| `ColorGradeGlobalLum` | -100 … +100 | |
| `ColorGradeBlending` | 0 … 100 | Shadow↔Highlight blend |
| `ColorGradeBalance` | -100 … +100 | |

Legacy split toning (PV2012):
- `SplitToningShadowHue`, `SplitToningShadowSaturation`, `SplitToningHighlightHue`, `SplitToningHighlightSaturation`, `SplitToningBalance`

## Detail (sharpening + noise reduction)

| Key | Range | Notes |
|---|---|---|
| `Sharpness` | 0 … 150 | |
| `SharpenRadius` | 0.5 … 3.0 | |
| `SharpenDetail` | 0 … 100 | |
| `SharpenEdgeMasking` | 0 … 100 | |
| `LuminanceSmoothing` | 0 … 100 | Luma noise reduction amount |
| `LuminanceNoiseReductionDetail` | 0 … 100 | |
| `LuminanceNoiseReductionContrast` | 0 … 100 | |
| `ColorNoiseReduction` | 0 … 100 | |
| `ColorNoiseReductionDetail` | 0 … 100 | |
| `ColorNoiseReductionSmoothness` | 0 … 100 | |

AI denoise (LR Classic 12.3+) is not a settable key — it generates a new DNG and is invoked via Lightroom UI / LrEnhance, not the develop settings dictionary.

## Lens corrections

| Key | Type | Notes |
|---|---|---|
| `LensProfileEnable` | 0 / 1 | |
| `LensProfileSetup` | string | `"LensDefaults"`, `"Auto"`, `"Custom"` |
| `LensProfileName` | string | Profile name (e.g. `"Adobe (Canon RF 24-70mm F2.8 L IS USM)"`) |
| `LensProfileDistortionScale` | 0 … 200 | |
| `LensProfileVignettingScale` | 0 … 200 | |
| `AutoLateralCA` | 0 / 1 | Remove chromatic aberration |
| `DefringePurpleAmount` | 0 … 20 | |
| `DefringePurpleHueLo` | 0 … 100 | |
| `DefringePurpleHueHi` | 0 … 100 | |
| `DefringeGreenAmount` | 0 … 20 | |
| `DefringeGreenHueLo` | 0 … 100 | |
| `DefringeGreenHueHi` | 0 … 100 | |
| `DistortionCorrection` | -100 … +100 | Manual distortion |
| `PerspectiveVertical` | -100 … +100 | |
| `PerspectiveHorizontal` | -100 … +100 | |
| `PerspectiveRotate` | -10 … +10 | |
| `PerspectiveScale` | 50 … 150 | |
| `PerspectiveAspect` | -100 … +100 | |
| `PerspectiveX` | -100 … +100 | |
| `PerspectiveY` | -100 … +100 | |
| `PerspectiveUpright` | 0 … 5 | 0=Off, 1=Auto, 2=Level, 3=Vertical, 4=Full, 5=Guided |

## Transform / crop

| Key | Range | Notes |
|---|---|---|
| `CropTop` | 0.0 … 1.0 | Normalized to image |
| `CropLeft` | 0.0 … 1.0 | |
| `CropBottom` | 0.0 … 1.0 | |
| `CropRight` | 0.0 … 1.0 | |
| `CropAngle` | -45 … +45 | Degrees |
| `CropConstrainToWarp` | 0 / 1 | |

## Effects (post-crop vignette + grain)

| Key | Range | Notes |
|---|---|---|
| `PostCropVignetteAmount` | -100 … +100 | |
| `PostCropVignetteMidpoint` | 0 … 100 | |
| `PostCropVignetteFeather` | 0 … 100 | |
| `PostCropVignetteRoundness` | -100 … +100 | |
| `PostCropVignetteStyle` | 1 / 2 / 3 | 1=Highlight Priority, 2=Color Priority, 3=Paint Overlay |
| `PostCropVignetteHighlightContrast` | 0 … 100 | |
| `GrainAmount` | 0 … 100 | |
| `GrainSize` | 0 … 100 | |
| `GrainFrequency` | 0 … 100 | |

## Calibration (camera profile)

| Key | Type | Notes |
|---|---|---|
| `CameraProfile` | string | Profile name. Common: `"Adobe Color"`, `"Adobe Standard"`, `"Adobe Landscape"`, `"Adobe Portrait"`, `"Adobe Vivid"`, `"Adobe Neutral"`, `"Adobe Monochrome"`. Camera-specific profiles (e.g. `"Camera Standard"`) require the camera maker's data. |
| `ShadowTint` | -100 … +100 | |
| `RedHue` | -100 … +100 | |
| `RedSaturation` | -100 … +100 | |
| `GreenHue` | -100 … +100 | |
| `GreenSaturation` | -100 … +100 | |
| `BlueHue` | -100 … +100 | |
| `BlueSaturation` | -100 … +100 | |

## Local adjustments

Masks (radial/linear/brush/AI subject/AI sky) are stored as nested structures, not flat keys. **Do not write them via `set_develop_settings`** — apply via preset or copy from a reference photo with `copy_develop_settings`.

## Common traps

- `Vibrance` and `Saturation` are **not** suffixed `2012`. Don't add the suffix.
- `Exposure2012` is in stops as a float (e.g. `0.5`, `-0.33`), not a 0-100 slider scalar.
- Booleans in develop settings are `0` / `1` integers, not Lua booleans.
- Setting any `Crop*` key requires updating all four edges to keep the rectangle valid.
- HSL channel keys are unsuffixed (`HueRed`, not `HueRed2012`).
- `ToneCurveName2012` only takes effect when `ToneCurvePV2012` is also a curve consistent with the named preset.
- White balance: prefer setting `WhiteBalance` as a string preset where possible. Setting `Temperature` / `Tint` numerically silently switches it to `"Custom"`.

## Discovery via metadata

To inspect what keys a photo currently uses:
```
get_photo_metadata(photo_id)
```
Returns develop settings as a dictionary. Useful before `copy_develop_settings` to confirm what will be carried over.
