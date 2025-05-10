from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class ReferencesAgentS9(BaseReviewerAgent):
    """Agent responsible for evaluating the references of a manuscript."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "S9_References_Agent"
        self.category = "Section Review"
        
    def analyze_references(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the references of the manuscript."""
        prompt = f"""Analyze the reference list (bibliography) provided at the end of the manuscript. Focus exclusively on the reference list, not in-text citations. Assess:
        1. Completeness of reference details (authors, title, journal, year, etc.)
        2. Consistency and correctness of reference formatting
        3. Relevance and recency of sources
        4. Diversity of sources (journals, books, etc.)
        5. Organization and ordering of the reference list
        6. Adherence to the required style guide for the reference list
        7. Cross-reference accuracy (do all references correspond to actual entries in the list?)

        For each aspect, provide at least 2-3 improvement suggestions. Consider these categories:
        - Completeness: Are all necessary details present for each reference?
        - Format: Is the reference list formatted consistently and according to the required style?
        - Quality: Are the sources relevant, recent, and diverse?
        - Organization: Is the reference list well-organized and correctly ordered?

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "score": int,  # Single comprehensive score (1-5)
            # 1 = Poor: Major issues that significantly impact quality
            # 2 = Below Average: Several notable issues that need attention
            # 3 = Average: Some issues but generally acceptable
            # 4 = Good: Minor issues that don't significantly impact quality
            # 5 = Excellent: Very few or no issues, high quality
            "critical_remarks": [{{
                "category": str,  # "completeness", "format", "quality", "organization"
                "location": str,  # Reference number or section
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects manuscript quality
            }}],
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic reference
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "completeness", "format", "quality", "organization"
                "focus": str  # "reference", "format", "style", "relevance", "recency", "diversity"
            }}],
            "detailed_feedback": {{
                "completeness_analysis": str,  # Detailed paragraph about reference completeness
                "format_analysis": str,  # Detailed paragraph about format consistency
                "quality_analysis": str,  # Detailed paragraph about source quality
                "organization_analysis": str  # Detailed paragraph about reference organization
            }},
            "summary": str  # Overall assessment paragraph
        }}

        Focus on 3-5 highest-impact improvements that would significantly enhance the research value.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the reference list.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing references: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "completeness_analysis": "",
                "format_analysis": "",
                "quality_analysis": "",
                "organization_analysis": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 