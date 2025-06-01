from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class IntroductionAgentS3(BaseReviewerAgent):
    """Agent responsible for evaluating the introduction of a manuscript."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "S3_Introduction_Agent"
        self.category = "Section Review"
        
    def analyze_introduction(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the introduction of the manuscript."""
        prompt = f"""Analyze the following introduction for quality and effectiveness. Focus on:
        1. Background context
        2. Problem statement
        3. Research gap identification
        4. Objectives clarity
        5. Significance justification
        6. Literature integration
        7. Flow and organization
        8. Technical accuracy
        9. Research scope
        10. Hypothesis/questions

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Context: Background, field overview
        - Problem: Issue identification, gap analysis
        - Objectives: Goals, research questions
        - Significance: Impact, contribution
        - Structure: Organization, flow

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
                "category": str,  # "context", "problem", "objectives", "significance", "structure"
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
                "category": str,  # "context", "problem", "objectives", "significance", "structure"
                "focus": str  # "background", "problem", "gap", "objectives", "significance", "flow"
            }}],
            
            "detailed_feedback": {{
                "context_analysis": str,  # Detailed paragraph about background
                "problem_analysis": str,  # Detailed paragraph about problem statement
                "objectives_analysis": str,  # Detailed paragraph about research goals
                "significance_assessment": str,  # Detailed paragraph about impact
                "structure_evaluation": str  # Detailed paragraph about organization
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the introduction.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing introduction: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "context_analysis": "",
                "problem_analysis": "",
                "objectives_analysis": "",
                "significance_assessment": "",
                "structure_evaluation": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 