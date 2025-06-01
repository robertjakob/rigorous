from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class ResultsAgentS6(BaseReviewerAgent):
    """Agent responsible for evaluating the results of a manuscript."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "S6_Results_Agent"
        self.category = "Section Review"
        
    def analyze_results(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the results of the manuscript."""
        prompt = f"""Analyze the following results for quality and presentation. Focus on:
        1. Data presentation
        2. Statistical analysis
        3. Figure/table quality
        4. Result interpretation
        5. Significance reporting
        6. Effect sizes
        7. Confidence intervals
        8. Statistical tests
        9. Data visualization
        10. Result organization

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Presentation: Clarity, organization, visualization
        - Analysis: Statistical methods, significance
        - Interpretation: Meaning, implications
        - Quality: Accuracy, completeness
        - Impact: Significance, effect sizes

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
                "category": str,  # "presentation", "analysis", "interpretation", "quality", "impact"
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
                "category": str,  # "presentation", "analysis", "interpretation", "quality", "impact"
                "focus": str  # "clarity", "statistics", "visualization", "interpretation", "significance"
            }}],
            
            "detailed_feedback": {{
                "presentation_analysis": str,  # Detailed paragraph about data presentation
                "analysis_quality": str,  # Detailed paragraph about statistical analysis
                "interpretation_review": str,  # Detailed paragraph about result interpretation
                "visualization_assessment": str,  # Detailed paragraph about figures/tables
                "significance_evaluation": str  # Detailed paragraph about statistical significance
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the results section.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing results: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "presentation_analysis": "",
                "analysis_quality": "",
                "interpretation_review": "",
                "visualization_assessment": "",
                "significance_evaluation": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 