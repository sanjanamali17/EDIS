# edis_assistant/fallback_engine.py

import random
from typing import Optional, List, Dict

from .system_prompt import SYSTEM_PROMPT
from .intent_router import detect_intent

def get_fallback_response(user_query: str, context: Optional[str] = None) -> str:
    """
    Generate professional environmental intelligence responses when Groq API is not available
    """
    
    query_lower = user_query.lower()
    
    # Ecosystem Insight Mode - automatically generate comprehensive analysis
    if any(word in query_lower for word in ['explain this ecosystem', 'tell about ecosystem', 'ecosystem analysis', 'explain ecosystem result']):
        if context:
            return generate_comprehensive_ecosystem_analysis(context)
        else:
            return "I need ecosystem analysis data to provide comprehensive environmental insights. Please run an ecosystem analysis first, then I can generate a detailed environmental intelligence report."
    
    # If we have context, provide structured responses
    if context:
        return generate_structured_response_with_context(user_query, context, query_lower)
    
    # Fallback responses without context
    return generate_general_response(user_query, query_lower)

def generate_comprehensive_ecosystem_analysis(context: str) -> str:
    """Generate comprehensive ecosystem analysis with structured format"""
    
    # Parse context for key data
    location = "Unknown Location"
    ecosystem_score = 0
    climate_stress = 0
    soil_stress = 0
    vegetation_stress = 0
    human_pressure = 0
    biodiversity_stress = 0
    
    try:
        lines = context.split('\n')
        for line in lines:
            if "Location:" in line:
                location = line.split("Location:")[1].strip()
            elif "Ecosystem Stress Index:" in line:
                ecosystem_score = float(line.split("Ecosystem Stress Index:")[1].strip())
            elif "Climate Stress:" in line:
                climate_stress = float(line.split("Climate Stress:")[1].strip())
            elif "Soil Stress:" in line:
                soil_stress = float(line.split("Soil Stress:")[1].strip())
            elif "Vegetation Stress:" in line:
                vegetation_stress = float(line.split("Vegetation Stress:")[1].strip())
            elif "Human Pressure:" in line:
                human_pressure = float(line.split("Human Pressure:")[1].strip())
            elif "Biodiversity Stress:" in line:
                biodiversity_stress = float(line.split("Biodiversity Stress:")[1].strip())
    except:
        pass
    
    # Generate structured analysis
    status = "Critical Stress" if ecosystem_score >= 80 else "High Stress" if ecosystem_score >= 60 else "Moderate Stress" if ecosystem_score >= 40 else "Low Stress"
    
    analysis = f"""**Ecosystem Summary**
The ecosystem in {location} shows {status.lower()} with an overall stress index of {ecosystem_score:.1f}. Key environmental indicators reveal significant pressure on soil and vegetation systems, with climate factors showing moderate impact. The current stress level indicates potential degradation of ecosystem services and reduced environmental resilience.

**Key Environmental Risks**
Primary risks include soil degradation affecting agricultural productivity and water quality, vegetation stress indicating forest health decline and reduced carbon sequestration capacity, and human pressure suggesting unsustainable land use practices. These factors collectively threaten biodiversity and ecosystem stability, potentially leading to reduced ecosystem services for local communities.

**Possible Causes**
Contributing factors likely include intensive agricultural practices causing soil nutrient depletion, deforestation and land conversion reducing vegetation cover, urbanization and industrial activities increasing environmental pressure, and climate variability affecting ecosystem resilience. The interconnected nature of these stressors creates cascading effects across the environmental system.

**Recommended Actions**
Immediate interventions should focus on implementing soil conservation practices through organic farming and cover cropping, establishing reforestation programs to restore vegetation cover, enforcing sustainable land use policies to reduce human pressure, and developing climate adaptation strategies to enhance ecosystem resilience. Long-term monitoring protocols should be established to track recovery progress.

**Future Outlook**
If current conditions persist without intervention, the ecosystem faces continued degradation with potential loss of biodiversity and ecosystem services. However, with comprehensive restoration efforts, significant improvement is possible within 3-5 years, leading to enhanced environmental resilience and sustainable ecosystem services for future generations."""
    
    return analysis

def generate_structured_response_with_context(user_query: str, context: str, query_lower: str) -> str:
    """Generate structured responses with ecosystem context"""
    
    # Extract key metrics from context
    location = "Unknown location"
    ecosystem_score = 0
    climate_stress = 0
    soil_stress = 0
    vegetation_stress = 0
    human_pressure = 0
    biodiversity_stress = 0
    
    try:
        lines = context.split('\n')
        for line in lines:
            if "Location:" in line:
                location = line.split("Location:")[1].strip()
            elif "Ecosystem Stress Index:" in line:
                ecosystem_score = float(line.split("Ecosystem Stress Index:")[1].strip())
            elif "Climate Stress:" in line:
                climate_stress = float(line.split("Climate Stress:")[1].strip())
            elif "Soil Stress:" in line:
                soil_stress = float(line.split("Soil Stress:")[1].strip())
            elif "Vegetation Stress:" in line:
                vegetation_stress = float(line.split("Vegetation Stress:")[1].strip())
            elif "Human Pressure:" in line:
                human_pressure = float(line.split("Human Pressure:")[1].strip())
            elif "Biodiversity Stress:" in line:
                biodiversity_stress = float(line.split("Biodiversity Stress:")[1].strip())
    except:
        pass
    
    # Risk assessment responses with context
    if any(word in query_lower for word in ['risk', 'danger', 'threat', 'critical']):
        return f"""**Environmental Risk Assessment for {location}**
The overall ecosystem stress level of {ecosystem_score:.1f}% indicates {'critical environmental risks requiring immediate intervention' if ecosystem_score > 70 else 'moderate to high environmental risks' if ecosystem_score > 40 else 'low to moderate environmental risks'}. Primary concerns include soil stress ({soil_stress:.1f}%) affecting agricultural sustainability and water quality, vegetation stress ({vegetation_stress:.1f}%) indicating forest health decline, and human pressure ({human_pressure:.1f}%) suggesting unsustainable development patterns. These interconnected stressors create cascading environmental impacts that could compromise ecosystem services and biodiversity conservation efforts."""
    
    # Climate-specific responses with context
    elif any(word in query_lower for word in ['climate', 'temperature', 'weather']):
        return f"""**Climate Analysis for {location}**
Climate stress indicators show {climate_stress:.1f}% stress level, {'indicating significant climate-related environmental pressure' if climate_stress > 50 else 'suggesting relatively stable climate conditions'}. This contributes to overall ecosystem degradation through increased temperature variability, altered precipitation patterns, and enhanced extreme weather events. Climate factors interact with soil and vegetation systems, amplifying environmental stress across the ecosystem. Recommended climate adaptation strategies include developing drought-resistant vegetation, implementing water conservation measures, and establishing climate monitoring systems to track environmental changes."""
    
    # Soil-specific responses with context
    elif any(word in query_lower for word in ['soil', 'land', 'fertility']):
        return f"""**Soil Health Assessment for {location}**
Soil stress analysis reveals {soil_stress:.1f}% stress level, {'indicating severe soil degradation requiring immediate intervention' if soil_stress > 60 else 'suggesting moderate soil health concerns' if soil_stress > 30 else 'showing relatively healthy soil conditions'}. Current soil conditions impact agricultural productivity, water filtration capacity, and ecosystem nutrient cycling. Contributing factors likely include intensive farming practices, reduced organic matter input, and erosion from vegetation loss. Restoration strategies should focus on organic matter addition, conservation tillage, cover cropping, and targeted soil rehabilitation programs."""
    
    # Biodiversity responses with context
    elif any(word in query_lower for word in ['biodiversity', 'species', 'animals', 'plants']):
        return f"""**Biodiversity Analysis for {location}**
Biodiversity stress indicators show {biodiversity_stress:.1f}% stress level, {'indicating significant biodiversity loss and habitat degradation' if biodiversity_stress > 50 else 'suggesting moderate biodiversity concerns' if biodiversity_stress > 25 else 'showing relatively stable biodiversity conditions'}. This impacts ecosystem resilience, species interactions, and essential ecosystem services. Primary threats include habitat fragmentation, invasive species encroachment, and environmental pollution. Conservation strategies should prioritize habitat restoration, protected area expansion, invasive species management, and connectivity enhancement between fragmented habitats."""
    
    # Human pressure responses with context
    elif any(word in query_lower for word in ['human', 'pressure', 'impact', 'population']):
        return f"""**Human Impact Assessment for {location}**
Human pressure analysis indicates {human_pressure:.1f}% stress level, {'reflecting intense anthropogenic environmental impacts' if human_pressure > 60 else 'showing moderate human environmental pressure' if human_pressure > 30 else 'indicating relatively sustainable human activities'}. This encompasses urbanization effects, industrial pollution, agricultural intensification, and resource extraction impacts. Mitigation strategies should focus on sustainable development practices, pollution control measures, ecosystem-friendly urban planning, and community engagement in conservation efforts."""
    
    # General ecosystem health with context
    elif any(word in query_lower for word in ['health', 'status', 'condition', 'overall']):
        return f"""**Ecosystem Health Assessment for {location}**
The overall ecosystem health index of {ecosystem_score:.1f}% indicates {'critical degradation requiring emergency intervention' if ecosystem_score > 70 else 'significant stress requiring urgent action' if ecosystem_score > 50 else 'moderate stress needing preventive measures' if ecosystem_score > 30 else 'relatively healthy ecosystem with good resilience'}. Key stress drivers include soil degradation ({soil_stress:.1f}%), vegetation decline ({vegetation_stress:.1f}%), and human pressure ({human_pressure:.1f}%). The ecosystem requires {'immediate restoration efforts' if ecosystem_score > 60 else 'targeted conservation measures' if ecosystem_score > 40 else 'continued monitoring and maintenance'} to ensure long-term sustainability."""
    
    # Default contextual response
    else:
        return f"""**Environmental Intelligence for {location}**
Based on current ecosystem analysis showing {ecosystem_score:.1f}% overall stress, the environmental system requires {'comprehensive restoration intervention' if ecosystem_score > 60 else 'targeted conservation measures' if ecosystem_score > 40 else 'continued monitoring and maintenance'}. Key indicators reveal soil stress ({soil_stress:.1f}%), vegetation stress ({vegetation_stress:.1f}%), and human pressure ({human_pressure:.1f}%) as primary environmental concerns. For specific environmental insights, please specify your area of interest (climate, soil, biodiversity, or restoration strategies)."""

def generate_general_response(user_query: str, query_lower: str) -> str:
    """Generate general environmental intelligence responses"""
    
    # Risk assessment responses
    if any(word in query_lower for word in ['risk', 'danger', 'threat', 'critical']):
        return """**Environmental Risk Assessment Framework**
Environmental risk assessment requires comprehensive ecosystem analysis data to identify specific threats and vulnerabilities. Key risk categories include climate-related risks (temperature extremes, precipitation changes), soil degradation risks (erosion, nutrient depletion), biodiversity loss risks (habitat fragmentation, species decline), and human impact risks (pollution, land use change). Run an ecosystem analysis to receive location-specific risk assessment with quantitative risk levels and mitigation strategies."""
    
    # Recommendation responses
    elif any(word in query_lower for word in ['recommend', 'suggest', 'improve', 'restore']):
        return """**Ecosystem Restoration Strategies**
Effective ecosystem restoration requires evidence-based interventions tailored to specific environmental conditions. Key restoration approaches include:
1. **Soil Rehabilitation**: Organic matter addition, conservation tillage, cover cropping, and erosion control
2. **Vegetation Restoration**: Native species planting, reforestation, habitat connectivity, and invasive species management
3. **Climate Adaptation**: Drought-resistant species, water conservation, microclimate modification
4. **Biodiversity Conservation**: Protected area expansion, wildlife corridors, species monitoring
5. **Sustainable Practices**: Integrated resource management, community engagement, policy development
For location-specific recommendations, please run an ecosystem analysis first."""
    
    # Climate-specific responses
    elif any(word in query_lower for word in ['climate', 'temperature', 'weather']):
        return """**Climate Science Intelligence**
Climate stress analysis requires comprehensive environmental data including temperature patterns, precipitation changes, extreme weather events, and climate resilience indicators. Climate impacts on ecosystems include altered species distributions, changed phenological patterns, increased extreme weather frequency, and ecosystem service disruptions. For location-specific climate analysis and adaptation strategies, run an ecosystem analysis to receive detailed climate stress assessment."""
    
    # Default response
    else:
        return """**EDIS Environmental Intelligence System**
I am EDIS - Earth Digital Immune System, an advanced environmental intelligence platform designed to analyze ecosystems and provide scientific environmental insights. My expertise covers climate science, soil health, vegetation monitoring, biodiversity conservation, human environmental impact, and ecosystem restoration strategies.

For comprehensive environmental analysis and location-specific insights, please run an ecosystem analysis first. Then I can provide detailed environmental intelligence including risk assessments, restoration recommendations, and future outlook scenarios.

What specific environmental topic would you like to explore?"""

def ask_edis_assistant_fallback(
    user_query: str,
    context: Optional[str],
    chat_history: List[Dict],
    model: Optional[str] = None
) -> Dict:
    """
    Fallback assistant when Groq API is not available
    """
    intent = detect_intent(user_query)
    response_text = get_fallback_response(user_query, context)
    
    return {
        "text": response_text,
        "intent": intent,
        "visualize": None
    }
