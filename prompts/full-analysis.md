# Complete Voice Analysis

## Prompt

```
Listen to the voice sample I've provided and perform a comprehensive voice analysis covering all aspects of the recording.

Please provide a complete report with the following sections:

---

## 1. SPEAKING RATE & PACING

- Estimated Words Per Minute (WPM)
- Pacing consistency (1-5 scale)
- Syllable rate observations
- Pause patterns and timing

---

## 2. PITCH ANALYSIS

- Estimated mean fundamental frequency (F0) in Hz
- Pitch range (lowest to highest Hz)
- Pitch variability (1-5: monotone to expressive)
- Intonation patterns
- Voice register assessment

---

## 3. LOUDNESS & DYNAMICS

- Overall loudness assessment
- Dynamic range (narrow/moderate/wide)
- Volume consistency
- Peak/clipping observations
- Estimated proximity to broadcast standards (-16 LUFS)

---

## 4. FREQUENCY ANALYSIS & EQ RECOMMENDATIONS

Assess each frequency band:
- Sub-bass (20-80 Hz)
- Bass/Body (80-250 Hz)
- Low-mids (250-500 Hz)
- Midrange (500-2000 Hz)
- Presence (2000-4000 Hz)
- Brilliance (4000-8000 Hz)
- Highs (8000-16000 Hz)

Provide specific EQ recommendations:
| Frequency (Hz) | Gain (dB) | Q/Type | Reason |
|----------------|-----------|--------|--------|

High-pass filter recommendation:
- Cutoff frequency
- Slope

---

## 5. COMPRESSION SETTINGS

| Parameter | Recommended Value | Reasoning |
|-----------|-------------------|-----------|
| Threshold | | |
| Ratio | | |
| Attack | | |
| Release | | |
| Makeup Gain | | |

De-essing needed? (Y/N, if yes: target frequency and intensity)

---

## 6. VOICE QUALITY (GRBAS)

| Parameter | Score (0-3) | Notes |
|-----------|-------------|-------|
| Grade | | |
| Roughness | | |
| Breathiness | | |
| Asthenia | | |
| Strain | | |

---

## 7. PERCEPTUAL QUALITY (MOS-Style)

| Aspect | Rating (1-5) |
|--------|--------------|
| Overall Quality | |
| Listening Effort | |
| Naturalness | |
| Comprehension | |
| Pleasantness | |

---

## 8. SPEECH & LINGUISTIC ANALYSIS

- Accent identification
- Pronunciation clarity (1-5)
- Articulation quality
- Prosody assessment
- TTS/STT suitability (1-5)

---

## 9. OVERALL ASSESSMENT

**Strengths:**
- (list key positive attributes)

**Areas for Improvement:**
- (list actionable improvements)

**Best Use Cases:**
- (podcast, audiobook, commercial, etc.)

**Overall Rating:** ___/10

---

## 10. RECOMMENDED PROCESSING CHAIN

Suggest the complete signal chain order:
1. (first processor)
2. (second processor)
3. (etc.)

---

Provide specific, actionable recommendations throughout. Include exact values where applicable (Hz, dB, ms, ratios).
```

## What This Covers

This comprehensive prompt requests analysis of:

1. **Speaking Rate** - WPM and pacing
2. **Pitch** - F0, range, and variability
3. **Loudness** - Levels and dynamics
4. **Frequency Content** - Full-spectrum EQ analysis
5. **Compression** - Complete dynamics processing recommendations
6. **Voice Quality** - Clinical GRBAS assessment
7. **Perceptual Quality** - MOS-style subjective ratings
8. **Speech Patterns** - Accent, articulation, prosody
9. **Overall Assessment** - Strengths, weaknesses, use cases
10. **Processing Chain** - Complete recommended signal flow

This is equivalent to running all individual prompts and getting a unified report.
