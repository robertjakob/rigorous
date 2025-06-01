from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class ImpactSignificanceAgent(BaseReviewerAgent):
    """Agent responsible for evaluating research impact and significance."""
    
    def __init__(self, model="gpt-4.1-nano"):
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

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Abstract: Impact statement, significance highlights
        - Introduction: Research importance, field relevance
        - Literature Review: Gap impact, field advancement
        - Methodology: Innovation potential, scalability
        - Results: Key findings impact, practical value
        - Discussion: Broader implications, future directions
        - Conclusion: Impact summary, application potential

        Text to analyze: {text}
        Field context: {json.dumps(field_context, indent=2)}

        Provide a detailed analysis in the following JSON format:
        {{
            "impact_significance_score": int,  # Single comprehensive score (1-5)
            # IMPORTANT: The score MUST be between 1 and 5, where:
            # 1 = Poor: Major issues that significantly impact quality
            # 2 = Below Average: Several notable issues that need attention
            # 3 = Average: Some issues but generally acceptable
            # 4 = Good: Minor issues that don't significantly impact quality
            # 5 = Excellent: Very few or no issues, high quality
            
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
                "location": str,  # Where to apply this change
                "category": str,  # "abstract", "introduction", "literature", "methodology", "results", "discussion", "conclusion"
                "focus": str  # "field_influence", "implications", "future_research", "applications", "policy"
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

        Important: Generate at least 5-10 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the research impact and significance.
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