from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class MethodologyAgentS5(BaseReviewerAgent):
    """Agent responsible for evaluating the methodology of a manuscript."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "S5_Methodology_Agent"
        self.category = "Section Review"
        
    def analyze_methodology(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the methodology of the manuscript."""
        prompt = f"""Analyze the following methodology for quality and completeness. Focus on:
        1. Research design
        2. Data collection
        3. Sampling approach
        4. Instrumentation
        5. Procedures
        6. Analysis methods
        7. Validity measures
        8. Reliability assessment
        9. Ethical considerations
        10. Limitations handling

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Design: Approach, framework, rationale
        - Methods: Techniques, procedures, tools
        - Analysis: Statistical methods, qualitative approaches
        - Quality: Validity, reliability, rigor
        - Ethics: Consent, approval, considerations

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
                "category": str,  # "design", "methods", "analysis", "quality", "ethics"
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
                "category": str,  # "design", "methods", "analysis", "quality", "ethics"
                "focus": str  # "approach", "techniques", "procedures", "validity", "reliability"
            }}],
            
            "detailed_feedback": {{
                "design_analysis": str,  # Detailed paragraph about research design
                "methods_assessment": str,  # Detailed paragraph about methodology
                "analysis_evaluation": str,  # Detailed paragraph about analysis approach
                "quality_review": str,  # Detailed paragraph about validity and reliability
                "ethics_compliance": str  # Detailed paragraph about ethical considerations
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the methodology.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing methodology: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "design_analysis": "",
                "methods_assessment": "",
                "analysis_evaluation": "",
                "quality_review": "",
                "ethics_compliance": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 