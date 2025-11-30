# EQ Recommendations

## Prompt

```
Listen to the voice sample I've provided and provide specific EQ (equalization) recommendations.

Please analyze the frequency content and provide:

1. **Frequency Band Assessment**
   Evaluate each band and note any issues:
   - **Sub-bass (20-80 Hz)**: Rumble, handling noise, HVAC noise
   - **Bass/Body (80-250 Hz)**: Warmth, proximity effect, boominess
   - **Low-mids (250-500 Hz)**: Boxiness, muddiness, nasal quality
   - **Midrange (500-2000 Hz)**: Presence, honkiness, intelligibility
   - **Upper-mids/Presence (2000-4000 Hz)**: Clarity, harshness, sibilance buildup
   - **Brilliance (4000-8000 Hz)**: Air, sibilance, detail
   - **High frequencies (8000-16000 Hz)**: Sparkle, noise, excessive brightness

2. **Specific EQ Moves**
   For each recommended adjustment, provide:
   - Center frequency (Hz)
   - Gain adjustment (dB, positive or negative)
   - Q/Bandwidth (narrow, medium, wide, or shelf)
   - Reasoning for the adjustment

   Format as a table:
   | Frequency (Hz) | Gain (dB) | Q/Type | Reason |
   |----------------|-----------|--------|--------|

3. **High-Pass Filter Recommendation**
   - Suggested cutoff frequency
   - Slope recommendation (12dB/oct, 18dB/oct, 24dB/oct)
   - Reasoning

4. **Problem Areas**
   - Note any specific issues detected (sibilance, plosives, room resonances)
   - Frequency ranges to treat with care

5. **Processing Order Suggestion**
   - Where should EQ sit in the signal chain?
   - Pre-compression vs post-compression EQ recommendations

Provide specific, actionable recommendations with exact frequency and gain values.
```

## What This Analyzes

- **Frequency balance**: How energy is distributed across the spectrum
- **Problem frequencies**: Resonances, muddiness, harshness
- **Tonal character**: Warm, bright, thin, boomy, etc.
- **Room/recording issues**: Resonances from the recording environment
- **Sibilance and plosives**: High-frequency and transient issues

## Common EQ Reference Points

| Frequency | Typical Voice Characteristic |
|-----------|------------------------------|
| 80-100 Hz | Rumble, handling noise |
| 100-200 Hz | Body, warmth, proximity effect |
| 250-400 Hz | Boxiness, muddiness |
| 800-1000 Hz | Nasal quality |
| 1-2 kHz | Intelligibility, honk |
| 2-4 kHz | Presence, clarity |
| 4-7 kHz | Sibilance (S, T sounds) |
| 8-12 kHz | Air, brightness |
