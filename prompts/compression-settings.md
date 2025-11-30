# Compression Settings Recommendations

## Prompt

```
Listen to the voice sample I've provided and recommend compression settings.

Please analyze the dynamics and provide:

1. **Dynamics Assessment**
   - How dynamic is the performance? (Rate: very consistent, moderate variation, highly dynamic)
   - Are there problematic peaks or level drops?
   - Does the voice need taming or is it already well-controlled?

2. **Compression Recommendations**
   Provide specific settings:

   | Parameter | Recommended Value | Reasoning |
   |-----------|-------------------|-----------|
   | Threshold | ___ dB | |
   | Ratio | ___:1 | |
   | Attack | ___ ms | |
   | Release | ___ ms | |
   | Knee | Hard/Soft | |
   | Makeup Gain | ___ dB | |

3. **Compression Style**
   - Is gentle leveling (2:1-3:1) or more aggressive compression (4:1+) appropriate?
   - Would parallel compression be beneficial?
   - Is multi-band compression needed, or is broadband sufficient?

4. **Limiting Recommendations**
   - Is a limiter needed for peaks?
   - Suggested ceiling level (-1 dB, -0.5 dB, etc.)
   - Peak reduction amount if applicable

5. **De-essing (if applicable)**
   - Is de-essing needed?
   - Target frequency range for de-esser
   - Intensity recommendation (light, moderate, aggressive)

6. **Processing Chain Order**
   Suggest the order of dynamics processing:
   - Where should compression sit relative to EQ?
   - Should there be multiple stages of compression?

Provide specific, actionable settings suitable for voice/podcast/voiceover work.
```

## What This Analyzes

- **Dynamic range**: How much level variation exists
- **Transient behavior**: How the voice attacks words/phrases
- **Consistency needs**: Whether leveling is required
- **Peak management**: Whether limiting is needed
- **Sibilance levels**: Whether de-essing would help

## Typical Compression Settings for Voice

| Use Case | Threshold | Ratio | Attack | Release |
|----------|-----------|-------|--------|---------|
| Gentle leveling | -18 to -15 dB | 2:1-3:1 | 10-20 ms | 100-150 ms |
| Podcast/broadcast | -20 to -16 dB | 3:1-4:1 | 5-15 ms | 80-120 ms |
| Aggressive (VO) | -24 to -18 dB | 4:1-6:1 | 2-10 ms | 50-100 ms |
| Limiting | -6 to -3 dB | 10:1+ | <1 ms | 50-100 ms |
