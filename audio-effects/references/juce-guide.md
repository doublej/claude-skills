# JUCE Framework Guide

JUCE is the industry-standard C++ framework for audio plugin development. Used by Korg, ROLI, Native Instruments, and many commercial plugin vendors.

## Setup

### Installation

**macOS (Homebrew):**
```bash
brew install juce
```

**Manual Installation:**
1. Download from [juce.com](https://juce.com/get-juce)
2. Run Projucer (GUI project manager)
3. Or use CMake directly (recommended for CI/CD)

### CMake Project Setup (Recommended)

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.22)
project(MyPlugin VERSION 1.0.0)

# Fetch JUCE
include(FetchContent)
FetchContent_Declare(
    JUCE
    GIT_REPOSITORY https://github.com/juce-framework/JUCE.git
    GIT_TAG 7.0.9  # Use latest stable
)
FetchContent_MakeAvailable(JUCE)

# Plugin target
juce_add_plugin(MyPlugin
    COMPANY_NAME "Your Company"
    PLUGIN_MANUFACTURER_CODE Manu
    PLUGIN_CODE Plg1
    FORMATS VST3 AU Standalone
    PRODUCT_NAME "My Plugin"
)

# Source files
target_sources(MyPlugin PRIVATE
    src/PluginProcessor.cpp
    src/PluginEditor.cpp
)

# JUCE modules
target_link_libraries(MyPlugin PRIVATE
    juce::juce_audio_utils
    juce::juce_dsp
    juce::juce_recommended_config_flags
    juce::juce_recommended_lto_flags
    juce::juce_recommended_warning_flags
)

# Compile definitions
target_compile_definitions(MyPlugin PUBLIC
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0
)
```

### Build Commands

```bash
# Configure
cmake -B build -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build build --config Release

# Plugin location (macOS)
# build/MyPlugin_artefacts/Release/VST3/MyPlugin.vst3
# build/MyPlugin_artefacts/Release/AU/MyPlugin.component
```

## Project Structure

```
MyPlugin/
├── CMakeLists.txt
├── src/
│   ├── PluginProcessor.h
│   ├── PluginProcessor.cpp
│   ├── PluginEditor.h
│   └── PluginEditor.cpp
└── resources/
    └── (images, presets, etc.)
```

## AudioProcessor (DSP Core)

The `AudioProcessor` class handles all audio processing:

```cpp
// PluginProcessor.h
#pragma once
#include <juce_audio_processors/juce_audio_processors.h>
#include <juce_dsp/juce_dsp.h>

class MyProcessor : public juce::AudioProcessor {
public:
    MyProcessor();
    ~MyProcessor() override;

    // Required overrides
    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;
    void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    // Editor
    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override { return true; }

    // Plugin info
    const juce::String getName() const override { return "My Plugin"; }
    bool acceptsMidi() const override { return false; }
    bool producesMidi() const override { return false; }
    double getTailLengthSeconds() const override { return 0.0; }

    // Programs (presets)
    int getNumPrograms() override { return 1; }
    int getCurrentProgram() override { return 0; }
    void setCurrentProgram(int) override {}
    const juce::String getProgramName(int) override { return {}; }
    void changeProgramName(int, const juce::String&) override {}

    // State persistence
    void getStateInformation(juce::MemoryBlock& destData) override;
    void setStateInformation(const void* data, int sizeInBytes) override;

    // Parameter tree
    juce::AudioProcessorValueTreeState parameters;

private:
    // DSP objects
    juce::dsp::Gain<float> gain;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MyProcessor)
};
```

```cpp
// PluginProcessor.cpp
#include "PluginProcessor.h"
#include "PluginEditor.h"

// Parameter layout
static juce::AudioProcessorValueTreeState::ParameterLayout createParameters() {
    std::vector<std::unique_ptr<juce::RangedAudioParameter>> params;

    params.push_back(std::make_unique<juce::AudioParameterFloat>(
        juce::ParameterID{"gain", 1},  // ID, version
        "Gain",                         // Name
        juce::NormalisableRange<float>(-60.0f, 12.0f, 0.1f),  // Range
        0.0f,                           // Default
        juce::String(),                 // Label
        juce::AudioProcessorParameter::genericParameter,
        [](float val, int) { return juce::String(val, 1) + " dB"; },  // Value to string
        [](const juce::String& s) { return s.getFloatValue(); }       // String to value
    ));

    return { params.begin(), params.end() };
}

MyProcessor::MyProcessor()
    : AudioProcessor(BusesProperties()
        .withInput("Input", juce::AudioChannelSet::stereo(), true)
        .withOutput("Output", juce::AudioChannelSet::stereo(), true)),
      parameters(*this, nullptr, "Parameters", createParameters())
{
}

MyProcessor::~MyProcessor() {}

void MyProcessor::prepareToPlay(double sampleRate, int samplesPerBlock) {
    // Prepare DSP objects
    juce::dsp::ProcessSpec spec;
    spec.sampleRate = sampleRate;
    spec.maximumBlockSize = static_cast<juce::uint32>(samplesPerBlock);
    spec.numChannels = static_cast<juce::uint32>(getTotalNumOutputChannels());

    gain.prepare(spec);
}

void MyProcessor::releaseResources() {
    // Free any resources
}

void MyProcessor::processBlock(juce::AudioBuffer<float>& buffer,
                                juce::MidiBuffer& midiMessages) {
    juce::ScopedNoDenormals noDenormals;

    // Clear unused channels
    for (auto i = getTotalNumInputChannels(); i < getTotalNumOutputChannels(); ++i)
        buffer.clear(i, 0, buffer.getNumSamples());

    // Get parameter value
    float gainDB = *parameters.getRawParameterValue("gain");
    gain.setGainDecibels(gainDB);

    // Process using juce::dsp
    juce::dsp::AudioBlock<float> block(buffer);
    juce::dsp::ProcessContextReplacing<float> context(block);
    gain.process(context);
}

juce::AudioProcessorEditor* MyProcessor::createEditor() {
    return new MyEditor(*this);
}

void MyProcessor::getStateInformation(juce::MemoryBlock& destData) {
    auto state = parameters.copyState();
    std::unique_ptr<juce::XmlElement> xml(state.createXml());
    copyXmlToBinary(*xml, destData);
}

void MyProcessor::setStateInformation(const void* data, int sizeInBytes) {
    std::unique_ptr<juce::XmlElement> xml(getXmlFromBinary(data, sizeInBytes));
    if (xml && xml->hasTagName(parameters.state.getType()))
        parameters.replaceState(juce::ValueTree::fromXml(*xml));
}

// Required: Plugin factory
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter() {
    return new MyProcessor();
}
```

## AudioProcessorEditor (GUI)

```cpp
// PluginEditor.h
#pragma once
#include <juce_audio_processors/juce_audio_processors.h>
#include "PluginProcessor.h"

class MyEditor : public juce::AudioProcessorEditor {
public:
    explicit MyEditor(MyProcessor&);
    ~MyEditor() override;

    void paint(juce::Graphics&) override;
    void resized() override;

private:
    MyProcessor& processor;

    juce::Slider gainSlider;
    juce::Label gainLabel;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> gainAttachment;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MyEditor)
};
```

```cpp
// PluginEditor.cpp
#include "PluginEditor.h"

MyEditor::MyEditor(MyProcessor& p)
    : AudioProcessorEditor(&p), processor(p)
{
    // Gain slider
    gainSlider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    gainSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    addAndMakeVisible(gainSlider);

    // Attach to parameter
    gainAttachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        processor.parameters, "gain", gainSlider);

    // Label
    gainLabel.setText("Gain", juce::dontSendNotification);
    gainLabel.setJustificationType(juce::Justification::centred);
    addAndMakeVisible(gainLabel);

    // Window size
    setSize(400, 300);
}

MyEditor::~MyEditor() {}

void MyEditor::paint(juce::Graphics& g) {
    g.fillAll(juce::Colours::darkgrey);
}

void MyEditor::resized() {
    auto bounds = getLocalBounds().reduced(20);
    gainLabel.setBounds(bounds.removeFromTop(30));
    gainSlider.setBounds(bounds.reduced(50));
}
```

## JUCE DSP Module

JUCE provides ready-to-use DSP classes:

### Filters

```cpp
#include <juce_dsp/juce_dsp.h>

// IIR Filters
juce::dsp::IIR::Filter<float> lowpass;
auto coeffs = juce::dsp::IIR::Coefficients<float>::makeLowPass(sampleRate, 1000.0f, 0.707f);
lowpass.coefficients = coeffs;

// State Variable Filter (better for modulation)
juce::dsp::StateVariableTPTFilter<float> svf;
svf.setType(juce::dsp::StateVariableTPTFilterType::lowpass);
svf.setCutoffFrequency(1000.0f);
svf.setResonance(0.707f);

// Ladder Filter (4-pole, Moog-style)
juce::dsp::LadderFilter<float> ladder;
ladder.setMode(juce::dsp::LadderFilterMode::LPF24);
ladder.setCutoffFrequencyHz(800.0f);
ladder.setResonance(0.5f);
```

### Delay

```cpp
juce::dsp::DelayLine<float, juce::dsp::DelayLineInterpolationTypes::Linear> delay;

void prepareToPlay(double sampleRate, int samplesPerBlock) {
    delay.setMaximumDelayInSamples(static_cast<int>(sampleRate * 2.0));  // 2 sec max
    delay.prepare({sampleRate, (juce::uint32)samplesPerBlock, 2});
}

void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer&) {
    float delayTimeMs = 250.0f;
    float delaySamples = delayTimeMs * getSampleRate() / 1000.0f;
    delay.setDelay(delaySamples);

    for (int ch = 0; ch < buffer.getNumChannels(); ++ch) {
        auto* data = buffer.getWritePointer(ch);
        for (int i = 0; i < buffer.getNumSamples(); ++i) {
            float delayed = delay.popSample(ch);
            delay.pushSample(ch, data[i]);
            data[i] = data[i] + delayed * 0.5f;  // Mix
        }
    }
}
```

### Compressor

```cpp
juce::dsp::Compressor<float> compressor;

compressor.setThreshold(-20.0f);  // dB
compressor.setRatio(4.0f);
compressor.setAttack(10.0f);      // ms
compressor.setRelease(100.0f);    // ms
```

### Reverb

```cpp
juce::dsp::Reverb reverb;
juce::dsp::Reverb::Parameters reverbParams;

reverbParams.roomSize = 0.7f;
reverbParams.damping = 0.5f;
reverbParams.wetLevel = 0.3f;
reverbParams.dryLevel = 0.7f;
reverbParams.width = 1.0f;

reverb.setParameters(reverbParams);
```

### Convolution

```cpp
juce::dsp::Convolution convolution;

// Load IR from file
convolution.loadImpulseResponse(
    juce::File("/path/to/ir.wav"),
    juce::dsp::Convolution::Stereo::yes,
    juce::dsp::Convolution::Trim::yes,
    0  // Size (0 = auto)
);

// Or from binary data
convolution.loadImpulseResponse(
    BinaryData::ir_wav, BinaryData::ir_wavSize,
    juce::dsp::Convolution::Stereo::yes,
    juce::dsp::Convolution::Trim::yes,
    0
);
```

### Waveshaper (Distortion)

```cpp
juce::dsp::WaveShaper<float> waveshaper;

// Soft clipping
waveshaper.functionToUse = [](float x) {
    return std::tanh(x);
};

// Hard clipping
waveshaper.functionToUse = [](float x) {
    return juce::jlimit(-1.0f, 1.0f, x);
};

// Custom waveshape lookup table (faster)
waveshaper.functionToUse = juce::dsp::FastMathApproximations::tanh;
```

### Oscillator

```cpp
juce::dsp::Oscillator<float> osc;

// Sine
osc.initialise([](float x) { return std::sin(x); });

// Saw
osc.initialise([](float x) { return x / juce::MathConstants<float>::pi; });

// Square
osc.initialise([](float x) {
    return x < 0.0f ? -1.0f : 1.0f;
});

osc.setFrequency(440.0f);
```

### Oversampling

```cpp
juce::dsp::Oversampling<float> oversampling(
    2,  // numChannels
    2,  // oversamplingFactor (2^2 = 4x)
    juce::dsp::Oversampling<float>::filterHalfBandPolyphaseIIR
);

void prepareToPlay(double sampleRate, int samplesPerBlock) {
    oversampling.initProcessing(static_cast<size_t>(samplesPerBlock));
}

void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer&) {
    juce::dsp::AudioBlock<float> block(buffer);

    // Upsample
    auto oversampledBlock = oversampling.processSamplesUp(block);

    // Process at higher sample rate (for non-linear effects)
    // waveshaper.process(juce::dsp::ProcessContextReplacing<float>(oversampledBlock));

    // Downsample
    oversampling.processSamplesDown(block);
}
```

## ProcessorChain (Signal Chain)

Combine multiple processors:

```cpp
using MonoChain = juce::dsp::ProcessorChain<
    juce::dsp::IIR::Filter<float>,   // Highpass
    juce::dsp::Gain<float>,          // Input gain
    juce::dsp::WaveShaper<float>,    // Distortion
    juce::dsp::IIR::Filter<float>,   // Lowpass
    juce::dsp::Gain<float>           // Output gain
>;

MonoChain chain;

enum ChainPositions {
    Highpass,
    InputGain,
    Distortion,
    Lowpass,
    OutputGain
};

// Access individual processors
auto& highpass = chain.get<Highpass>();
auto& distortion = chain.get<Distortion>();
```

## Parameter Types

### Float Parameter

```cpp
std::make_unique<juce::AudioParameterFloat>(
    juce::ParameterID{"freq", 1},
    "Frequency",
    juce::NormalisableRange<float>(20.0f, 20000.0f, 1.0f, 0.25f),  // Skewed for log
    1000.0f
)
```

### Bool Parameter

```cpp
std::make_unique<juce::AudioParameterBool>(
    juce::ParameterID{"bypass", 1},
    "Bypass",
    false
)
```

### Choice Parameter

```cpp
std::make_unique<juce::AudioParameterChoice>(
    juce::ParameterID{"filterType", 1},
    "Filter Type",
    juce::StringArray{"Lowpass", "Highpass", "Bandpass"},
    0  // Default index
)
```

### Int Parameter

```cpp
std::make_unique<juce::AudioParameterInt>(
    juce::ParameterID{"voices", 1},
    "Voices",
    1, 8,  // Min, max
    4      // Default
)
```

## Thread Safety

### Parameter Access

```cpp
// SAFE: Atomic read in audio thread
float value = *parameters.getRawParameterValue("gain");

// SAFE: Using smoothed values
juce::SmoothedValue<float> smoothedGain;

void prepareToPlay(double sampleRate, int samplesPerBlock) {
    smoothedGain.reset(sampleRate, 0.02);  // 20ms smoothing
}

void processBlock(...) {
    smoothedGain.setTargetValue(*parameters.getRawParameterValue("gain"));
    for (int i = 0; i < buffer.getNumSamples(); ++i) {
        float gain = smoothedGain.getNextValue();
        // Use gain...
    }
}
```

### Background Processing

```cpp
// For heavy non-realtime work
juce::ThreadPool threadPool(4);

threadPool.addJob([this]() {
    // Heavy work here (file loading, analysis, etc.)
    // Then signal back to audio thread
});
```

## Testing

### Unit Tests

```cpp
#include <juce_audio_processors/juce_audio_processors.h>

class MyProcessorTests : public juce::UnitTest {
public:
    MyProcessorTests() : juce::UnitTest("MyProcessor Tests") {}

    void runTest() override {
        beginTest("Basic Processing");

        MyProcessor processor;
        processor.prepareToPlay(44100.0, 512);

        juce::AudioBuffer<float> buffer(2, 512);
        buffer.clear();
        buffer.setSample(0, 0, 1.0f);  // Impulse

        juce::MidiBuffer midi;
        processor.processBlock(buffer, midi);

        // Assert output
        expect(buffer.getMagnitude(0, 512) > 0.0f);
    }
};

static MyProcessorTests tests;
```

### Plugin Validation

```bash
# macOS AU validation
auval -v aufx Plg1 Manu

# Steinberg VST3 validator
vstvalidator /path/to/MyPlugin.vst3
```

## Performance Tips

1. **Use `ScopedNoDenormals`** at start of processBlock
2. **Pre-allocate all memory** in prepareToPlay
3. **Avoid branching** in tight loops
4. **Use SIMD** via `juce::dsp::SIMDRegister`
5. **Profile with Tracy** or Instruments

```cpp
// SIMD example
#include <juce_dsp/juce_dsp.h>

using SIMDFloat = juce::dsp::SIMDRegister<float>;
constexpr size_t simdSize = SIMDFloat::size();

void processBlock(juce::AudioBuffer<float>& buffer, ...) {
    auto* data = buffer.getWritePointer(0);
    int numSamples = buffer.getNumSamples();

    // Process in SIMD chunks
    int simdIterations = numSamples / simdSize;
    for (int i = 0; i < simdIterations; ++i) {
        auto samples = SIMDFloat::fromRawArray(data + i * simdSize);
        samples = samples * gainValue;
        samples.copyToRawArray(data + i * simdSize);
    }

    // Handle remainder
    for (int i = simdIterations * simdSize; i < numSamples; ++i) {
        data[i] *= gainValue;
    }
}
```

## Resources

- [JUCE Documentation](https://docs.juce.com/)
- [JUCE Tutorials](https://juce.com/learn/tutorials)
- [JUCE Forum](https://forum.juce.com/)
- [The Audio Programmer YouTube](https://www.youtube.com/@TheAudioProgrammer)
