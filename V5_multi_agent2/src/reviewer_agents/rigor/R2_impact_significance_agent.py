from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class ImpactSignificanceAgent(BaseReviewerAgent):
    """Agent responsible for evaluating research impact and significance."""
    
    def __init__(self, model="gpt-4"):
        super().__init__(model)
        self.name = "R2_Impact_Significance_Agent"
        self.category = "Scientific Rigor"
        
    def analyze_impact_significance(self, text: str, field_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes the impact and significance of the research."""
        prompt = f"""Analyze the following text for impact and significance. Focus on:
        1. Potential influence on the field
        2. Broader implications of findings
        3. Influence on future research
        4. Practical applications
        5. Policy implications

        Text to analyze: {text}
        Field context: {json.dumps(field_context, indent=2)}

        Provide a detailed analysis in the following JSON format:
        {{
            "impact_significance_score": int,  # Single comprehensive score (1-10)
            
            "critical_remarks": [{{
                "category": str,  # "field_influence", "implications", "future_research", "applications", "policy"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects the research significance
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str  # Where to apply this change
            }}],
            
            "detailed_feedback": {{
                "field_influence": str,  # Detailed paragraph about field influence
                "broader_implications": str,  # Detailed paragraph about implications
                "future_research_impact": str,  # Detailed paragraph about future research
                "practical_applications": str,  # Detailed paragraph about applications
                "policy_implications": str  # Detailed paragraph about policy
            }},
            
            "summary": str  # Overall assessment paragraph
        }}
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing impact and significance: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "impact_significance_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "field_influence": "",
                "broader_implications": "",
                "future_research_impact": "",
                "practical_applications": "",
                "policy_implications": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 