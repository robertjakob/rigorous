from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class DiscussionAgentS7(BaseReviewerAgent):
    """Agent responsible for evaluating the discussion of a manuscript."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "S7_Discussion_Agent"
        self.category = "Section Review"
        
    def analyze_discussion(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the discussion of the manuscript."""
        prompt = f"""Analyze the following discussion for quality and completeness. Focus on:
        1. Result interpretation
        2. Literature comparison
        3. Limitation analysis
        4. Future work
        5. Practical implications
        6. Theoretical contributions
        7. Research gap addressing
        8. Methodology reflection
        9. Result significance
        10. Conclusion alignment

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Interpretation: Result analysis, significance
        - Context: Literature comparison, research gaps
        - Reflection: Limitations, future work
        - Impact: Practical implications, theoretical contributions
        - Quality: Completeness, coherence

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
                "category": str,  # "interpretation", "context", "reflection", "impact", "quality"
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
                "category": str,  # "interpretation", "context", "reflection", "impact", "quality"
                "focus": str  # "interpretation", "comparison", "limitations", "implications", "significance"
            }}],
            
            "detailed_feedback": {{
                "interpretation_analysis": str,  # Detailed paragraph about result interpretation
                "context_review": str,  # Detailed paragraph about literature comparison
                "reflection_assessment": str,  # Detailed paragraph about limitations/future work
                "impact_evaluation": str,  # Detailed paragraph about practical/theoretical impact
                "quality_analysis": str  # Detailed paragraph about overall discussion quality
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the discussion.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing discussion: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "interpretation_analysis": "",
                "context_review": "",
                "reflection_assessment": "",
                "impact_evaluation": "",
                "quality_analysis": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 