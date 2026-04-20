# edis_assistant/context_builder.py

from datetime import datetime
from typing import Dict, Optional

def build_context(
    location: str,
    indices: Dict[str, Optional[float]],
    ecosystem_score: float,
    confidence: float = 1.0
) -> str:
    """
    Builds a comprehensive, LLM-optimized ecosystem context for professional environmental intelligence.
    """

    # -----------------------------
    # Risk classification
    # -----------------------------
    if ecosystem_score >= 80:
        risk = "Critical"
        urgency = "Immediate intervention required"
        status = "Critical Stress"
    elif ecosystem_score >= 60:
        risk = "High"
        urgency = "Urgent action needed"
        status = "High Stress"
    elif ecosystem_score >= 40:
        risk = "Moderate"
        urgency = "Monitoring and mitigation recommended"
        status = "Moderate Stress"
    else:
        risk = "Low"
        urgency = "Maintain current practices"
        status = "Low Stress"

    valid_indices = {
        k: v for k, v in indices.items()
        if isinstance(v, (int, float))
    }

    # Sort indicators by stress level (highest first)
    sorted_indices = sorted(valid_indices.items(), key=lambda x: x[1], reverse=True)
    dominant_driver = sorted_indices[0][0] if sorted_indices else "Unknown"
    secondary_driver = sorted_indices[1][0] if len(sorted_indices) > 1 else None

    # Build structured context for environmental intelligence
    context_lines = [
        f"Location: {location}",
        "",
        "Indicators:",
        f"Climate Stress: {indices.get('climate_stress', 'N/A')}",
        f"Soil Stress: {indices.get('soil_stress', 'N/A')}",
        f"Vegetation Stress: {indices.get('vegetation_stress', 'N/A')}",
        f"Human Pressure: {indices.get('human_pressure', 'N/A')}",
        f"Biodiversity Stress: {indices.get('biodiversity_stress', 'N/A')}",
        "",
        f"Ecosystem Stress Index: {round(ecosystem_score, 1)}",
        f"Status: {status}",
        "",
        f"Risk Level: {risk}",
        f"Urgency: {urgency}",
        f"Confidence: {round(confidence, 2)}",
        "",
        "Primary Stress Driver: " + dominant_driver.replace('_', ' ').title(),
    ]
    
    if secondary_driver:
        context_lines.append(
            f"Secondary Stress Driver: " + secondary_driver.replace('_', ' ').title()
        )

    context_lines.extend([
        "",
        "Environmental Analysis Required:",
        "- Provide comprehensive ecosystem assessment",
        "- Analyze key environmental risks and causes",
        "- Recommend specific restoration strategies",
        "- Include future outlook and monitoring protocols",
        "- Use structured response format with detailed insights"
    ])

    return "\n".join(context_lines)
