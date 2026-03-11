"""
AI Environmental Insight Generator
Earth Digital Immune System (EDIS)

This module generates AI-powered environmental insights and recommendations
based on ecosystem predictions using the existing LLM infrastructure.
"""

from typing import Dict, List, Optional
from edis_assistant.chat_engine import ask_edis_assistant
import json

class EnvironmentalInsightGenerator:
    """
    AI-powered environmental insight and recommendation generator
    """
    
    def __init__(self):
        self.insight_templates = {
            'climate_change': {
                'indicators': ['climate_stress', 'temperature_trends', 'precipitation_patterns'],
                'risks': ['heat_waves', 'drought', 'extreme_weather'],
                'actions': ['green_infrastructure', 'cooling_centers', 'water_conservation']
            },
            'soil_health': {
                'indicators': ['soil_stress', 'soil_moisture', 'nutrient_levels'],
                'risks': ['soil_degradation', 'erosion', 'fertility_loss'],
                'actions': ['organic_farming', 'cover_crops', 'soil_restoration']
            },
            'vegetation_cover': {
                'indicators': ['vegetation_stress', 'forest_cover', 'green_spaces'],
                'risks': ['deforestation', 'habitat_loss', 'reduced_oxygen'],
                'actions': ['afforestation', 'urban_greening', 'forest_protection']
            },
            'human_pressure': {
                'indicators': ['human_pressure', 'population_density', 'industrial_activity'],
                'risks': ['pollution', 'resource_depletion', 'urban_sprawl'],
                'actions': ['sustainable_development', 'waste_management', 'eco_planning']
            },
            'biodiversity': {
                'indicators': ['biodiversity_stress', 'species_diversity', 'habitat_quality'],
                'risks': ['species_loss', 'ecosystem_collapse', 'reduced_resilience'],
                'actions': ['conservation_areas', 'wildlife_corridors', 'species_protection']
            }
        }
    
    def generate_insights(self, prediction_result: Dict) -> Dict:
        """
        Generate comprehensive environmental insights based on prediction results
        
        Args:
            prediction_result: Dictionary containing prediction data
            
        Returns:
            Dictionary containing insights, risks, and recommendations
        """
        try:
            city = prediction_result.get('city', 'Unknown')
            predictions = prediction_result.get('predictions', [])
            trend_analysis = prediction_result.get('trend_analysis', {})
            training_data = prediction_result.get('training_data', {})
            
            if not predictions:
                return {
                    'success': False,
                    'error': 'No predictions available for insight generation'
                }
            
            # Analyze prediction trends
            current_esi = training_data.get('esi_values', [0])[-1] if training_data.get('esi_values') else 0
            future_esi = predictions[-1]['esi'] if predictions else current_esi
            trend_direction = trend_analysis.get('direction', 'stable')
            
            # Generate insights using LLM
            insights = self._generate_ai_insights(city, predictions, current_esi, future_esi, trend_direction)
            
            # Generate structured analysis
            structured_insights = self._generate_structured_analysis(predictions, trend_direction)
            
            return {
                'success': True,
                'city': city,
                'ai_insights': insights,
                'structured_analysis': structured_insights,
                'trend_summary': {
                    'current_esi': current_esi,
                    'future_esi': future_esi,
                    'trend_direction': trend_direction,
                    'change_magnitude': future_esi - current_esi
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error generating insights: {str(e)}'
            }
    
    def _generate_ai_insights(self, city: str, predictions: List[Dict], current_esi: float, future_esi: float, trend_direction: str) -> str:
        """
        Generate AI-powered insights using the existing LLM infrastructure
        """
        try:
            # Prepare context for the LLM
            context = f"""
            City: {city}
            Current Ecosystem Stress Index: {current_esi:.1f}
            Future Ecosystem Stress Index: {future_esi:.1f}
            Trend Direction: {trend_direction}
            
            Predictions:
            {json.dumps(predictions, indent=2)}
            
            Please analyze this ecosystem prediction and provide:
            1. Predicted Environmental Changes
            2. Potential Risks
            3. Recommended Sustainability Actions
            
            Format the response in clear sections with bullet points.
            """
            
            # Generate insights using the existing assistant
            result = ask_edis_assistant(
                user_query=f"Analyze the ecosystem prediction for {city} and provide environmental insights",
                context=context,
                chat_history=[]
            )
            
            return result.get('text', 'Unable to generate AI insights at this time.')
            
        except Exception as e:
            return f"Error generating AI insights: {str(e)}"
    
    def _generate_structured_analysis(self, predictions: List[Dict], trend_direction: str) -> Dict:
        """
        Generate structured analysis based on prediction patterns
        """
        try:
            # Analyze key indicators from predictions
            esi_values = [p['esi'] for p in predictions]
            years = [p['year'] for p in predictions]
            
            # Calculate trend metrics
            if len(esi_values) > 1:
                slope = (esi_values[-1] - esi_values[0]) / (years[-1] - years[0])
                acceleration = slope > 0.5  # Rapidly increasing stress
            else:
                slope = 0
                acceleration = False
            
            # Identify risk levels
            max_esi = max(esi_values)
            risk_level = self._assess_risk_level(max_esi)
            
            # Generate environmental changes
            environmental_changes = self._identify_environmental_changes(trend_direction, slope, acceleration)
            
            # Generate potential risks
            potential_risks = self._identify_potential_risks(risk_level, trend_direction, acceleration)
            
            # Generate recommended actions
            recommended_actions = self._generate_recommended_actions(risk_level, trend_direction, environmental_changes)
            
            return {
                'environmental_changes': environmental_changes,
                'potential_risks': potential_risks,
                'recommended_actions': recommended_actions,
                'risk_level': risk_level,
                'trend_metrics': {
                    'slope': round(slope, 3),
                    'acceleration': acceleration,
                    'max_predicted_esi': round(max_esi, 2)
                }
            }
            
        except Exception as e:
            return {
                'environmental_changes': ['Unable to analyze environmental changes'],
                'potential_risks': ['Unable to assess potential risks'],
                'recommended_actions': ['Unable to generate recommendations'],
                'risk_level': 'Unknown',
                'error': str(e)
            }
    
    def _assess_risk_level(self, esi_value: float) -> str:
        """Assess risk level based on ESI value"""
        if esi_value < 30:
            return "Low Risk"
        elif esi_value < 45:
            return "Moderate Risk"
        elif esi_value < 60:
            return "High Risk"
        else:
            return "Critical Risk"
    
    def _identify_environmental_changes(self, trend_direction: str, slope: float, acceleration: bool) -> List[str]:
        """Identify likely environmental changes based on trends"""
        changes = []
        
        if trend_direction == "declining":
            changes.append("Ecosystem health deteriorating over time")
            if acceleration:
                changes.append("Rapid acceleration of environmental stress")
            else:
                changes.append("Gradual increase in ecosystem pressure")
            
            if slope > 1:
                changes.append("Climate instability increasing")
                changes.append("Vegetation stress rising significantly")
                changes.append("Human pressure growing rapidly")
            elif slope > 0.5:
                changes.append("Climate stress moderately increasing")
                changes.append("Soil degradation progressing")
            else:
                changes.append("Slow but steady environmental decline")
        elif trend_direction == "improving":
            changes.append("Ecosystem health improving over time")
            if slope < -1:
                changes.append("Rapid environmental recovery")
            else:
                changes.append("Gradual ecosystem improvement")
        else:
            changes.append("Ecosystem conditions relatively stable")
        
        return changes
    
    def _identify_potential_risks(self, risk_level: str, trend_direction: str, acceleration: bool) -> List[str]:
        """Identify potential environmental risks"""
        risks = []
        
        if risk_level in ["High Risk", "Critical Risk"]:
            risks.extend([
                "Urban heat island expansion",
                "Water scarcity and drought conditions",
                "Soil degradation and reduced fertility",
                "Loss of biodiversity and habitat destruction",
                "Air quality deterioration"
            ])
        
        if acceleration and trend_direction == "declining":
            risks.extend([
                "Ecosystem collapse threshold approaching",
                "Irreversible environmental damage",
                "Cascading environmental failures"
            ])
        
        if trend_direction == "declining":
            risks.extend([
                "Increased frequency of extreme weather events",
                "Reduced agricultural productivity",
                "Public health impacts from pollution"
            ])
        
        return risks
    
    def _generate_recommended_actions(self, risk_level: str, trend_direction: str, environmental_changes: List[str]) -> List[str]:
        """Generate recommended sustainability actions"""
        actions = []
        
        # Core actions based on risk level
        if risk_level in ["High Risk", "Critical Risk"]:
            actions.extend([
                "Implement emergency environmental protection measures",
                "Establish strict pollution control regulations",
                "Create comprehensive ecosystem restoration plan"
            ])
        else:
            actions.extend([
                "Continue monitoring environmental indicators",
                "Implement preventive conservation measures"
            ])
        
        # Actions based on trend direction
        if trend_direction == "declining":
            actions.extend([
                "Increase green cover and urban forests",
                "Protect and restore water bodies",
                "Promote sustainable agricultural practices",
                "Implement green infrastructure development",
                "Enhance waste management systems",
                "Develop renewable energy sources"
            ])
        
        # Actions based on specific environmental changes
        if any("climate" in change.lower() for change in environmental_changes):
            actions.extend([
                "Develop climate adaptation strategies",
                "Create early warning systems for extreme weather",
                "Implement heat island mitigation measures"
            ])
        
        if any("vegetation" in change.lower() for change in environmental_changes):
            actions.extend([
                "Launch afforestation and reforestation programs",
                "Protect existing forest cover",
                "Promote urban gardening and green roofs"
            ])
        
        if any("human pressure" in change.lower() for change in environmental_changes):
            actions.extend([
                "Implement sustainable urban planning",
                "Promote public transportation",
                "Develop eco-industrial zones"
            ])
        
        return actions

# Initialize the insight generator
insight_generator = EnvironmentalInsightGenerator()
