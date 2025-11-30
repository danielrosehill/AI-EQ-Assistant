#!/usr/bin/env python3
"""
AI-EQ Voice Analysis Script

Comprehensive voice analysis including:
- Accent/dialect detection via OpenAI
- Spectral analysis via librosa
- Frequency characteristics and formant estimation
- EQ recommendations based on voice profile
"""

import json
import sys
import base64
import os
from pathlib import Path
from datetime import datetime

import numpy as np
import librosa
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def encode_audio_to_base64(audio_path: Path) -> str:
    """Read and encode audio file to base64."""
    with open(audio_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def analyze_audio_characteristics(audio_path: Path, output_dir: Path) -> dict:
    """
    Analyze audio characteristics using librosa.

    Returns frequency analysis, generates spectrograms.
    """
    # Load audio
    y, sr = librosa.load(str(audio_path), sr=None)
    duration = librosa.get_duration(y=y, sr=sr)

    # Fundamental frequency (pitch) analysis
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7')
    )
    f0_valid = f0[~np.isnan(f0)]

    if len(f0_valid) > 0:
        f0_mean = float(np.mean(f0_valid))
        f0_min = float(np.min(f0_valid))
        f0_max = float(np.max(f0_valid))
        f0_std = float(np.std(f0_valid))
    else:
        f0_mean = f0_min = f0_max = f0_std = 0.0

    # Spectral analysis
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]

    # RMS energy
    rms = librosa.feature.rms(y=y)[0]

    # Zero crossing rate (relates to noisiness/breathiness)
    zcr = librosa.feature.zero_crossing_rate(y)[0]

    # MFCCs for voice quality
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # Generate spectrograms
    spectrogram_path = output_dir / "spectrogram.png"
    mel_spectrogram_path = output_dir / "mel_spectrogram.png"
    frequency_plot_path = output_dir / "frequency_analysis.png"

    # Regular spectrogram
    plt.figure(figsize=(12, 4))
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz', cmap='magma')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.tight_layout()
    plt.savefig(spectrogram_path, dpi=150, bbox_inches='tight')
    plt.close()

    # Mel spectrogram
    plt.figure(figsize=(12, 4))
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_db = librosa.power_to_db(S, ref=np.max)
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='mel', cmap='magma')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    plt.tight_layout()
    plt.savefig(mel_spectrogram_path, dpi=150, bbox_inches='tight')
    plt.close()

    # Frequency analysis plot
    fig, axes = plt.subplots(3, 1, figsize=(12, 8))

    times = librosa.times_like(spectral_centroids, sr=sr)

    # Spectral centroid
    axes[0].plot(times, spectral_centroids, color='#2563eb', linewidth=0.8)
    axes[0].set_ylabel('Hz')
    axes[0].set_title('Spectral Centroid (Brightness)')
    axes[0].axhline(y=np.mean(spectral_centroids), color='red', linestyle='--', alpha=0.7, label=f'Mean: {np.mean(spectral_centroids):.0f} Hz')
    axes[0].legend()

    # F0 (pitch)
    f0_times = librosa.times_like(f0, sr=sr)
    axes[1].plot(f0_times, f0, color='#16a34a', linewidth=0.8)
    axes[1].set_ylabel('Hz')
    axes[1].set_title('Fundamental Frequency (Pitch)')
    if f0_mean > 0:
        axes[1].axhline(y=f0_mean, color='red', linestyle='--', alpha=0.7, label=f'Mean: {f0_mean:.0f} Hz')
        axes[1].legend()

    # RMS Energy
    rms_times = librosa.times_like(rms, sr=sr)
    axes[2].plot(rms_times, rms, color='#dc2626', linewidth=0.8)
    axes[2].set_ylabel('Amplitude')
    axes[2].set_title('RMS Energy (Loudness)')
    axes[2].set_xlabel('Time (s)')

    plt.tight_layout()
    plt.savefig(frequency_plot_path, dpi=150, bbox_inches='tight')
    plt.close()

    # Determine voice characteristics for EQ recommendations
    voice_characteristics = categorize_voice(f0_mean, np.mean(spectral_centroids), np.mean(zcr))

    return {
        "duration_seconds": round(duration, 2),
        "sample_rate": sr,
        "fundamental_frequency": {
            "mean_hz": round(f0_mean, 1),
            "min_hz": round(f0_min, 1),
            "max_hz": round(f0_max, 1),
            "std_hz": round(f0_std, 1),
            "range_hz": round(f0_max - f0_min, 1),
        },
        "spectral_characteristics": {
            "centroid_mean_hz": round(float(np.mean(spectral_centroids)), 1),
            "rolloff_mean_hz": round(float(np.mean(spectral_rolloff)), 1),
            "bandwidth_mean_hz": round(float(np.mean(spectral_bandwidth)), 1),
        },
        "energy": {
            "rms_mean": round(float(np.mean(rms)), 4),
            "rms_max": round(float(np.max(rms)), 4),
            "dynamic_range_db": round(float(20 * np.log10(np.max(rms) / (np.mean(rms) + 1e-10))), 1),
        },
        "voice_quality": {
            "zero_crossing_rate_mean": round(float(np.mean(zcr)), 4),
            "breathiness_indicator": "high" if np.mean(zcr) > 0.1 else "moderate" if np.mean(zcr) > 0.05 else "low",
        },
        "voice_characteristics": voice_characteristics,
        "plots": {
            "spectrogram": str(spectrogram_path),
            "mel_spectrogram": str(mel_spectrogram_path),
            "frequency_analysis": str(frequency_plot_path),
        }
    }


def categorize_voice(f0_mean: float, centroid_mean: float, zcr_mean: float) -> dict:
    """Categorize voice based on acoustic features."""
    # Voice type based on fundamental frequency
    if f0_mean < 130:
        voice_type = "bass"
        voice_range = "low"
    elif f0_mean < 180:
        voice_type = "baritone" if f0_mean < 155 else "tenor"
        voice_range = "low-mid"
    elif f0_mean < 250:
        voice_type = "alto" if f0_mean < 220 else "mezzo-soprano"
        voice_range = "mid"
    else:
        voice_type = "soprano"
        voice_range = "high"

    # Brightness based on spectral centroid
    if centroid_mean < 1500:
        brightness = "dark/warm"
    elif centroid_mean < 2500:
        brightness = "balanced"
    elif centroid_mean < 3500:
        brightness = "bright"
    else:
        brightness = "very bright/sibilant"

    return {
        "voice_type": voice_type,
        "voice_range": voice_range,
        "brightness": brightness,
    }


def generate_eq_recommendations(audio_analysis: dict, accent_analysis: dict) -> dict:
    """Generate EQ recommendations based on voice analysis."""
    f0 = audio_analysis["fundamental_frequency"]["mean_hz"]
    centroid = audio_analysis["spectral_characteristics"]["centroid_mean_hz"]
    breathiness = audio_analysis["voice_quality"]["breathiness_indicator"]
    voice_chars = audio_analysis["voice_characteristics"]

    recommendations = []
    eq_bands = []

    # Low-end recommendations
    if f0 > 0:
        # High-pass filter recommendation
        hp_freq = max(60, f0 * 0.5)
        recommendations.append(f"Apply high-pass filter at {hp_freq:.0f} Hz to remove rumble without affecting voice fundamentals")
        eq_bands.append({
            "type": "high-pass",
            "frequency_hz": round(hp_freq),
            "description": "Remove sub-bass rumble"
        })

        # Fundamental boost/cut
        if voice_chars["voice_range"] in ["low", "low-mid"]:
            recommendations.append(f"Consider subtle boost (+1-2 dB) around {f0:.0f} Hz to add warmth and body")
            eq_bands.append({
                "type": "bell",
                "frequency_hz": round(f0),
                "gain_db": "+1 to +2",
                "q": 1.5,
                "description": "Add warmth and body"
            })

    # Mid-range presence
    presence_freq = 2500 if f0 < 200 else 3000
    recommendations.append(f"Boost presence around {presence_freq} Hz (+2-3 dB) for clarity and intelligibility")
    eq_bands.append({
        "type": "bell",
        "frequency_hz": presence_freq,
        "gain_db": "+2 to +3",
        "q": 1.0,
        "description": "Enhance presence and clarity"
    })

    # Brightness control
    if voice_chars["brightness"] == "very bright/sibilant":
        recommendations.append("Apply de-esser or reduce 5-8 kHz range (-2-4 dB) to control sibilance")
        eq_bands.append({
            "type": "bell",
            "frequency_hz": 6500,
            "gain_db": "-2 to -4",
            "q": 2.0,
            "description": "Control sibilance"
        })
    elif voice_chars["brightness"] == "dark/warm":
        recommendations.append("Add air and sparkle with a gentle high shelf boost (+2-3 dB) above 10 kHz")
        eq_bands.append({
            "type": "high-shelf",
            "frequency_hz": 10000,
            "gain_db": "+2 to +3",
            "description": "Add air and sparkle"
        })

    # Breathiness handling
    if breathiness == "high":
        recommendations.append("Consider reducing 4-6 kHz slightly (-1-2 dB) to manage breathiness, or embrace it for intimacy")
        eq_bands.append({
            "type": "bell",
            "frequency_hz": 5000,
            "gain_db": "-1 to -2",
            "q": 1.5,
            "description": "Control breathiness (optional)"
        })

    # Mud reduction
    recommendations.append("Cut 200-400 Hz range slightly (-1-3 dB) if voice sounds muddy or boxy")
    eq_bands.append({
        "type": "bell",
        "frequency_hz": 300,
        "gain_db": "-1 to -3",
        "q": 1.0,
        "description": "Reduce muddiness (if needed)"
    })

    # Accent-specific recommendations
    accent = accent_analysis.get("primary_accent", "").lower()
    accent_tips = []

    if "irish" in accent or "celtic" in accent:
        accent_tips.append("Irish accents often have melodic qualities - preserve natural intonation by avoiding heavy compression")
        accent_tips.append("The characteristic 'lilt' sits in the 1-3 kHz range - be careful not to over-boost this region")
    elif "british" in accent or "english" in accent:
        accent_tips.append("RP/British accents may benefit from slight presence boost for clarity")
    elif "american" in accent:
        accent_tips.append("American accents often have strong 'r' sounds - watch the 2-3 kHz region")

    return {
        "summary": f"Voice profile: {voice_chars['voice_type']} with {voice_chars['brightness']} tonal quality",
        "recommendations": recommendations,
        "eq_bands": eq_bands,
        "accent_specific_tips": accent_tips,
        "processing_suggestions": [
            "Apply subtle compression (2:1 to 4:1 ratio) for consistent levels",
            "Use a noise gate if there's background noise between phrases",
            "Consider gentle saturation/warmth for added character",
        ]
    }


def analyze_accent(audio_path: Path) -> dict:
    """Analyze accent/dialect using OpenAI's audio model."""
    client = OpenAI()

    audio_data = encode_audio_to_base64(audio_path)

    system_prompt = """You are an expert linguist and phonetician specializing in accent and dialect analysis.
Analyze the provided voice recording and identify:

1. The primary accent or dialect detected
2. Your confidence level (high/medium/low)
3. Specific phonetic features that led to your conclusion
4. Any secondary accent influences if present
5. Regional and cultural context

Respond in JSON format with the following structure:
{
    "primary_accent": "Name of accent/dialect",
    "confidence": "high|medium|low",
    "confidence_percentage": 0-100,
    "phonetic_features": ["list", "of", "observed", "features"],
    "secondary_influences": ["any", "other", "accent", "influences"],
    "regional_context": "Brief description of where this accent is typically found",
    "speech_characteristics": {
        "tempo": "description of speech speed",
        "intonation": "description of pitch patterns",
        "notable_sounds": ["specific", "sound", "observations"]
    },
    "analysis_notes": "Any additional observations about the speaker's voice"
}"""

    response = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please analyze this voice recording and identify the speaker's accent or dialect. Provide your analysis in the JSON format specified. Return ONLY the JSON object, no markdown.",
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": audio_data,
                            "format": "mp3",
                        },
                    },
                ],
            },
        ],
    )

    response_text = response.choices[0].message.content.strip()
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1])

    return json.loads(response_text)


def main():
    if len(sys.argv) < 2:
        samples_dir = Path(__file__).parent / "voice-samples"
        audio_files = list(samples_dir.glob("*.mp3")) + list(samples_dir.glob("*.wav"))
        if not audio_files:
            print("Usage: python analyze_voice.py <audio_file>")
            print("Or place audio files in voice-samples/ directory")
            sys.exit(1)
        audio_path = audio_files[0]
    else:
        audio_path = Path(sys.argv[1])

    if not audio_path.exists():
        print(f"Error: File not found: {audio_path}")
        sys.exit(1)

    # Setup output directory
    output_dir = Path(__file__).parent / "analysis"
    output_dir.mkdir(exist_ok=True)

    print(f"Analyzing: {audio_path.name}")
    print("=" * 50)

    # Step 1: Audio characteristics analysis
    print("\n[1/3] Analyzing audio characteristics...")
    audio_analysis = analyze_audio_characteristics(audio_path, output_dir)
    print(f"      Duration: {audio_analysis['duration_seconds']}s")
    print(f"      Fundamental frequency: {audio_analysis['fundamental_frequency']['mean_hz']} Hz")
    print(f"      Voice type: {audio_analysis['voice_characteristics']['voice_type']}")

    # Step 2: Accent detection
    print("\n[2/3] Detecting accent via OpenAI...")
    accent_analysis = analyze_accent(audio_path)
    print(f"      Detected: {accent_analysis['primary_accent']}")
    print(f"      Confidence: {accent_analysis['confidence']} ({accent_analysis.get('confidence_percentage', 'N/A')}%)")

    # Step 3: Generate EQ recommendations
    print("\n[3/3] Generating EQ recommendations...")
    eq_recommendations = generate_eq_recommendations(audio_analysis, accent_analysis)
    print(f"      {eq_recommendations['summary']}")

    # Compile full result
    result = {
        "metadata": {
            "audio_file": audio_path.name,
            "analysis_timestamp": datetime.now().isoformat(),
            "models_used": {
                "audio_analysis": "librosa",
                "accent_detection": "gpt-4o-audio-preview",
            }
        },
        "audio_analysis": audio_analysis,
        "accent_analysis": accent_analysis,
        "eq_recommendations": eq_recommendations,
    }

    # Save JSON output
    output_file = output_dir / f"{audio_path.stem}_analysis.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n{'=' * 50}")
    print(f"Analysis complete!")
    print(f"Results saved to: {output_file}")
    print(f"Spectrograms saved to: {output_dir}/")

    # Print summary
    print(f"\n{'=' * 50}")
    print("SUMMARY")
    print("=" * 50)
    print(f"\nAccent: {accent_analysis['primary_accent']}")
    print(f"Voice: {audio_analysis['voice_characteristics']['voice_type']} ({audio_analysis['voice_characteristics']['brightness']})")
    print(f"\nTop EQ Recommendations:")
    for i, rec in enumerate(eq_recommendations['recommendations'][:3], 1):
        print(f"  {i}. {rec}")


if __name__ == "__main__":
    main()
