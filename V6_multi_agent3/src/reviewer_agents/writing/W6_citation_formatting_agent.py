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
        prompt = f"""Analyze the following text for citation formatting and consistency. Focus on:
        1. In-text citation format
        2. Reference list formatting
        3. Citation style consistency
        4. Reference completeness
        5. DOI/URL formatting
        6. Author name formatting
        7. Publication date formatting
        8. Journal name formatting
        9. Volume/issue/page formatting
        10. Cross-reference accuracy

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Abstract: Citation style
        - Introduction: First citations
        - Literature Review: Multiple citations
        - Methodology: Method citations
        - Results: Data citations
        - Discussion: Comparison citations
        - Conclusion: Summary citations
        - References: List formatting

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "citation_formatting_score": int,  # Single comprehensive score (1-5)
            
            "critical_remarks": [{{
                "category": str,  # "in_text_format", "reference_format", "style_consistency", "reference_completeness", "doi_format", "author_format", "date_format", "journal_format", "volume_format", "cross_reference"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects citation quality
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "abstract", "introduction", "literature", "methodology", "results", "discussion", "conclusion", "references"
                "focus": str  # "in_text_format", "reference_format", "style_consistency", "reference_completeness", "doi_format", "author_format", "date_format", "journal_format", "volume_format", "cross_reference"
            }}],
            
            "detailed_feedback": {{
                "in_text_citation_format": str,  # Detailed paragraph about in-text citation format
                "reference_list_format": str,  # Detailed paragraph about reference list formatting
                "citation_style_consistency": str,  # Detailed paragraph about citation style consistency
                "reference_completeness": str,  # Detailed paragraph about reference completeness
                "doi_url_formatting": str,  # Detailed paragraph about DOI/URL formatting
                "author_name_formatting": str,  # Detailed paragraph about author name formatting
                "publication_date_formatting": str,  # Detailed paragraph about publication date formatting
                "journal_name_formatting": str,  # Detailed paragraph about journal name formatting
                "volume_issue_page_formatting": str,  # Detailed paragraph about volume/issue/page formatting
                "cross_reference_accuracy": str  # Detailed paragraph about cross-reference accuracy
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 10-15 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances citation formatting.
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
                "reference_list_format": "",
                "citation_style_consistency": "",
                "reference_completeness": "",
                "doi_url_formatting": "",
                "author_name_formatting": "",
                "publication_date_formatting": "",
                "journal_name_formatting": "",
                "volume_issue_page_formatting": "",
                "cross_reference_accuracy": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 