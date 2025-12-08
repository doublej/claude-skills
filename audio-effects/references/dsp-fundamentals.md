# DSP Fundamentals for Audio Effects

Core digital signal processing concepts for building audio plugins.

## Audio Basics

### Sample Rate

Number of samples per second (Hz):
- **44100 Hz** - CD quality, common default
- **48000 Hz** - Video/broadcast standard
- **96000 Hz** - High-quality production
- **192000 Hz** - Mastering/archival

**Nyquist frequency** = Sample Rate / 2 (highest representable frequency)

```cpp
// Always use sample rate for time-based calculations
float delayMs = 100.0f;
int delaySamples = (int)(delayMs * sampleRate / 1000.0f);
```

### Bit Depth

Number of bits per sample:
- **16-bit**: 96 dB dynamic range (CD)
- **24-bit**: 144 dB dynamic range (professional)
- **32-bit float**: ~1500 dB (internal processing)

Most plugins process in 32-bit or 64-bit float internally.

### Decibels (dB)

Logarithmic ratio scale:

```cpp
// Linear gain to dB
float dB = 20.0f * log10(gain);

// dB to linear gain
float gain = pow(10.0f, dB / 20.0f);

// Common values:
// +6 dB  = 2.0 (double amplitude)
// 0 dB   = 1.0 (unity)
// -6 dB  = 0.5 (half amplitude)
// -12 dB = 0.25
// -20 dB = 0.1
// -∞ dB  = 0.0 (silence)
```

### Block Processing

Audio processed in blocks (buffers), not sample-by-sample:

```
Host provides:
├── sampleRate: 48000 Hz
├── blockSize: 512 samples (≈10.7ms)
├── numChannels: 2 (stereo)
└── buffer: float[channels][samples]
```

Block size varies (64-2048 typical). Never assume fixed size.

## Filters

### Filter Types

| Type | Use Case |
|------|----------|
| **Lowpass (LP)** | Remove high frequencies, warming |
| **Highpass (HP)** | Remove low frequencies, clarity |
| **Bandpass (BP)** | Isolate frequency range |
| **Bandreject/Notch** | Remove specific frequency |
| **Allpass** | Phase shift (phasers, reverbs) |
| **Shelf** | Boost/cut above or below frequency |
| **Peak/Bell** | Boost/cut around frequency (EQ) |

### Filter Parameters

- **Cutoff/Center Frequency**: Where filter acts (Hz)
- **Q (Quality Factor)**: Resonance/bandwidth
  - Higher Q = narrower, more resonant
  - Q = 0.707 = Butterworth (flat)
  - Q > 0.707 = resonant peak
- **Gain**: For shelf/peak filters (dB)
- **Slope**: Steepness (dB/octave)
  - 6 dB/oct = 1st order
  - 12 dB/oct = 2nd order (biquad)
  - 24 dB/oct = 4th order

### Biquad Filter (2nd Order IIR)

Most common filter structure. Implements any 2nd-order transfer function.

**Direct Form II Transposed** (recommended for floating point):

```cpp
class Biquad {
    // Coefficients
    float b0, b1, b2;  // Numerator (feedforward)
    float a1, a2;       // Denominator (feedback)

    // State
    float z1 = 0, z2 = 0;

public:
    float process(float input) {
        float output = b0 * input + z1;
        z1 = b1 * input - a1 * output + z2;
        z2 = b2 * input - a2 * output;
        return output;
    }

    void reset() {
        z1 = z2 = 0;
    }
};
```

**Coefficient Formulas** (Audio EQ Cookbook by Robert Bristow-Johnson):

```cpp
void setLowpass(float freq, float Q, float sampleRate) {
    float w0 = 2.0f * M_PI * freq / sampleRate;
    float cosw0 = cos(w0);
    float sinw0 = sin(w0);
    float alpha = sinw0 / (2.0f * Q);

    float a0 = 1.0f + alpha;
    b0 = ((1.0f - cosw0) / 2.0f) / a0;
    b1 = (1.0f - cosw0) / a0;
    b2 = b0;
    a1 = (-2.0f * cosw0) / a0;
    a2 = (1.0f - alpha) / a0;
}

void setHighpass(float freq, float Q, float sampleRate) {
    float w0 = 2.0f * M_PI * freq / sampleRate;
    float cosw0 = cos(w0);
    float sinw0 = sin(w0);
    float alpha = sinw0 / (2.0f * Q);

    float a0 = 1.0f + alpha;
    b0 = ((1.0f + cosw0) / 2.0f) / a0;
    b1 = -(1.0f + cosw0) / a0;
    b2 = b0;
    a1 = (-2.0f * cosw0) / a0;
    a2 = (1.0f - alpha) / a0;
}

void setBandpass(float freq, float Q, float sampleRate) {
    float w0 = 2.0f * M_PI * freq / sampleRate;
    float cosw0 = cos(w0);
    float sinw0 = sin(w0);
    float alpha = sinw0 / (2.0f * Q);

    float a0 = 1.0f + alpha;
    b0 = alpha / a0;
    b1 = 0.0f;
    b2 = -alpha / a0;
    a1 = (-2.0f * cosw0) / a0;
    a2 = (1.0f - alpha) / a0;
}

void setPeakingEQ(float freq, float Q, float gainDB, float sampleRate) {
    float A = pow(10.0f, gainDB / 40.0f);
    float w0 = 2.0f * M_PI * freq / sampleRate;
    float cosw0 = cos(w0);
    float sinw0 = sin(w0);
    float alpha = sinw0 / (2.0f * Q);

    float a0 = 1.0f + alpha / A;
    b0 = (1.0f + alpha * A) / a0;
    b1 = (-2.0f * cosw0) / a0;
    b2 = (1.0f - alpha * A) / a0;
    a1 = b1;
    a2 = (1.0f - alpha / A) / a0;
}

void setLowShelf(float freq, float Q, float gainDB, float sampleRate) {
    float A = pow(10.0f, gainDB / 40.0f);
    float w0 = 2.0f * M_PI * freq / sampleRate;
    float cosw0 = cos(w0);
    float sinw0 = sin(w0);
    float alpha = sinw0 / (2.0f * Q);

    float a0 = (A + 1) + (A - 1) * cosw0 + 2 * sqrt(A) * alpha;
    b0 = A * ((A + 1) - (A - 1) * cosw0 + 2 * sqrt(A) * alpha) / a0;
    b1 = 2 * A * ((A - 1) - (A + 1) * cosw0) / a0;
    b2 = A * ((A + 1) - (A - 1) * cosw0 - 2 * sqrt(A) * alpha) / a0;
    a1 = -2 * ((A - 1) + (A + 1) * cosw0) / a0;
    a2 = ((A + 1) + (A - 1) * cosw0 - 2 * sqrt(A) * alpha) / a0;
}

void setHighShelf(float freq, float Q, float gainDB, float sampleRate) {
    float A = pow(10.0f, gainDB / 40.0f);
    float w0 = 2.0f * M_PI * freq / sampleRate;
    float cosw0 = cos(w0);
    float sinw0 = sin(w0);
    float alpha = sinw0 / (2.0f * Q);

    float a0 = (A + 1) - (A - 1) * cosw0 + 2 * sqrt(A) * alpha;
    b0 = A * ((A + 1) + (A - 1) * cosw0 + 2 * sqrt(A) * alpha) / a0;
    b1 = -2 * A * ((A - 1) + (A + 1) * cosw0) / a0;
    b2 = A * ((A + 1) + (A - 1) * cosw0 - 2 * sqrt(A) * alpha) / a0;
    a1 = 2 * ((A - 1) - (A + 1) * cosw0) / a0;
    a2 = ((A + 1) - (A - 1) * cosw0 - 2 * sqrt(A) * alpha) / a0;
}
```

### State Variable Filter (SVF)

Better for modulation (no coefficient jumps):

```cpp
class SVFilter {
    float ic1eq = 0, ic2eq = 0;
    float g, k, a1, a2, a3;

public:
    enum Type { LP, HP, BP, Notch, Peak, AllPass };

    void setCoefficients(float freq, float Q, float sampleRate) {
        g = tan(M_PI * freq / sampleRate);
        k = 1.0f / Q;
        a1 = 1.0f / (1.0f + g * (g + k));
        a2 = g * a1;
        a3 = g * a2;
    }

    float process(float input, Type type) {
        float v3 = input - ic2eq;
        float v1 = a1 * ic1eq + a2 * v3;
        float v2 = ic2eq + a2 * ic1eq + a3 * v3;

        ic1eq = 2.0f * v1 - ic1eq;
        ic2eq = 2.0f * v2 - ic2eq;

        switch (type) {
            case LP:     return v2;
            case BP:     return v1;
            case HP:     return input - k * v1 - v2;
            case Notch:  return input - k * v1;
            case Peak:   return input - k * v1 - 2.0f * v2;
            case AllPass: return input - 2.0f * k * v1;
        }
        return v2;
    }
};
```

### One-Pole Filter

Simplest filter (6 dB/octave):

```cpp
class OnePole {
    float z1 = 0;
    float a0, b1;

public:
    // Lowpass
    void setLowpass(float freq, float sampleRate) {
        b1 = exp(-2.0f * M_PI * freq / sampleRate);
        a0 = 1.0f - b1;
    }

    // Highpass
    void setHighpass(float freq, float sampleRate) {
        b1 = exp(-2.0f * M_PI * freq / sampleRate);
        a0 = (1.0f + b1) / 2.0f;
    }

    float process(float input) {
        z1 = input * a0 + z1 * b1;
        return z1;
    }
};
```

## Delay Lines

### Basic Delay

```cpp
class DelayLine {
    std::vector<float> buffer;
    int writePos = 0;
    int maxDelay;

public:
    void prepare(int maxDelaySamples) {
        maxDelay = maxDelaySamples;
        buffer.resize(maxDelay, 0.0f);
    }

    void write(float sample) {
        buffer[writePos] = sample;
        writePos = (writePos + 1) % maxDelay;
    }

    float read(int delaySamples) {
        int readPos = (writePos - delaySamples + maxDelay) % maxDelay;
        return buffer[readPos];
    }

    void reset() {
        std::fill(buffer.begin(), buffer.end(), 0.0f);
    }
};
```

### Interpolated Delay (for smooth modulation)

```cpp
// Linear interpolation
float readLinear(float delaySamples) {
    int delay0 = (int)delaySamples;
    int delay1 = delay0 + 1;
    float frac = delaySamples - delay0;

    float y0 = read(delay0);
    float y1 = read(delay1);

    return y0 + frac * (y1 - y0);
}

// Cubic interpolation (better quality)
float readCubic(float delaySamples) {
    int delay1 = (int)delaySamples;
    float frac = delaySamples - delay1;

    float y0 = read(delay1 - 1);
    float y1 = read(delay1);
    float y2 = read(delay1 + 1);
    float y3 = read(delay1 + 2);

    // Hermite interpolation
    float c0 = y1;
    float c1 = 0.5f * (y2 - y0);
    float c2 = y0 - 2.5f * y1 + 2.0f * y2 - 0.5f * y3;
    float c3 = 0.5f * (y3 - y0) + 1.5f * (y1 - y2);

    return ((c3 * frac + c2) * frac + c1) * frac + c0;
}

// Allpass interpolation (best for small modulations)
class AllpassDelayLine {
    DelayLine delay;
    float z1 = 0;

public:
    float read(float delaySamples) {
        int delayInt = (int)delaySamples;
        float frac = delaySamples - delayInt;

        // Allpass coefficient for fractional delay
        float coeff = (1.0f - frac) / (1.0f + frac);

        float y0 = delay.read(delayInt);
        float y1 = delay.read(delayInt + 1);

        float output = y1 + coeff * (y0 - z1);
        z1 = output;

        return output;
    }
};
```

## Envelope Followers

### Peak Detector

```cpp
class PeakDetector {
    float envelope = 0;
    float attackCoeff, releaseCoeff;

public:
    void setTimes(float attackMs, float releaseMs, float sampleRate) {
        attackCoeff = exp(-1.0f / (attackMs * sampleRate / 1000.0f));
        releaseCoeff = exp(-1.0f / (releaseMs * sampleRate / 1000.0f));
    }

    float process(float input) {
        float absInput = fabs(input);

        if (absInput > envelope)
            envelope = attackCoeff * envelope + (1.0f - attackCoeff) * absInput;
        else
            envelope = releaseCoeff * envelope;

        return envelope;
    }
};
```

### RMS Detector

```cpp
class RMSDetector {
    std::vector<float> buffer;
    float sum = 0;
    int writePos = 0;
    int windowSize;

public:
    void prepare(float windowMs, float sampleRate) {
        windowSize = (int)(windowMs * sampleRate / 1000.0f);
        buffer.resize(windowSize, 0.0f);
    }

    float process(float input) {
        float squared = input * input;

        // Subtract old, add new
        sum -= buffer[writePos];
        sum += squared;
        buffer[writePos] = squared;

        writePos = (writePos + 1) % windowSize;

        return sqrt(sum / windowSize);
    }
};
```

## Oscillators

### Phase Accumulator

```cpp
class PhaseAccumulator {
    float phase = 0;
    float phaseIncrement = 0;

public:
    void setFrequency(float freq, float sampleRate) {
        phaseIncrement = freq / sampleRate;
    }

    float next() {
        float out = phase;
        phase += phaseIncrement;
        if (phase >= 1.0f) phase -= 1.0f;
        return out;
    }
};
```

### Basic Waveforms

```cpp
// Sine
float sine(float phase) {
    return sin(2.0f * M_PI * phase);
}

// Triangle
float triangle(float phase) {
    return 4.0f * fabs(phase - 0.5f) - 1.0f;
}

// Sawtooth
float saw(float phase) {
    return 2.0f * phase - 1.0f;
}

// Square
float square(float phase) {
    return phase < 0.5f ? 1.0f : -1.0f;
}
```

### Anti-Aliased Oscillators (PolyBLEP)

```cpp
// PolyBLEP correction for discontinuities
float polyBlep(float t, float dt) {
    if (t < dt) {
        t /= dt;
        return t + t - t * t - 1.0f;
    } else if (t > 1.0f - dt) {
        t = (t - 1.0f) / dt;
        return t * t + t + t + 1.0f;
    }
    return 0.0f;
}

class PolyBlepOscillator {
    float phase = 0;
    float freq = 440.0f;
    float sampleRate = 44100.0f;

public:
    float sawtoothNext() {
        float dt = freq / sampleRate;
        float out = 2.0f * phase - 1.0f;
        out -= polyBlep(phase, dt);

        phase += dt;
        if (phase >= 1.0f) phase -= 1.0f;

        return out;
    }

    float squareNext() {
        float dt = freq / sampleRate;
        float out = phase < 0.5f ? 1.0f : -1.0f;
        out += polyBlep(phase, dt);
        out -= polyBlep(fmod(phase + 0.5f, 1.0f), dt);

        phase += dt;
        if (phase >= 1.0f) phase -= 1.0f;

        return out;
    }
};
```

## Parameter Smoothing

Avoid clicks from sudden parameter changes.

### One-Pole Smoothing

```cpp
class SmoothedValue {
    float current = 0;
    float target = 0;
    float coeff = 0;

public:
    void prepare(float smoothTimeMs, float sampleRate) {
        coeff = 1.0f - exp(-1.0f / (smoothTimeMs * sampleRate / 1000.0f));
    }

    void setTarget(float value) {
        target = value;
    }

    float next() {
        current += coeff * (target - current);
        return current;
    }

    bool isSmoothing() {
        return fabs(target - current) > 1e-6f;
    }
};
```

### Linear Ramp

```cpp
class LinearRamp {
    float current = 0;
    float target = 0;
    float step = 0;
    int samplesRemaining = 0;

public:
    void setTarget(float value, int numSamples) {
        target = value;
        samplesRemaining = numSamples;
        step = (target - current) / numSamples;
    }

    float next() {
        if (samplesRemaining > 0) {
            current += step;
            samplesRemaining--;
        } else {
            current = target;
        }
        return current;
    }
};
```

## FFT Basics

For spectral processing (vocoders, spectral effects).

### Using FFTW or KissFFT

```cpp
#include <fftw3.h>

class FFTProcessor {
    int fftSize;
    fftwf_plan forwardPlan, inversePlan;
    float* timeData;
    fftwf_complex* freqData;

public:
    void prepare(int size) {
        fftSize = size;
        timeData = fftwf_alloc_real(fftSize);
        freqData = fftwf_alloc_complex(fftSize / 2 + 1);

        forwardPlan = fftwf_plan_dft_r2c_1d(fftSize, timeData, freqData, FFTW_MEASURE);
        inversePlan = fftwf_plan_dft_c2r_1d(fftSize, freqData, timeData, FFTW_MEASURE);
    }

    void forward(const float* input) {
        memcpy(timeData, input, fftSize * sizeof(float));
        fftwf_execute(forwardPlan);
    }

    void inverse(float* output) {
        fftwf_execute(inversePlan);
        // Normalize
        for (int i = 0; i < fftSize; i++)
            output[i] = timeData[i] / fftSize;
    }

    // Access frequency bins
    float getMagnitude(int bin) {
        return sqrt(freqData[bin][0] * freqData[bin][0] +
                    freqData[bin][1] * freqData[bin][1]);
    }

    float getPhase(int bin) {
        return atan2(freqData[bin][1], freqData[bin][0]);
    }

    ~FFTProcessor() {
        fftwf_destroy_plan(forwardPlan);
        fftwf_destroy_plan(inversePlan);
        fftwf_free(timeData);
        fftwf_free(freqData);
    }
};
```

### Overlap-Add for Real-Time

```cpp
class OLAProcessor {
    int fftSize, hopSize;
    std::vector<float> inputBuffer, outputBuffer;
    std::vector<float> window;
    int inputWritePos = 0;
    int outputReadPos = 0;

public:
    void prepare(int fft, int hop) {
        fftSize = fft;
        hopSize = hop;
        inputBuffer.resize(fftSize, 0.0f);
        outputBuffer.resize(fftSize * 2, 0.0f);

        // Hann window
        window.resize(fftSize);
        for (int i = 0; i < fftSize; i++)
            window[i] = 0.5f * (1.0f - cos(2.0f * M_PI * i / fftSize));
    }

    void process(const float* input, float* output, int numSamples) {
        for (int i = 0; i < numSamples; i++) {
            // Collect input
            inputBuffer[inputWritePos] = input[i];
            inputWritePos++;

            // Process when buffer is full
            if (inputWritePos >= fftSize) {
                processFFTBlock();
                inputWritePos = fftSize - hopSize;

                // Shift input buffer
                memmove(inputBuffer.data(), inputBuffer.data() + hopSize,
                        inputWritePos * sizeof(float));
            }

            // Output
            output[i] = outputBuffer[outputReadPos];
            outputBuffer[outputReadPos] = 0;
            outputReadPos = (outputReadPos + 1) % (fftSize * 2);
        }
    }

    void processFFTBlock() {
        // Apply window, FFT, process, IFFT, overlap-add
        // (implementation depends on processing)
    }
};
```

## Math Utilities

```cpp
// Clamp
float clamp(float x, float min, float max) {
    return x < min ? min : (x > max ? max : x);
}

// Linear interpolation
float lerp(float a, float b, float t) {
    return a + t * (b - a);
}

// Map range
float mapRange(float x, float inMin, float inMax, float outMin, float outMax) {
    return outMin + (x - inMin) * (outMax - outMin) / (inMax - inMin);
}

// Soft clipping (tanh)
float softClip(float x) {
    return tanh(x);
}

// Fast tanh approximation
float fastTanh(float x) {
    float x2 = x * x;
    return x * (27.0f + x2) / (27.0f + 9.0f * x2);
}

// Denormal prevention
float flushDenormals(float x) {
    return (fabs(x) < 1e-15f) ? 0.0f : x;
}
```

## Resources

- [Audio EQ Cookbook](https://www.w3.org/2011/audio/audio-eq-cookbook.html) - Biquad formulas
- [MusicDSP Archive](https://www.musicdsp.org/) - Algorithm collection
- [DSP Guide](https://www.dspguide.com/) - Free textbook
- [Julius O. Smith III](https://ccrma.stanford.edu/~jos/) - Academic resources
