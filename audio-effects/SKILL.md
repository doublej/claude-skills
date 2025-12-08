---
name: audio-effects
description: Comprehensive guide for building audio effect processors and VST/AU plugins. Covers JUCE (C++), NIH-plug (Rust), iPlug2, DSP fundamentals, and common effect implementations (filters, delays, reverbs, compressors). Use when building audio plugins, implementing DSP algorithms, or learning audio programming.
---

# Audio Effects Plugin Development

Build professional audio effect processors as VST3, AU, AAX, and CLAP plugins.

## When to Use This Skill

- Building VST/AU audio plugins
- Implementing DSP algorithms (filters, delays, reverbs, dynamics)
- Learning audio programming fundamentals
- Choosing between JUCE, NIH-plug, iPlug2, or other frameworks
- Debugging audio processing issues

## Framework Quick Reference

| Framework | Language | Formats | Best For |
|-----------|----------|---------|----------|
| [JUCE](https://juce.com/) | C++ | VST, VST3, AU, AUv3, AAX, LV2 | Professional/commercial, industry standard |
| [NIH-plug](https://github.com/robbert-vdh/nih-plug) | Rust | VST3, CLAP | Modern, memory-safe, growing ecosystem |
| [iPlug2](https://github.com/iPlug2/iPlug2) | C++ | VST2, VST3, AU, AUv3, AAX, WAM | Minimalist, excellent docs |
| [DPF](https://github.com/DISTRHO/DPF) | C++ | LADSPA, DSSI, LV2, VST2, VST3, CLAP | Open-source, cross-platform |
| [Dplug](https://github.com/AuburnSounds/Dplug) | D | VST2, VST3, AU, AAX, LV2 | Physical-modeled GUI |
| [HISE](https://hise.dev/) | Visual/Script | Native compiled | No-code, rapid prototyping |

### Recommendation Matrix

```
Need commercial support?
├── Yes → JUCE (industry standard, Korg/ROLI/Native Instruments use it)
└── No
    ├── Want memory safety?
    │   └── Yes → NIH-plug (Rust)
    └── Prefer minimal boilerplate?
        └── Yes → iPlug2 (C++)
```

## Quick Start: Your First Plugin

### Option A: JUCE (C++)

```bash
# Install JUCE (macOS)
brew install juce

# Or download from juce.com and use Projucer
```

Minimal gain plugin structure:

```cpp
// PluginProcessor.h
class GainProcessor : public juce::AudioProcessor {
public:
    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    juce::AudioProcessorValueTreeState parameters;
private:
    float currentGain = 1.0f;
};

// PluginProcessor.cpp
void GainProcessor::processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer&) {
    float targetGain = *parameters.getRawParameterValue("gain");

    // Smooth gain changes to avoid clicks
    for (int sample = 0; sample < buffer.getNumSamples(); ++sample) {
        currentGain += 0.001f * (targetGain - currentGain);
        for (int channel = 0; channel < buffer.getNumChannels(); ++channel) {
            buffer.getSample(channel, sample) *= currentGain;
        }
    }
}
```

See **[JUCE GUIDE](references/juce-guide.md)** for complete setup and patterns.

### Option B: NIH-plug (Rust)

```bash
# Create new plugin
cargo new --lib my_plugin
cd my_plugin
```

```toml
# Cargo.toml
[package]
name = "my_plugin"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
nih_plug = { git = "https://github.com/robbert-vdh/nih-plug.git" }
```

Minimal gain plugin:

```rust
use nih_plug::prelude::*;
use std::sync::Arc;

struct GainPlugin {
    params: Arc<GainParams>,
}

#[derive(Params)]
struct GainParams {
    #[id = "gain"]
    gain: FloatParam,
}

impl Default for GainPlugin {
    fn default() -> Self {
        Self {
            params: Arc::new(GainParams::default()),
        }
    }
}

impl Default for GainParams {
    fn default() -> Self {
        Self {
            gain: FloatParam::new(
                "Gain",
                util::db_to_gain(0.0),
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

impl Plugin for GainPlugin {
    const NAME: &'static str = "Gain Plugin";
    const VENDOR: &'static str = "Your Name";
    const URL: &'static str = "";
    const EMAIL: &'static str = "";
    const VERSION: &'static str = env!("CARGO_PKG_VERSION");

    const AUDIO_IO_LAYOUTS: &'static [AudioIOLayout] = &[
        AudioIOLayout {
            main_input_channels: NonZeroU32::new(2),
            main_output_channels: NonZeroU32::new(2),
            ..AudioIOLayout::const_default()
        },
    ];

    type SysExMessage = ();
    type BackgroundTask = ();

    fn params(&self) -> Arc<dyn Params> {
        self.params.clone()
    }

    fn process(
        &mut self,
        buffer: &mut Buffer,
        _aux: &mut AuxiliaryBuffers,
        _context: &mut impl ProcessContext<Self>,
    ) -> ProcessStatus {
        for channel_samples in buffer.iter_samples() {
            let gain = self.params.gain.smoothed.next();
            for sample in channel_samples {
                *sample *= gain;
            }
        }
        ProcessStatus::Normal
    }
}

nih_export_vst3!(GainPlugin);
nih_export_clap!(GainPlugin);
```

See **[NIH-PLUG GUIDE](references/nih-plug-guide.md)** for complete patterns.

## Core DSP Concepts

### Audio Buffer Processing

Every audio plugin processes audio in **blocks** (typically 64-512 samples):

```
Host → Plugin.process(buffer) → Output
         │
         ├── buffer.numChannels (usually 2 for stereo)
         ├── buffer.numSamples (block size, varies)
         └── buffer.sampleRate (44100, 48000, 96000 Hz)
```

### Sample Rate Awareness

Always scale time-dependent parameters by sample rate:

```cpp
// WRONG: Hardcoded delay
int delaySamples = 1000;

// RIGHT: Time-based delay
float delayMs = 100.0f;
int delaySamples = static_cast<int>(delayMs * sampleRate / 1000.0f);
```

### Parameter Smoothing

Never apply parameter changes directly—causes clicks:

```cpp
// WRONG: Instant change (clicks)
gain = newGain;

// RIGHT: Smoothed change
gain += 0.001f * (newGain - gain);  // Simple one-pole

// BETTER: Exponential smoothing
const float smoothTime = 0.01f;  // 10ms
const float coeff = 1.0f - std::exp(-1.0f / (smoothTime * sampleRate));
gain += coeff * (newGain - gain);
```

### Decibels vs Linear Gain

```cpp
// dB to linear gain
float gain = std::pow(10.0f, dB / 20.0f);

// Linear gain to dB
float dB = 20.0f * std::log10(gain);

// Common values:
// 0 dB = 1.0 (unity)
// -6 dB ≈ 0.5 (half amplitude)
// -12 dB ≈ 0.25
// -inf dB = 0.0 (silence)
```

See **[DSP FUNDAMENTALS](references/dsp-fundamentals.md)** for filters, FFT, and more.

## Common Audio Effects

### 1. Filters (EQ, Tone Control)

**Biquad filter** (most common, 2nd-order IIR):

```cpp
class BiquadFilter {
    float b0, b1, b2, a1, a2;  // Coefficients
    float z1 = 0, z2 = 0;       // State (per channel)

public:
    void setLowpass(float freq, float Q, float sampleRate) {
        float w0 = 2.0f * M_PI * freq / sampleRate;
        float cosw0 = std::cos(w0);
        float sinw0 = std::sin(w0);
        float alpha = sinw0 / (2.0f * Q);

        float a0 = 1.0f + alpha;
        b0 = ((1.0f - cosw0) / 2.0f) / a0;
        b1 = (1.0f - cosw0) / a0;
        b2 = b0;
        a1 = (-2.0f * cosw0) / a0;
        a2 = (1.0f - alpha) / a0;
    }

    float process(float input) {
        float output = b0 * input + z1;
        z1 = b1 * input - a1 * output + z2;
        z2 = b2 * input - a2 * output;
        return output;
    }
};
```

### 2. Delay Effects

```cpp
class Delay {
    std::vector<float> buffer;
    int writePos = 0;

public:
    void prepare(float maxDelayMs, float sampleRate) {
        int maxSamples = static_cast<int>(maxDelayMs * sampleRate / 1000.0f);
        buffer.resize(maxSamples, 0.0f);
    }

    float process(float input, float delayMs, float feedback, float sampleRate) {
        int delaySamples = static_cast<int>(delayMs * sampleRate / 1000.0f);
        int readPos = (writePos - delaySamples + buffer.size()) % buffer.size();

        float delayed = buffer[readPos];
        buffer[writePos] = input + delayed * feedback;
        writePos = (writePos + 1) % buffer.size();

        return delayed;
    }
};
```

### 3. Dynamics (Compressor)

```cpp
class Compressor {
    float envelope = 0.0f;

public:
    float process(float input, float threshold, float ratio,
                  float attackMs, float releaseMs, float sampleRate) {
        // Envelope follower
        float absInput = std::abs(input);
        float attackCoeff = std::exp(-1.0f / (attackMs * sampleRate / 1000.0f));
        float releaseCoeff = std::exp(-1.0f / (releaseMs * sampleRate / 1000.0f));

        if (absInput > envelope)
            envelope = attackCoeff * envelope + (1.0f - attackCoeff) * absInput;
        else
            envelope = releaseCoeff * envelope + (1.0f - releaseCoeff) * absInput;

        // Gain computation
        float envDB = 20.0f * std::log10(envelope + 1e-6f);
        float gainDB = 0.0f;

        if (envDB > threshold)
            gainDB = (threshold - envDB) * (1.0f - 1.0f / ratio);

        float gain = std::pow(10.0f, gainDB / 20.0f);
        return input * gain;
    }
};
```

See **[COMMON EFFECTS](references/common-effects.md)** for reverbs, distortion, modulation.

## Plugin Formats Explained

| Format | Developer | Platform | Notes |
|--------|-----------|----------|-------|
| **VST3** | Steinberg | All | Modern standard, free license since 3.8.0 |
| **AU** | Apple | macOS/iOS | Required for Logic Pro, GarageBand |
| **AAX** | Avid | All | Required for Pro Tools (needs developer account) |
| **CLAP** | Bitwig/u-he | All | Newest format, modern design, fully open |
| **LV2** | Community | Linux | Open standard for Linux DAWs |
| **VST2** | Steinberg | All | Legacy (no new licenses), still widely supported |

### Format Recommendation

- **Minimum**: VST3 (covers most DAWs)
- **Mac users**: Add AU
- **Pro Tools**: Add AAX
- **Future-proof**: Consider CLAP

## Testing & Debugging

### Test in Multiple Hosts

Different DAWs process differently:
- **REAPER**: Free trial, excellent for testing
- **Ableton Live**: Strict AU validation
- **Logic Pro**: Apple AU validation
- **Bitwig**: First-class CLAP support

### Common Issues

| Symptom | Likely Cause |
|---------|--------------|
| Clicks/pops | Parameter changes not smoothed |
| Crackles | Buffer underrun, processing too slow |
| No output | Forgot to write to output buffer |
| CPU spikes | Allocating memory in process() |
| Crashes on load | Uninitialized state |

### Golden Rules

1. **Never allocate in process()** - All memory allocation in `prepare()`
2. **Never block in process()** - No mutex, file I/O, network
3. **Handle edge cases** - Zero samples, channel count changes
4. **Reset state properly** - Clear buffers on `reset()` call
5. **Be sample rate aware** - Recalculate coefficients when rate changes

## Learning Path

### Beginner
1. Build a gain plugin (parameter smoothing)
2. Add a simple lowpass filter
3. Create basic delay effect

### Intermediate
4. Multi-band EQ with biquads
5. Compressor with sidechain
6. Chorus/flanger with LFO modulation

### Advanced
7. Convolution reverb (FFT-based)
8. Physical modeling (waveguide synthesis)
9. Spectral processing (phase vocoder)

## Recommended Resources

### Books
- **"Designing Audio Effect Plugins in C++"** by Will Pirkle - Comprehensive, covers JUCE
- **"DAFX: Digital Audio Effects"** by Zölzer - Academic but thorough
- **"The Audio Programming Book"** by Boulanger/Lazzarini - Theory and practice

### Online
- [Audio Developer Conference](https://audio.dev/) - Annual talks, many free
- [The Audio Programmer Discord](https://discord.gg/audiodeveloper) - Active community
- [KVR Forum](https://www.kvraudio.com/forum/) - Plugin development discussions
- [Musicdsp.org](https://www.musicdsp.org/) - Algorithm archive

### Reference Docs
- **[JUCE GUIDE](references/juce-guide.md)** - JUCE setup, patterns, GUI
- **[NIH-PLUG GUIDE](references/nih-plug-guide.md)** - Rust plugin development
- **[DSP FUNDAMENTALS](references/dsp-fundamentals.md)** - Filters, FFT, math
- **[COMMON EFFECTS](references/common-effects.md)** - Effect implementations
