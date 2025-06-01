from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class AbstractAgentS2(BaseReviewerAgent):
    """Agent responsible for evaluating the abstract of a manuscript."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "S2_Abstract_Agent"
        self.category = "Section Review"
        
    def analyze_abstract(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the abstract of the manuscript."""
        prompt = f"""Analyze the following abstract for quality and completeness. Focus on:
        1. Structure and organization
        2. Content completeness
        3. Clarity and readability
        4. Methodology description
        5. Results presentation
        6. Conclusion strength
        7. Scientific writing standards
        8. Field-specific requirements
        9. Impact communication
        10. Technical accuracy

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Structure: Organization, flow, section presence
        - Content: Completeness, accuracy, technical details
        - Clarity: Language, readability, technical terms
        - Standards: Scientific writing, field conventions
        - Impact: Significance, implications, contributions

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "score": int,  # Single comprehensive score (1-5)
            
            "critical_remarks": [{{
                "category": str,  # "structure", "content", "clarity", "standards", "impact"
                "location": str,  # Section reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects manuscript quality
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "structure", "content", "clarity", "standards", "impact"
                "focus": str  # "organization", "completeness", "readability", "methodology", "results", "conclusion"
            }}],
            
            "detailed_feedback": {{
                "structure_analysis": str,  # Detailed paragraph about abstract structure
                "content_analysis": str,  # Detailed paragraph about content completeness
                "clarity_assessment": str,  # Detailed paragraph about readability
                "standards_compliance": str,  # Detailed paragraph about scientific standards
                "impact_evaluation": str  # Detailed paragraph about significance
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the abstract.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing abstract: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "structure_analysis": "",
                "content_analysis": "",
                "clarity_assessment": "",
                "standards_compliance": "",
                "impact_evaluation": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 