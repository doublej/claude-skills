# Common Audio Effects Implementations

Ready-to-use patterns for building audio effects.

---

## Delay Effects

### Simple Delay (Echo)

```cpp
class SimpleDelay {
    std::vector<float> buffer;
    int writePos = 0;
    float feedback = 0.5f;
    float mix = 0.5f;

public:
    void prepare(float maxDelayMs, float sampleRate) {
        int maxSamples = (int)(maxDelayMs * sampleRate / 1000.0f);
        buffer.resize(maxSamples, 0.0f);
    }

    float process(float input, float delayMs, float sampleRate) {
        int delaySamples = (int)(delayMs * sampleRate / 1000.0f);
        int readPos = (writePos - delaySamples + buffer.size()) % buffer.size();

        float delayed = buffer[readPos];
        buffer[writePos] = input + delayed * feedback;
        writePos = (writePos + 1) % buffer.size();

        return input * (1.0f - mix) + delayed * mix;
    }
};
```

**Parameters:**
- Delay Time: 1-2000ms
- Feedback: 0-95% (>100% causes runaway)
- Mix: 0-100%

---

### Ping-Pong Delay (Stereo)

```cpp
class PingPongDelay {
    SimpleDelay leftDelay, rightDelay;
    float feedback = 0.5f;

public:
    void prepare(float maxDelayMs, float sampleRate) {
        leftDelay.prepare(maxDelayMs, sampleRate);
        rightDelay.prepare(maxDelayMs, sampleRate);
    }

    void process(float& left, float& right, float delayMs, float sampleRate) {
        // Cross-feed: left → right delay, right → left delay
        float leftDelayed = leftDelay.process(right * feedback, delayMs, sampleRate);
        float rightDelayed = rightDelay.process(left * feedback, delayMs, sampleRate);

        left = left + leftDelayed;
        right = right + rightDelayed;
    }
};
```

---

### Tape Delay (with modulation + filtering)

```cpp
class TapeDelay {
    DelayLine delay;
    OnePoleFilter lowpass, highpass;
    LFO wobble;
    float feedback = 0.5f;

public:
    void prepare(float maxDelayMs, float sampleRate) {
        delay.prepare((int)(maxDelayMs * sampleRate / 1000.0f + 100));
        lowpass.setLowpass(8000.0f, sampleRate);   // Tape rolloff
        highpass.setHighpass(80.0f, sampleRate);    // Remove rumble
        wobble.setFrequency(0.5f, sampleRate);      // Wow/flutter
    }

    float process(float input, float delayMs, float sampleRate) {
        // Modulate delay time (tape speed variation)
        float modulation = wobble.next() * 0.5f;  // ±0.5ms
        float modulatedDelay = delayMs + modulation;
        int delaySamples = (int)(modulatedDelay * sampleRate / 1000.0f);

        float delayed = delay.readLinear(delaySamples);

        // Tape coloring
        delayed = lowpass.process(delayed);
        delayed = highpass.process(delayed);

        // Soft saturation
        delayed = tanh(delayed * 1.5f) / 1.5f;

        delay.write(input + delayed * feedback);
        return delayed;
    }
};
```

---

## Modulation Effects

### Chorus

```cpp
class Chorus {
    DelayLine delay;
    LFO lfo;
    float depth = 3.0f;    // ms
    float rate = 1.5f;     // Hz
    float mix = 0.5f;

public:
    void prepare(float sampleRate) {
        delay.prepare((int)(50.0f * sampleRate / 1000.0f));  // 50ms max
        lfo.setFrequency(rate, sampleRate);
    }

    float process(float input, float sampleRate) {
        float modulation = lfo.next() * depth;
        float delaySamples = (7.0f + modulation) * sampleRate / 1000.0f;  // 7ms center

        float delayed = delay.readCubic(delaySamples);
        delay.write(input);

        return input * (1.0f - mix) + delayed * mix;
    }
};
```

**Parameters:**
- Rate: 0.1-10 Hz (slow = lush, fast = vibrato)
- Depth: 1-10ms
- Mix: 0-100%

---

### Flanger

```cpp
class Flanger {
    DelayLine delay;
    LFO lfo;
    float feedback = 0.7f;
    float depth = 5.0f;    // ms
    float rate = 0.5f;     // Hz

public:
    void prepare(float sampleRate) {
        delay.prepare((int)(20.0f * sampleRate / 1000.0f));
        lfo.setFrequency(rate, sampleRate);
    }

    float process(float input, float sampleRate) {
        float modulation = (lfo.next() + 1.0f) * 0.5f;  // 0-1
        float delaySamples = (0.1f + modulation * depth) * sampleRate / 1000.0f;

        float delayed = delay.readAllpass(delaySamples);
        delay.write(input + delayed * feedback);

        return input + delayed;
    }
};
```

**Key difference from chorus:** Shorter delay (0-10ms), higher feedback, creates comb filtering.

---

### Phaser

```cpp
class AllpassStage {
    float z1 = 0;
    float coeff = 0;

public:
    void setCoeff(float c) { coeff = c; }

    float process(float input) {
        float output = coeff * (input - z1) + z1 * coeff + input * (-1);
        // Simplified: output = -input + coeff * input + z1 - coeff * z1
        output = coeff * input - z1;
        z1 = output + coeff * input;
        // Standard allpass: y[n] = -a * x[n] + x[n-1] + a * y[n-1]
        output = -coeff * input + z1;
        z1 = input + coeff * output;
        return output;
    }
};

class Phaser {
    static constexpr int numStages = 4;
    AllpassStage stages[numStages];
    LFO lfo;
    float feedback = 0.7f;
    float lastOutput = 0;

public:
    void setRate(float rate, float sampleRate) {
        lfo.setFrequency(rate, sampleRate);
    }

    float process(float input, float sampleRate) {
        // Modulate allpass frequencies
        float mod = (lfo.next() + 1.0f) * 0.5f;  // 0-1

        // Frequency range: 200Hz - 2kHz (typical)
        float minFreq = 200.0f;
        float maxFreq = 2000.0f;
        float freq = minFreq + mod * (maxFreq - minFreq);

        // Calculate allpass coefficient
        float coeff = (tan(M_PI * freq / sampleRate) - 1.0f) /
                      (tan(M_PI * freq / sampleRate) + 1.0f);

        for (int i = 0; i < numStages; i++)
            stages[i].setCoeff(coeff);

        // Process through allpass chain
        float output = input + lastOutput * feedback;
        for (int i = 0; i < numStages; i++)
            output = stages[i].process(output);

        lastOutput = output;
        return input + output * 0.5f;
    }
};
```

---

### Tremolo

```cpp
class Tremolo {
    LFO lfo;
    float depth = 0.5f;  // 0-1

public:
    void setRate(float rate, float sampleRate) {
        lfo.setFrequency(rate, sampleRate);
    }

    float process(float input) {
        float mod = (lfo.next() + 1.0f) * 0.5f;  // 0-1
        float gain = 1.0f - depth + depth * mod;
        return input * gain;
    }
};
```

---

### Vibrato

```cpp
class Vibrato {
    DelayLine delay;
    LFO lfo;
    float depth = 2.0f;  // ms

public:
    void prepare(float sampleRate) {
        delay.prepare((int)(20.0f * sampleRate / 1000.0f));
    }

    float process(float input, float sampleRate) {
        float mod = lfo.next() * depth;
        float delaySamples = (5.0f + mod) * sampleRate / 1000.0f;

        float output = delay.readCubic(delaySamples);
        delay.write(input);
        return output;
    }
};
```

---

## Dynamics

### Compressor

```cpp
class Compressor {
    float envelope = 0;
    float attackCoeff, releaseCoeff;
    float threshold = -20.0f;  // dB
    float ratio = 4.0f;
    float makeupGain = 0.0f;   // dB

public:
    void prepare(float attackMs, float releaseMs, float sampleRate) {
        attackCoeff = exp(-1.0f / (attackMs * sampleRate / 1000.0f));
        releaseCoeff = exp(-1.0f / (releaseMs * sampleRate / 1000.0f));
    }

    float process(float input) {
        // Envelope follower
        float absInput = fabs(input);
        if (absInput > envelope)
            envelope = attackCoeff * envelope + (1.0f - attackCoeff) * absInput;
        else
            envelope = releaseCoeff * envelope;

        // Gain computation
        float envDB = 20.0f * log10(envelope + 1e-6f);
        float gainDB = 0.0f;

        if (envDB > threshold)
            gainDB = (threshold - envDB) * (1.0f - 1.0f / ratio);

        gainDB += makeupGain;
        float gain = pow(10.0f, gainDB / 20.0f);

        return input * gain;
    }
};
```

**Parameters:**
- Threshold: -60 to 0 dB
- Ratio: 1:1 to 20:1 (∞:1 = limiter)
- Attack: 0.1-100ms
- Release: 10-1000ms
- Makeup Gain: 0-24 dB

---

### Limiter (Brickwall)

```cpp
class Limiter {
    float envelope = 0;
    float releaseCoeff;
    float ceiling = 0.99f;

public:
    void prepare(float releaseMs, float sampleRate) {
        releaseCoeff = exp(-1.0f / (releaseMs * sampleRate / 1000.0f));
    }

    float process(float input) {
        float absInput = fabs(input);

        // Instant attack
        if (absInput > envelope)
            envelope = absInput;
        else
            envelope = releaseCoeff * envelope;

        float gain = 1.0f;
        if (envelope > ceiling)
            gain = ceiling / envelope;

        return input * gain;
    }
};
```

---

### Gate / Expander

```cpp
class Gate {
    float envelope = 0;
    float attackCoeff, releaseCoeff, holdCoeff;
    float threshold = -40.0f;  // dB
    float range = -80.0f;      // dB (attenuation when closed)
    int holdSamples = 0;
    int holdCounter = 0;

public:
    void prepare(float attackMs, float holdMs, float releaseMs, float sampleRate) {
        attackCoeff = exp(-1.0f / (attackMs * sampleRate / 1000.0f));
        releaseCoeff = exp(-1.0f / (releaseMs * sampleRate / 1000.0f));
        holdSamples = (int)(holdMs * sampleRate / 1000.0f);
    }

    float process(float input) {
        float absInput = fabs(input);
        float inputDB = 20.0f * log10(absInput + 1e-6f);

        float targetGain;
        if (inputDB > threshold) {
            targetGain = 1.0f;
            holdCounter = holdSamples;
        } else if (holdCounter > 0) {
            targetGain = 1.0f;
            holdCounter--;
        } else {
            targetGain = pow(10.0f, range / 20.0f);
        }

        // Smooth gain
        if (targetGain > envelope)
            envelope = attackCoeff * envelope + (1.0f - attackCoeff) * targetGain;
        else
            envelope = releaseCoeff * envelope + (1.0f - releaseCoeff) * targetGain;

        return input * envelope;
    }
};
```

---

## Distortion

### Soft Clipping (Tanh)

```cpp
float softClip(float input, float drive) {
    return tanh(input * drive);
}
```

---

### Hard Clipping

```cpp
float hardClip(float input, float threshold) {
    if (input > threshold) return threshold;
    if (input < -threshold) return -threshold;
    return input;
}
```

---

### Tube Saturation

```cpp
float tubeSaturation(float input, float drive) {
    // Asymmetric soft clipping
    float x = input * drive;
    if (x >= 0)
        return 1.0f - exp(-x);
    else
        return -1.0f + exp(x);
}
```

---

### Waveshaper (Polynomial)

```cpp
float waveshape(float input, float amount) {
    // Chebyshev polynomial (adds harmonics)
    float x = input;
    float x2 = x * x;
    float x3 = x2 * x;

    // Mix between clean and shaped
    float shaped = x - amount * x3 / 3.0f;
    return shaped;
}
```

---

### Bitcrusher

```cpp
class Bitcrusher {
    float lastSample = 0;
    int sampleCounter = 0;

public:
    float process(float input, int bitDepth, int sampleRateReduction) {
        // Sample rate reduction
        sampleCounter++;
        if (sampleCounter >= sampleRateReduction) {
            lastSample = input;
            sampleCounter = 0;
        }

        // Bit depth reduction
        float levels = pow(2.0f, bitDepth);
        float quantized = round(lastSample * levels) / levels;

        return quantized;
    }
};
```

---

## Reverb

### Simple Comb Filter Reverb

```cpp
class CombFilter {
    std::vector<float> buffer;
    int writePos = 0;
    float feedback = 0.8f;
    float damping = 0.2f;
    float lastOutput = 0;

public:
    void prepare(int delaySamples) {
        buffer.resize(delaySamples, 0.0f);
    }

    float process(float input) {
        float output = buffer[writePos];

        // Lowpass in feedback path (damping)
        lastOutput = output * (1.0f - damping) + lastOutput * damping;

        buffer[writePos] = input + lastOutput * feedback;
        writePos = (writePos + 1) % buffer.size();

        return output;
    }
};
```

---

### Schroeder Reverb

```cpp
class SchroederReverb {
    CombFilter combs[4];
    AllpassFilter allpasses[2];

public:
    void prepare(float sampleRate) {
        // Comb filter delays (prime numbers for diffusion)
        combs[0].prepare((int)(29.7f * sampleRate / 1000.0f));
        combs[1].prepare((int)(37.1f * sampleRate / 1000.0f));
        combs[2].prepare((int)(41.1f * sampleRate / 1000.0f));
        combs[3].prepare((int)(43.7f * sampleRate / 1000.0f));

        // Allpass delays
        allpasses[0].prepare((int)(5.0f * sampleRate / 1000.0f));
        allpasses[1].prepare((int)(1.7f * sampleRate / 1000.0f));
    }

    float process(float input) {
        // Parallel comb filters
        float combOutput = 0;
        for (int i = 0; i < 4; i++)
            combOutput += combs[i].process(input);
        combOutput /= 4.0f;

        // Series allpass filters
        float output = combOutput;
        for (int i = 0; i < 2; i++)
            output = allpasses[i].process(output);

        return output;
    }
};
```

---

### Freeverb (Simplified)

```cpp
class Freeverb {
    static constexpr int numCombs = 8;
    static constexpr int numAllpasses = 4;

    CombFilter combsL[numCombs], combsR[numCombs];
    AllpassFilter allpassesL[numAllpasses], allpassesR[numAllpasses];

    float roomSize = 0.8f;
    float damping = 0.5f;
    float wet = 0.3f;
    float width = 1.0f;

    // Comb delays (samples at 44.1kHz)
    const int combDelays[8] = {1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617};
    const int allpassDelays[4] = {556, 441, 341, 225};
    const int stereoSpread = 23;  // Stereo offset

public:
    void prepare(float sampleRate) {
        float scale = sampleRate / 44100.0f;

        for (int i = 0; i < numCombs; i++) {
            combsL[i].prepare((int)(combDelays[i] * scale));
            combsR[i].prepare((int)((combDelays[i] + stereoSpread) * scale));
            combsL[i].setFeedback(roomSize);
            combsR[i].setFeedback(roomSize);
            combsL[i].setDamping(damping);
            combsR[i].setDamping(damping);
        }

        for (int i = 0; i < numAllpasses; i++) {
            allpassesL[i].prepare((int)(allpassDelays[i] * scale));
            allpassesR[i].prepare((int)((allpassDelays[i] + stereoSpread) * scale));
            allpassesL[i].setFeedback(0.5f);
            allpassesR[i].setFeedback(0.5f);
        }
    }

    void process(float& left, float& right) {
        float inputL = left;
        float inputR = right;
        float mono = (inputL + inputR) * 0.5f;

        // Parallel combs
        float outL = 0, outR = 0;
        for (int i = 0; i < numCombs; i++) {
            outL += combsL[i].process(mono);
            outR += combsR[i].process(mono);
        }

        // Series allpasses
        for (int i = 0; i < numAllpasses; i++) {
            outL = allpassesL[i].process(outL);
            outR = allpassesR[i].process(outR);
        }

        // Stereo width
        float wet1 = wet * (width / 2.0f + 0.5f);
        float wet2 = wet * ((1.0f - width) / 2.0f);

        left = outL * wet1 + outR * wet2 + inputL * (1.0f - wet);
        right = outR * wet1 + outL * wet2 + inputR * (1.0f - wet);
    }
};
```

---

## EQ

### 3-Band EQ

```cpp
class ThreeBandEQ {
    Biquad lowShelf, mid, highShelf;

public:
    void prepare(float sampleRate) {
        // Default: 200Hz low, 1kHz mid, 4kHz high
        lowShelf.setLowShelf(200.0f, 0.707f, 0.0f, sampleRate);
        mid.setPeakingEQ(1000.0f, 1.0f, 0.0f, sampleRate);
        highShelf.setHighShelf(4000.0f, 0.707f, 0.0f, sampleRate);
    }

    void setLowGain(float gainDB, float sampleRate) {
        lowShelf.setLowShelf(200.0f, 0.707f, gainDB, sampleRate);
    }

    void setMidGain(float gainDB, float sampleRate) {
        mid.setPeakingEQ(1000.0f, 1.0f, gainDB, sampleRate);
    }

    void setHighGain(float gainDB, float sampleRate) {
        highShelf.setHighShelf(4000.0f, 0.707f, gainDB, sampleRate);
    }

    float process(float input) {
        float output = lowShelf.process(input);
        output = mid.process(output);
        output = highShelf.process(output);
        return output;
    }
};
```

---

### Parametric EQ Band

```cpp
class ParametricBand {
    Biquad filter;
    float frequency = 1000.0f;
    float gain = 0.0f;
    float q = 1.0f;

public:
    void setParameters(float freq, float gainDB, float qValue, float sampleRate) {
        frequency = freq;
        gain = gainDB;
        q = qValue;
        filter.setPeakingEQ(frequency, q, gain, sampleRate);
    }

    float process(float input) {
        return filter.process(input);
    }
};
```

---

## Utility Effects

### Stereo Widener

```cpp
void stereoWiden(float& left, float& right, float width) {
    // Mid-Side processing
    float mid = (left + right) * 0.5f;
    float side = (left - right) * 0.5f;

    // Adjust width
    side *= width;

    // Convert back to L/R
    left = mid + side;
    right = mid - side;
}
```

---

### Panning (Equal Power)

```cpp
void pan(float input, float& left, float& right, float pan) {
    // pan: -1 (left) to +1 (right)
    float angle = (pan + 1.0f) * 0.25f * M_PI;  // 0 to π/2
    left = input * cos(angle);
    right = input * sin(angle);
}
```

---

### DC Blocker

```cpp
class DCBlocker {
    float x1 = 0, y1 = 0;
    float R = 0.995f;  // Pole near z=1

public:
    float process(float input) {
        float output = input - x1 + R * y1;
        x1 = input;
        y1 = output;
        return output;
    }
};
```

---

## Resources

- [Audio EQ Cookbook](https://www.w3.org/2011/audio/audio-eq-cookbook.html)
- [MusicDSP.org](https://www.musicdsp.org/)
- [Freeverb Implementation](https://ccrma.stanford.edu/~jos/pasp/Freeverb.html)
