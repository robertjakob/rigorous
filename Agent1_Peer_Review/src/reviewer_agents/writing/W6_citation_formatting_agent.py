from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class CitationFormattingAgent(BaseReviewerAgent):
    """Agent responsible for evaluating citation formatting and consistency."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "W6_Citation_Formatting_Agent"
        self.category = "Writing and Presentation"
        
    def analyze_citation_formatting(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the formatting and consistency of citations in the text."""
        prompt = f"""Analyze the following manuscript text for in-text citation formatting, style, and consistency. Focus exclusively on in-text citations (not the reference list). Assess:
        1. In-text citation style (e.g., APA, Vancouver, Harvard, etc.)
        2. Consistency of in-text citation formatting throughout the manuscript
        3. Correct placement and ordering of in-text citations
        4. Proper use of et al., author names, and years (if applicable)
        5. Consistency in citation delimiters (parentheses, brackets, superscripts, etc.)
        6. Cross-reference accuracy (do all in-text citations correspond to entries in the reference list?)
        7. Handling of multiple citations in a single location
        8. Citation of figures, tables, and supplementary materials (if applicable)
        9. Adherence to the required style guide for in-text citations

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - In-text format: Is the citation style consistent and correct?
        - Placement: Are citations placed appropriately in the text?
        - Style consistency: Are delimiters, author lists, and years handled consistently?
        - Cross-reference: Do all in-text citations match the reference list?

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "citation_formatting_score": int,  # Single comprehensive score (1-5)
            # 1 = Poor: Major issues that significantly impact citation quality
            # 2 = Below Average: Several notable issues that need attention
            # 3 = Average: Some issues but generally acceptable
            # 4 = Good: Minor issues that don't significantly impact quality
            # 5 = Excellent: Very few or no issues, high quality
            "critical_remarks": [{{
                "category": str,  # "in_text_format", "placement", "style_consistency", "cross_reference"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects citation quality
            }}],
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic in-text citation
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "in_text_format", "placement", "style_consistency", "cross_reference"
                "focus": str  # "in_text_format", "placement", "style_consistency", "cross_reference"
            }}],
            "detailed_feedback": {{
                "in_text_citation_format": str,  # Detailed paragraph about in-text citation format
                "placement_analysis": str,  # Detailed paragraph about citation placement
                "style_consistency_analysis": str,  # Detailed paragraph about style consistency
                "cross_reference_accuracy": str  # Detailed paragraph about cross-reference accuracy
            }},
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different categories, focusing only on in-text citations.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances in-text citation formatting and consistency.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing citation formatting: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "citation_formatting_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "in_text_citation_format": "",
                "placement_analysis": "",
                "style_consistency_analysis": "",
                "cross_reference_accuracy": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 