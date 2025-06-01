from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class OriginalityContributionAgent(BaseReviewerAgent):
    """Agent responsible for assessing research novelty and unique contributions."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "R1_Originality_Contribution_Agent"
        self.category = "Scientific Rigor"
        
    def analyze_originality_contribution(self, text: str, field_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes the originality and contribution of the research."""
        prompt = f"""Analyze the following text for originality and contribution to the field. Focus on:
        1. Novelty of the research approach
        2. Unique contributions to the field
        3. Verification of stated novelty claims
        4. Comparison with existing literature
        5. Advancement of knowledge

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Abstract: Clarity of novelty statement, contribution highlights
        - Introduction: Research gap identification, novelty claims
        - Literature Review: Comparison with existing work, gap analysis
        - Methodology: Novel approach description, innovation details
        - Results: Contribution presentation, advancement demonstration
        - Discussion: Impact assessment, future implications
        - Conclusion: Contribution summary, field advancement

        Text to analyze: {text}
        Field context: {json.dumps(field_context, indent=2)}

        Provide a detailed analysis in the following JSON format:
        {{
            "originality_contribution_score": int,  # Single comprehensive score (1-5)
            
            "critical_remarks": [{{
                "category": str,  # "novelty", "contribution", "verification", "comparison", "advancement"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects the research validity
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "abstract", "introduction", "literature", "methodology", "results", "discussion", "conclusion"
                "focus": str  # "novelty", "contribution", "verification", "comparison", "advancement"
            }}],
            
            "detailed_feedback": {{
                "novelty_assessment": str,  # Detailed paragraph about research novelty
                "contribution_analysis": str,  # Detailed paragraph about contributions
                "verification_status": str,  # Detailed paragraph about novelty claims
                "comparative_analysis": str,  # Detailed paragraph about literature comparison
                "advancement_evaluation": str  # Detailed paragraph about knowledge advancement
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the research.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing originality and contribution: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "originality_contribution_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "novelty_assessment": "",
                "contribution_analysis": "",
                "verification_status": "",
                "comparative_analysis": "",
                "advancement_evaluation": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 