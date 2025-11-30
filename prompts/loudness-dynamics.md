# Loudness and Dynamics Analysis

## Prompt

```
Listen to the voice sample I've provided and analyze the loudness and dynamic characteristics.

Please provide:

1. **Overall Loudness Assessment**
   - Is the recording at an appropriate level?
   - Does it sound properly normalized or is it too quiet/loud?
   - Estimate how close to broadcast standards (-16 LUFS for podcasts, -14 LUFS for streaming) it appears to be

2. **Dynamic Range**
   - Rate the dynamic range: narrow (compressed), moderate, or wide
   - Are there significant volume differences between loud and soft parts?
   - Estimate the approximate dynamic range in dB if possible

3. **Consistency Analysis**
   - Is the volume consistent throughout, or are there dips/spikes?
   - Are word beginnings/endings at consistent levels?
   - Note any problematic volume variations

4. **Peak Assessment**
   - Are there any noticeable peaks or clipping?
   - Do plosives (P, B, T sounds) cause level spikes?
   - Is there any audible distortion?

5. **Recommendations**
   - Would this benefit from compression? If so, suggest intensity (light/moderate/heavy)
   - Normalization recommendations
   - Any other dynamics processing suggestions

Format your response as a structured report with clear sections.
```

## What This Analyzes

- **Loudness level**: Whether the recording is at appropriate broadcast/streaming levels
- **Dynamic range**: The difference between quietest and loudest parts
- **Volume consistency**: Stability of levels throughout the recording
- **Peaks and transients**: Problematic spikes that may need limiting
- **Compression needs**: Whether dynamics processing would help

## Target Loudness Standards

| Platform/Format | Target LUFS |
|-----------------|-------------|
| Podcast | -16 LUFS |
| YouTube | -14 LUFS |
| Spotify | -14 LUFS |
| Broadcast TV | -24 LUFS |
| Audiobook (ACX) | -18 to -23 LUFS |
