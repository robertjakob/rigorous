from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class ConclusionAgentS8(BaseReviewerAgent):
    """Agent responsible for evaluating the conclusion of a manuscript."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "S8_Conclusion_Agent"
        self.category = "Section Review"
        
    def analyze_conclusion(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the conclusion of the manuscript."""
        prompt = f"""Analyze the following conclusion for quality and completeness. Focus on:
        1. Support from results
        2. Research objective fulfillment
        3. Key findings summary
        4. Contribution clarity
        5. Practical implications
        6. Theoretical implications
        7. Future research suggestions
        8. Final statement strength
        9. Avoidance of new information
        10. Conciseness and clarity

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Support: Evidence-based, result alignment
        - Objectives: Fulfillment, contribution clarity
        - Implications: Practical, theoretical, future directions
        - Presentation: Clarity, conciseness, strength

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "score": int,  # Single comprehensive score (1-5)
            # IMPORTANT: The score MUST be between 1 and 5, where:
            # 1 = Poor: Major issues that significantly impact quality
            # 2 = Below Average: Several notable issues that need attention
            # 3 = Average: Some issues but generally acceptable
            # 4 = Good: Minor issues that don't significantly impact quality
            # 5 = Excellent: Very few or no issues, high quality
            
            "critical_remarks": [{{
                "category": str,  # "support", "objectives", "implications", "presentation"
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
                "category": str,  # "support", "objectives", "implications", "presentation"
                "focus": str  # "evidence", "fulfillment", "clarity", "implications", "future_directions", "strength"
            }}],
            
            "detailed_feedback": {{
                "support_analysis": str,  # Detailed paragraph about result support
                "objective_fulfillment": str,  # Detailed paragraph about research objective fulfillment
                "implications_analysis": str,  # Detailed paragraph about implications
                "presentation_analysis": str,  # Detailed paragraph about presentation quality
                "contribution_analysis": str  # Detailed paragraph about contribution clarity
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the conclusion.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing conclusion: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "support_analysis": "",
                "objective_fulfillment": "",
                "implications_analysis": "",
                "presentation_analysis": "",
                "contribution_analysis": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 