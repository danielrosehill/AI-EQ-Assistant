# Voice Analysis Prompts

This folder contains pre-written prompts for use with Google Gemini (or other multimodal LLMs that support audio input). Each prompt focuses on a specific aspect of voice analysis.

## How to Use

1. Upload your voice sample to Gemini (via [Google AI Studio](https://aistudio.google.com/) or the API)
2. Copy and paste the relevant prompt
3. Replace `[VOICE SAMPLE]` with a reference to your uploaded audio file (if using the web interface, simply mention "the audio file I uploaded" or similar)

## Available Prompts

| File | Analysis Type | Description |
|------|---------------|-------------|
| [speaking-rate-wpm.md](speaking-rate-wpm.md) | Speaking Rate | Calculate words per minute and pacing analysis |
| [pitch-analysis.md](pitch-analysis.md) | Pitch/F0 Analysis | Fundamental frequency, range, and variability |
| [loudness-dynamics.md](loudness-dynamics.md) | Loudness & Dynamics | RMS levels, dynamic range, and consistency |
| [eq-recommendations.md](eq-recommendations.md) | EQ Settings | Parametric EQ recommendations with frequency, gain, and Q values |
| [compression-settings.md](compression-settings.md) | Compression | Threshold, ratio, attack, release, and makeup gain |
| [voice-quality-assessment.md](voice-quality-assessment.md) | Voice Quality | GRBAS scale, MOS-style ratings, and overall quality |
| [speech-linguistic.md](speech-linguistic.md) | Speech & Linguistic | Accent, pronunciation, articulation, and prosody |
| [full-analysis.md](full-analysis.md) | Complete Analysis | Comprehensive analysis covering all aspects |

## Tips

- For best results, use a 30-60 second voice sample of natural speech
- Use raw, unprocessed audio for accurate analysis
- These prompts work with Gemini 1.5 Pro/Flash and other multimodal models that support audio

## Note

These prompts are designed to work independently of the main Python tool. They provide a manual alternative for users who want to run specific analyses without setting up the full environment.
