# NIH-plug Framework Guide

NIH-plug is a modern Rust framework for audio plugin development. Memory-safe, no GC pauses, excellent performance.

## Why NIH-plug?

- **Memory Safety**: Rust's ownership model prevents common audio bugs
- **No Runtime Overhead**: Zero-cost abstractions
- **Modern API**: Derive macros, ergonomic parameter handling
- **Multiple GUI Options**: Vizia, Iced, egui, or headless
- **Active Development**: Growing ecosystem

## Setup

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Add required targets (for cross-compilation)
rustup target add x86_64-apple-darwin
rustup target add aarch64-apple-darwin
```

### Project Setup

```bash
cargo new --lib my_plugin
cd my_plugin
```

```toml
# Cargo.toml
[package]
name = "my_plugin"
version = "0.1.0"
edition = "2021"
license = "GPL-3.0-or-later"  # Or your choice

[lib]
crate-type = ["cdylib", "lib"]

[dependencies]
nih_plug = { git = "https://github.com/robbert-vdh/nih-plug.git" }

# Optional: GUI frameworks
# nih_plug_vizia = { git = "https://github.com/robbert-vdh/nih-plug.git" }
# nih_plug_iced = { git = "https://github.com/robbert-vdh/nih-plug.git" }
# nih_plug_egui = { git = "https://github.com/robbert-vdh/nih-plug.git" }

[profile.release]
lto = "thin"
strip = "symbols"

[profile.profiling]
inherits = "release"
debug = true
strip = "none"
```

### Build Commands

```bash
# Build release
cargo build --release

# Build with bundling (creates proper plugin package)
cargo xtask bundle my_plugin --release

# Output locations:
# target/bundled/my_plugin.vst3
# target/bundled/my_plugin.clap
```

### Install xtask for Bundling

```bash
# Add to workspace
cargo install cargo-xtask

# Or add bundler as dev dependency
[dev-dependencies]
nih_plug_xtask = { git = "https://github.com/robbert-vdh/nih-plug.git" }
```

Create `xtask/main.rs`:
```rust
fn main() -> nih_plug_xtask::Result<()> {
    nih_plug_xtask::main()
}
```

## Basic Plugin Structure

```rust
// src/lib.rs
use nih_plug::prelude::*;
use std::sync::Arc;

struct MyPlugin {
    params: Arc<MyParams>,
}

#[derive(Params)]
struct MyParams {
    #[id = "gain"]
    pub gain: FloatParam,
}

impl Default for MyPlugin {
    fn default() -> Self {
        Self {
            params: Arc::new(MyParams::default()),
        }
    }
}

impl Default for MyParams {
    fn default() -> Self {
        Self {
            gain: FloatParam::new(
                "Gain",
                util::db_to_gain(0.0),  // Default: 0 dB
                FloatRange::Skewed {
                    min: util::db_to_gain(-30.0),
                    max: util::db_to_gain(30.0),
                    factor: FloatRange::gain_skew_factor(-30.0, 30.0),
                },
            )
            .with_smoother(SmoothingStyle::Logarithmic(50.0))
            .with_unit(" dB")
            .with_value_to_string(formatters::v2s_f32_gain_to_db(2))
            .with_string_to_value(formatters::s2v_f32_gain_to_db()),
        }
    }
}

impl Plugin for MyPlugin {
    const NAME: &'static str = "My Plugin";
    const VENDOR: &'static str = "Your Name";
    const URL: &'static str = "https://your-website.com";
    const EMAIL: &'static str = "you@email.com";
    const VERSION: &'static str = env!("CARGO_PKG_VERSION");

    const AUDIO_IO_LAYOUTS: &'static [AudioIOLayout] = &[
        AudioIOLayout {
            main_input_channels: NonZeroU32::new(2),
            main_output_channels: NonZeroU32::new(2),
            ..AudioIOLayout::const_default()
        },
    ];

    const MIDI_INPUT: MidiConfig = MidiConfig::None;
    const MIDI_OUTPUT: MidiConfig = MidiConfig::None;

    const SAMPLE_ACCURATE_AUTOMATION: bool = true;

    type SysExMessage = ();
    type BackgroundTask = ();

    fn params(&self) -> Arc<dyn Params> {
        self.params.clone()
    }

    fn initialize(
        &mut self,
        _audio_io_layout: &AudioIOLayout,
        _buffer_config: &BufferConfig,
        _context: &mut impl InitContext<Self>,
    ) -> bool {
        // Called once before processing starts
        // Return false to indicate initialization failure
        true
    }

    fn reset(&mut self) {
        // Called when playback stops or parameters reset
        // Clear delay lines, reset filters, etc.
    }

    fn process(
        &mut self,
        buffer: &mut Buffer,
        _aux: &mut AuxiliaryBuffers,
        _context: &mut impl ProcessContext<Self>,
    ) -> ProcessStatus {
        for channel_samples in buffer.iter_samples() {
            // Get smoothed parameter value
            let gain = self.params.gain.smoothed.next();

            for sample in channel_samples {
                *sample *= gain;
            }
        }

        ProcessStatus::Normal
    }
}

impl ClapPlugin for MyPlugin {
    const CLAP_ID: &'static str = "com.your-domain.my-plugin";
    const CLAP_DESCRIPTION: Option<&'static str> = Some("A gain plugin");
    const CLAP_MANUAL_URL: Option<&'static str> = None;
    const CLAP_SUPPORT_URL: Option<&'static str> = None;
    const CLAP_FEATURES: &'static [ClapFeature] = &[
        ClapFeature::AudioEffect,
        ClapFeature::Stereo,
        ClapFeature::Utility,
    ];
}

impl Vst3Plugin for MyPlugin {
    const VST3_CLASS_ID: [u8; 16] = *b"MyPluginABCDEFGH";  // Unique 16-byte ID
    const VST3_SUBCATEGORIES: &'static [Vst3SubCategory] = &[
        Vst3SubCategory::Fx,
        Vst3SubCategory::Tools,
    ];
}

nih_export_clap!(MyPlugin);
nih_export_vst3!(MyPlugin);
```

## Parameter Types

### FloatParam

```rust
FloatParam::new(
    "Cutoff",
    1000.0,
    FloatRange::Skewed {
        min: 20.0,
        max: 20000.0,
        factor: FloatRange::skew_factor(-2.0),  // Log-like
    },
)
.with_smoother(SmoothingStyle::Logarithmic(50.0))
.with_unit(" Hz")
.with_value_to_string(formatters::v2s_f32_hz_then_khz(2))
.with_string_to_value(formatters::s2v_f32_hz_then_khz())
```

### IntParam

```rust
IntParam::new(
    "Octave",
    0,
    IntRange::Linear { min: -2, max: 2 },
)
```

### BoolParam

```rust
BoolParam::new("Bypass", false)
    .with_value_to_string(formatters::v2s_bool_bypass())
    .with_string_to_value(formatters::s2v_bool_bypass())
```

### EnumParam

```rust
#[derive(Enum, PartialEq)]
enum FilterType {
    #[name = "Low Pass"]
    LowPass,
    #[name = "High Pass"]
    HighPass,
    #[name = "Band Pass"]
    BandPass,
}

EnumParam::new("Filter Type", FilterType::LowPass)
```

### Parameter Ranges

```rust
// Linear range
FloatRange::Linear { min: 0.0, max: 1.0 }

// Skewed (logarithmic-like)
FloatRange::Skewed {
    min: 20.0,
    max: 20000.0,
    factor: FloatRange::skew_factor(-2.0),
}

// Skewed with center point
FloatRange::SymmetricalSkewed {
    min: -24.0,
    max: 24.0,
    factor: FloatRange::skew_factor(-1.0),
    center: 0.0,
}

// Gain (special helper)
FloatRange::Skewed {
    min: util::db_to_gain(-60.0),
    max: util::db_to_gain(12.0),
    factor: FloatRange::gain_skew_factor(-60.0, 12.0),
}
```

### Parameter Smoothing

```rust
// Logarithmic (good for gain, frequency)
.with_smoother(SmoothingStyle::Logarithmic(50.0))  // 50ms

// Linear (good for pan, mix)
.with_smoother(SmoothingStyle::Linear(20.0))  // 20ms

// Exponential
.with_smoother(SmoothingStyle::Exponential(30.0))

// None (for discrete parameters)
.with_smoother(SmoothingStyle::None)
```

## Processing Patterns

### Sample-by-Sample

```rust
fn process(&mut self, buffer: &mut Buffer, ...) -> ProcessStatus {
    for channel_samples in buffer.iter_samples() {
        let gain = self.params.gain.smoothed.next();

        for sample in channel_samples {
            *sample *= gain;
        }
    }
    ProcessStatus::Normal
}
```

### Channel-by-Channel

```rust
fn process(&mut self, buffer: &mut Buffer, ...) -> ProcessStatus {
    for (channel_idx, channel) in buffer.iter_mut().enumerate() {
        for sample in channel {
            *sample = self.process_sample(*sample, channel_idx);
        }
    }
    ProcessStatus::Normal
}
```

### Block Processing

```rust
fn process(&mut self, buffer: &mut Buffer, ...) -> ProcessStatus {
    let num_samples = buffer.samples();

    // Process entire block at once
    for channel in buffer.iter_mut() {
        self.filter.process_block(channel);
    }

    ProcessStatus::Normal
}
```

### SIMD Processing

```rust
use std::simd::f32x4;

fn process(&mut self, buffer: &mut Buffer, ...) -> ProcessStatus {
    for channel in buffer.iter_mut() {
        // Process 4 samples at a time
        let chunks = channel.chunks_exact_mut(4);
        let remainder = chunks.into_remainder();

        for chunk in chunks {
            let samples = f32x4::from_slice(chunk);
            let processed = samples * f32x4::splat(self.gain);
            chunk.copy_from_slice(processed.as_array());
        }

        // Handle remainder
        for sample in remainder {
            *sample *= self.gain;
        }
    }
    ProcessStatus::Normal
}
```

## State Management

### Plugin State

```rust
struct MyPlugin {
    params: Arc<MyParams>,
    // Internal state (not saved)
    filter_state: FilterState,
}

impl MyPlugin {
    fn reset(&mut self) {
        self.filter_state.reset();
    }
}
```

### Persistent State

```rust
#[derive(Params)]
struct MyParams {
    #[persist = "editor-state"]
    editor_state: Arc<ViziaState>,

    #[nested(group = "filter")]
    filter: FilterParams,
}

#[derive(Params)]
struct FilterParams {
    #[id = "cutoff"]
    cutoff: FloatParam,

    #[id = "resonance"]
    resonance: FloatParam,
}
```

## DSP Helpers

### Utility Functions

```rust
use nih_plug::util;

// dB conversions
let gain = util::db_to_gain(-6.0);  // 0.5
let db = util::gain_to_db(0.5);     // -6.0

// Frequency conversions
let midi = util::freq_to_midi_note(440.0);  // 69.0
let freq = util::midi_note_to_freq(69.0);   // 440.0

// Smoothing coefficient
let coeff = util::smoothing_coefficient(sample_rate, time_ms);
```

### Simple Filter

```rust
struct OnePoleFilter {
    z1: f32,
    coeff: f32,
}

impl OnePoleFilter {
    fn new() -> Self {
        Self { z1: 0.0, coeff: 0.0 }
    }

    fn set_frequency(&mut self, freq: f32, sample_rate: f32) {
        self.coeff = (-2.0 * std::f32::consts::PI * freq / sample_rate).exp();
    }

    fn process(&mut self, input: f32) -> f32 {
        self.z1 = input + self.coeff * (self.z1 - input);
        self.z1
    }

    fn reset(&mut self) {
        self.z1 = 0.0;
    }
}
```

### Biquad Filter

```rust
struct Biquad {
    b0: f32, b1: f32, b2: f32,
    a1: f32, a2: f32,
    z1: f32, z2: f32,
}

impl Biquad {
    fn new() -> Self {
        Self {
            b0: 1.0, b1: 0.0, b2: 0.0,
            a1: 0.0, a2: 0.0,
            z1: 0.0, z2: 0.0,
        }
    }

    fn set_lowpass(&mut self, freq: f32, q: f32, sample_rate: f32) {
        let w0 = 2.0 * std::f32::consts::PI * freq / sample_rate;
        let cos_w0 = w0.cos();
        let sin_w0 = w0.sin();
        let alpha = sin_w0 / (2.0 * q);

        let a0 = 1.0 + alpha;
        self.b0 = ((1.0 - cos_w0) / 2.0) / a0;
        self.b1 = (1.0 - cos_w0) / a0;
        self.b2 = self.b0;
        self.a1 = (-2.0 * cos_w0) / a0;
        self.a2 = (1.0 - alpha) / a0;
    }

    fn process(&mut self, input: f32) -> f32 {
        let output = self.b0 * input + self.z1;
        self.z1 = self.b1 * input - self.a1 * output + self.z2;
        self.z2 = self.b2 * input - self.a2 * output;
        output
    }

    fn reset(&mut self) {
        self.z1 = 0.0;
        self.z2 = 0.0;
    }
}
```

### Delay Line

```rust
struct DelayLine {
    buffer: Vec<f32>,
    write_pos: usize,
}

impl DelayLine {
    fn new(max_delay_samples: usize) -> Self {
        Self {
            buffer: vec![0.0; max_delay_samples],
            write_pos: 0,
        }
    }

    fn write(&mut self, sample: f32) {
        self.buffer[self.write_pos] = sample;
        self.write_pos = (self.write_pos + 1) % self.buffer.len();
    }

    fn read(&self, delay_samples: usize) -> f32 {
        let read_pos = (self.write_pos + self.buffer.len() - delay_samples)
            % self.buffer.len();
        self.buffer[read_pos]
    }

    fn read_linear(&self, delay_samples: f32) -> f32 {
        let delay_int = delay_samples as usize;
        let frac = delay_samples - delay_int as f32;

        let y0 = self.read(delay_int);
        let y1 = self.read(delay_int + 1);

        y0 + frac * (y1 - y0)
    }

    fn reset(&mut self) {
        self.buffer.fill(0.0);
    }
}
```

## GUI with Vizia

```toml
# Cargo.toml
[dependencies]
nih_plug_vizia = { git = "https://github.com/robbert-vdh/nih-plug.git" }
```

```rust
// src/editor.rs
use nih_plug::prelude::*;
use nih_plug_vizia::vizia::prelude::*;
use nih_plug_vizia::widgets::*;
use nih_plug_vizia::{assets, create_vizia_editor, ViziaState, ViziaTheming};
use std::sync::Arc;

use crate::MyParams;

#[derive(Lens)]
struct Data {
    params: Arc<MyParams>,
}

impl Model for Data {}

pub fn default_state() -> Arc<ViziaState> {
    ViziaState::new(|| (400, 300))
}

pub fn create(params: Arc<MyParams>, editor_state: Arc<ViziaState>) -> Option<Box<dyn Editor>> {
    create_vizia_editor(editor_state, ViziaTheming::Custom, move |cx, _| {
        assets::register_noto_sans_light(cx);
        assets::register_noto_sans_thin(cx);

        Data {
            params: params.clone(),
        }
        .build(cx);

        VStack::new(cx, |cx| {
            Label::new(cx, "My Plugin")
                .font_size(24.0)
                .height(Pixels(50.0));

            ParamSlider::new(cx, Data::params, |params| &params.gain)
                .height(Pixels(40.0));
        })
        .row_between(Pixels(10.0))
        .child_space(Stretch(1.0));
    })
}
```

Update plugin:

```rust
// src/lib.rs
mod editor;

#[derive(Params)]
struct MyParams {
    #[persist = "editor-state"]
    editor_state: Arc<ViziaState>,

    #[id = "gain"]
    pub gain: FloatParam,
}

impl Default for MyParams {
    fn default() -> Self {
        Self {
            editor_state: editor::default_state(),
            gain: FloatParam::new(...),
        }
    }
}

impl Plugin for MyPlugin {
    fn editor(&mut self, _async_executor: AsyncExecutor<Self>) -> Option<Box<dyn Editor>> {
        editor::create(self.params.clone(), self.params.editor_state.clone())
    }
}
```

## GUI with egui

```toml
# Cargo.toml
[dependencies]
nih_plug_egui = { git = "https://github.com/robbert-vdh/nih-plug.git" }
```

```rust
use nih_plug_egui::{create_egui_editor, egui, EguiState};

fn editor(&mut self, _async_executor: AsyncExecutor<Self>) -> Option<Box<dyn Editor>> {
    let params = self.params.clone();

    create_egui_editor(
        self.params.editor_state.clone(),
        (),
        |_, _| {},
        move |egui_ctx, setter, _state| {
            egui::CentralPanel::default().show(egui_ctx, |ui| {
                ui.heading("My Plugin");

                ui.add(
                    egui::Slider::from_get_set(-30.0..=30.0, |new_val| {
                        if let Some(val) = new_val {
                            setter.begin_set_parameter(&params.gain);
                            setter.set_parameter(
                                &params.gain,
                                util::db_to_gain(val as f32),
                            );
                            setter.end_set_parameter(&params.gain);
                        }
                        util::gain_to_db(params.gain.value()) as f64
                    })
                    .suffix(" dB")
                    .text("Gain"),
                );
            });
        },
    )
}
```

## Background Tasks

```rust
struct MyPlugin {
    params: Arc<MyParams>,
}

enum BackgroundTask {
    LoadPreset(String),
    AnalyzeAudio(Vec<f32>),
}

impl Plugin for MyPlugin {
    type BackgroundTask = BackgroundTask;

    fn process(
        &mut self,
        buffer: &mut Buffer,
        _aux: &mut AuxiliaryBuffers,
        context: &mut impl ProcessContext<Self>,
    ) -> ProcessStatus {
        // Schedule background work
        context.execute_background(BackgroundTask::AnalyzeAudio(
            buffer.as_slice()[0].to_vec()
        ));

        ProcessStatus::Normal
    }

    fn task_executor(&mut self) -> TaskExecutor<Self> {
        Box::new(|task| {
            match task {
                BackgroundTask::LoadPreset(path) => {
                    // Heavy file I/O here
                }
                BackgroundTask::AnalyzeAudio(samples) => {
                    // CPU-intensive analysis
                }
            }
        })
    }
}
```

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use nih_plug::buffer::Buffer;

    #[test]
    fn test_gain() {
        let mut plugin = MyPlugin::default();

        // Create test buffer
        let mut buffer_data = [[0.5f32; 512]; 2];
        let mut buffer = Buffer::from(buffer_data.iter_mut().map(|c| c.as_mut_slice()));

        // Process
        plugin.process(
            &mut buffer,
            &mut AuxiliaryBuffers::default(),
            &mut (),
        );

        // Verify (with 0dB gain, output should equal input)
        assert!((buffer.as_slice()[0][0] - 0.5).abs() < 0.01);
    }
}
```

## Cross-Platform Building

```bash
# macOS Universal Binary
cargo xtask bundle my_plugin --release --target x86_64-apple-darwin
cargo xtask bundle my_plugin --release --target aarch64-apple-darwin

# Combine into universal
lipo -create \
    target/bundled/my_plugin.vst3/Contents/MacOS/my_plugin \
    -output target/bundled/my_plugin-universal.vst3/Contents/MacOS/my_plugin

# Windows (from macOS/Linux)
cargo xtask bundle my_plugin --release --target x86_64-pc-windows-gnu

# Linux
cargo xtask bundle my_plugin --release --target x86_64-unknown-linux-gnu
```

## Resources

- [NIH-plug GitHub](https://github.com/robbert-vdh/nih-plug)
- [NIH-plug Examples](https://github.com/robbert-vdh/nih-plug/tree/master/plugins)
- [Vizia Documentation](https://github.com/vizia/vizia)
- [Rust Audio Discord](https://discord.gg/rust-audio)
