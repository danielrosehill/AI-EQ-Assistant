#!/usr/bin/env python3
"""
AI-EQ PDF Report Generator

Generates a comprehensive PDF report with:
- Accent/dialect analysis
- Spectrograms and frequency plots
- Voice characteristics
- EQ recommendations
"""

import json
import sys
from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    Image,
    PageBreak,
    KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def create_styles():
    """Create custom paragraph styles for the report."""
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Heading1"],
            fontSize=26,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1a365d"),
        )
    )

    styles.add(
        ParagraphStyle(
            name="Subtitle",
            parent=styles["Normal"],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4a5568"),
            spaceAfter=30,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeader",
            parent=styles["Heading2"],
            fontSize=16,
            spaceBefore=25,
            spaceAfter=12,
            textColor=colors.HexColor("#2c5282"),
        )
    )

    styles.add(
        ParagraphStyle(
            name="SubsectionHeader",
            parent=styles["Heading3"],
            fontSize=12,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.HexColor("#4a5568"),
            fontName="Helvetica-Bold",
        )
    )

    styles.add(
        ParagraphStyle(
            name="AccentResult",
            parent=styles["Normal"],
            fontSize=20,
            spaceBefore=10,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#276749"),
            fontName="Helvetica-Bold",
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["Normal"],
            fontSize=10,
            spaceBefore=4,
            spaceAfter=4,
            leading=14,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BulletItem",
            parent=styles["Normal"],
            fontSize=10,
            leftIndent=20,
            spaceBefore=3,
            spaceAfter=3,
        )
    )

    styles.add(
        ParagraphStyle(
            name="EQRecommendation",
            parent=styles["Normal"],
            fontSize=10,
            leftIndent=15,
            spaceBefore=6,
            spaceAfter=6,
            backColor=colors.HexColor("#f7fafc"),
            borderPadding=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Footer",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.gray,
            alignment=TA_CENTER,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ImageCaption",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#718096"),
            alignment=TA_CENTER,
            spaceBefore=5,
            spaceAfter=15,
        )
    )

    return styles


def generate_pdf(analysis_data: dict, output_path: Path):
    """Generate a comprehensive PDF report from analysis data."""
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    styles = create_styles()
    story = []

    metadata = analysis_data.get("metadata", {})
    audio_analysis = analysis_data.get("audio_analysis", {})
    accent_analysis = analysis_data.get("accent_analysis", {})
    eq_recommendations = analysis_data.get("eq_recommendations", {})

    # ========== TITLE PAGE ==========
    story.append(Spacer(1, 50))
    story.append(Paragraph("AI-EQ Voice Analysis Report", styles["ReportTitle"]))
    story.append(HRFlowable(width="80%", thickness=3, color=colors.HexColor("#2c5282")))

    # Subtitle with file info
    audio_file = metadata.get("audio_file", "Unknown")
    timestamp = metadata.get("analysis_timestamp", "")[:19].replace("T", " ")
    story.append(Paragraph(f"Analysis of: {audio_file}<br/>Generated: {timestamp}", styles["Subtitle"]))

    # Quick summary box
    accent = accent_analysis.get("primary_accent", "Unknown")
    confidence = accent_analysis.get("confidence", "unknown")
    conf_pct = accent_analysis.get("confidence_percentage", "N/A")
    voice_chars = audio_analysis.get("voice_characteristics", {})

    story.append(Spacer(1, 30))
    story.append(Paragraph(f"{accent}", styles["AccentResult"]))

    conf_color = {"high": "#276749", "medium": "#c05621", "low": "#c53030"}.get(confidence.lower(), "#4a5568")
    story.append(Paragraph(
        f'<font color="{conf_color}">Confidence: {confidence.upper()} ({conf_pct}%)</font>',
        ParagraphStyle(name="ConfText", parent=styles["Normal"], alignment=TA_CENTER, fontSize=12)
    ))

    if voice_chars:
        story.append(Spacer(1, 10))
        story.append(Paragraph(
            f"Voice Profile: {voice_chars.get('voice_type', 'N/A').title()} • {voice_chars.get('brightness', 'N/A').title()}",
            ParagraphStyle(name="VoiceProfile", parent=styles["Normal"], alignment=TA_CENTER, fontSize=11, textColor=colors.HexColor("#4a5568"))
        ))

    story.append(PageBreak())

    # ========== AUDIO ANALYSIS SECTION ==========
    story.append(Paragraph("Audio Analysis", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0")))

    # Voice Characteristics Table
    story.append(Paragraph("Voice Characteristics", styles["SubsectionHeader"]))

    f0_data = audio_analysis.get("fundamental_frequency", {})
    spectral = audio_analysis.get("spectral_characteristics", {})
    energy = audio_analysis.get("energy", {})
    quality = audio_analysis.get("voice_quality", {})

    char_data = [
        ["Metric", "Value", "Interpretation"],
        ["Fundamental Frequency (F0)", f"{f0_data.get('mean_hz', 'N/A')} Hz", f"Voice type: {voice_chars.get('voice_type', 'N/A')}"],
        ["F0 Range", f"{f0_data.get('min_hz', 'N/A')} - {f0_data.get('max_hz', 'N/A')} Hz", f"Variation: {f0_data.get('std_hz', 'N/A')} Hz"],
        ["Spectral Centroid", f"{spectral.get('centroid_mean_hz', 'N/A')} Hz", f"Brightness: {voice_chars.get('brightness', 'N/A')}"],
        ["Spectral Rolloff", f"{spectral.get('rolloff_mean_hz', 'N/A')} Hz", "High frequency content"],
        ["Dynamic Range", f"{energy.get('dynamic_range_db', 'N/A')} dB", "Volume variation"],
        ["Breathiness", quality.get('breathiness_indicator', 'N/A').title(), f"ZCR: {quality.get('zero_crossing_rate_mean', 'N/A')}"],
    ]

    char_table = Table(char_data, colWidths=[2.2 * inch, 1.8 * inch, 2.5 * inch])
    char_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7fafc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(char_table)

    # Spectrograms
    plots = audio_analysis.get("plots", {})
    analysis_dir = output_path.parent

    story.append(Paragraph("Spectral Visualizations", styles["SubsectionHeader"]))

    # Spectrogram
    spectrogram_path = plots.get("spectrogram", "")
    if spectrogram_path and Path(spectrogram_path).exists():
        img = Image(spectrogram_path, width=6.5 * inch, height=2.2 * inch)
        story.append(img)
        story.append(Paragraph("Figure 1: Spectrogram showing frequency content over time", styles["ImageCaption"]))

    # Mel Spectrogram
    mel_path = plots.get("mel_spectrogram", "")
    if mel_path and Path(mel_path).exists():
        img = Image(mel_path, width=6.5 * inch, height=2.2 * inch)
        story.append(img)
        story.append(Paragraph("Figure 2: Mel Spectrogram (perceptually-weighted frequency representation)", styles["ImageCaption"]))

    # Frequency Analysis
    freq_path = plots.get("frequency_analysis", "")
    if freq_path and Path(freq_path).exists():
        story.append(PageBreak())
        img = Image(freq_path, width=6.5 * inch, height=4.5 * inch)
        story.append(img)
        story.append(Paragraph("Figure 3: Time-series analysis of spectral centroid, pitch, and energy", styles["ImageCaption"]))

    # ========== ACCENT ANALYSIS SECTION ==========
    story.append(Paragraph("Accent & Dialect Analysis", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0")))

    # Regional context
    story.append(Paragraph("Regional Context", styles["SubsectionHeader"]))
    story.append(Paragraph(accent_analysis.get("regional_context", "No context provided."), styles["BodyCustom"]))

    # Phonetic features
    features = accent_analysis.get("phonetic_features", [])
    if features:
        story.append(Paragraph("Phonetic Features Observed", styles["SubsectionHeader"]))
        for feature in features:
            story.append(Paragraph(f"• {feature}", styles["BulletItem"]))

    # Secondary influences
    influences = accent_analysis.get("secondary_influences", [])
    if influences:
        story.append(Paragraph("Secondary Accent Influences", styles["SubsectionHeader"]))
        for influence in influences:
            story.append(Paragraph(f"• {influence}", styles["BulletItem"]))

    # Speech characteristics
    speech_chars = accent_analysis.get("speech_characteristics", {})
    if speech_chars:
        story.append(Paragraph("Speech Patterns", styles["SubsectionHeader"]))
        if speech_chars.get("tempo"):
            story.append(Paragraph(f"<b>Tempo:</b> {speech_chars['tempo']}", styles["BodyCustom"]))
        if speech_chars.get("intonation"):
            story.append(Paragraph(f"<b>Intonation:</b> {speech_chars['intonation']}", styles["BodyCustom"]))
        notable = speech_chars.get("notable_sounds", [])
        if notable:
            story.append(Paragraph("<b>Notable Sounds:</b>", styles["BodyCustom"]))
            for sound in notable:
                story.append(Paragraph(f"• {sound}", styles["BulletItem"]))

    # Analysis notes
    notes = accent_analysis.get("analysis_notes")
    if notes:
        story.append(Paragraph("Additional Notes", styles["SubsectionHeader"]))
        story.append(Paragraph(notes, styles["BodyCustom"]))

    # ========== EQ RECOMMENDATIONS SECTION ==========
    story.append(PageBreak())
    story.append(Paragraph("EQ Recommendations", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0")))

    # Summary
    story.append(Paragraph(eq_recommendations.get("summary", ""), ParagraphStyle(
        name="EQSummary", parent=styles["Normal"], fontSize=12, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#2c5282"), spaceBefore=10, spaceAfter=15
    )))

    # Detailed recommendations
    story.append(Paragraph("Recommended EQ Adjustments", styles["SubsectionHeader"]))
    for i, rec in enumerate(eq_recommendations.get("recommendations", []), 1):
        story.append(Paragraph(f"<b>{i}.</b> {rec}", styles["EQRecommendation"]))

    # EQ Bands Table
    eq_bands = eq_recommendations.get("eq_bands", [])
    if eq_bands:
        story.append(Spacer(1, 15))
        story.append(Paragraph("Suggested EQ Bands", styles["SubsectionHeader"]))

        band_data = [["Type", "Frequency", "Gain", "Purpose"]]
        for band in eq_bands:
            band_data.append([
                band.get("type", "N/A").replace("-", " ").title(),
                f"{band.get('frequency_hz', 'N/A')} Hz",
                band.get("gain_db", "N/A"),
                band.get("description", ""),
            ])

        band_table = Table(band_data, colWidths=[1.3 * inch, 1.1 * inch, 1.0 * inch, 3 * inch])
        band_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#276749")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0fff4")]),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(band_table)

    # Accent-specific tips
    accent_tips = eq_recommendations.get("accent_specific_tips", [])
    if accent_tips:
        story.append(Spacer(1, 15))
        story.append(Paragraph("Accent-Specific Tips", styles["SubsectionHeader"]))
        for tip in accent_tips:
            story.append(Paragraph(f"• {tip}", styles["BulletItem"]))

    # Processing suggestions
    processing = eq_recommendations.get("processing_suggestions", [])
    if processing:
        story.append(Spacer(1, 15))
        story.append(Paragraph("Additional Processing Suggestions", styles["SubsectionHeader"]))
        for suggestion in processing:
            story.append(Paragraph(f"• {suggestion}", styles["BulletItem"]))

    # ========== FOOTER ==========
    story.append(Spacer(1, 40))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f"Generated by AI-EQ Assistant • {datetime.now().strftime('%Y-%m-%d %H:%M')}<br/>"
        f"Audio analysis: librosa • Accent detection: OpenAI gpt-4o-audio-preview",
        styles["Footer"]
    ))

    doc.build(story)


def main():
    if len(sys.argv) < 2:
        analysis_dir = Path(__file__).parent / "analysis"
        json_files = list(analysis_dir.glob("*_analysis.json"))
        if not json_files:
            print("Usage: python generate_pdf.py <analysis_json_file>")
            print("Or run analyze_voice.py first to generate analysis JSON")
            sys.exit(1)
        json_path = max(json_files, key=lambda p: p.stat().st_mtime)
    else:
        json_path = Path(sys.argv[1])

    if not json_path.exists():
        print(f"Error: File not found: {json_path}")
        sys.exit(1)

    print(f"Loading analysis from: {json_path}")

    with open(json_path) as f:
        analysis_data = json.load(f)

    output_path = json_path.with_suffix(".pdf")

    print("Generating comprehensive PDF report...")
    generate_pdf(analysis_data, output_path)

    print(f"PDF saved to: {output_path}")


if __name__ == "__main__":
    main()
