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
        prompt = f"""Analyze the following references for quality and completeness. Focus on:
        1. Citation accuracy
        2. Reference completeness
        3. Format consistency
        4. Source relevance
        5. Source recency
        6. Source diversity
        7. Citation-text alignment
        8. Reference list organization
        9. Style guide compliance
        10. Cross-reference accuracy

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Accuracy: Citation correctness, cross-reference accuracy
        - Completeness: Reference details, source information
        - Format: Style compliance, consistency
        - Quality: Relevance, recency, diversity

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "score": int,  # Single comprehensive score (1-10)
            
            "critical_remarks": [{{
                "category": str,  # "accuracy", "completeness", "format", "quality"
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
                "category": str,  # "accuracy", "completeness", "format", "quality"
                "focus": str  # "citation", "reference", "format", "style", "relevance", "recency", "diversity"
            }}],
            
            "detailed_feedback": {{
                "accuracy_analysis": str,  # Detailed paragraph about citation accuracy
                "completeness_analysis": str,  # Detailed paragraph about reference completeness
                "format_analysis": str,  # Detailed paragraph about format consistency
                "quality_analysis": str,  # Detailed paragraph about source quality
                "organization_analysis": str  # Detailed paragraph about reference organization
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 10-15 improvement suggestions across different categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the references.
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
                "accuracy_analysis": "",
                "completeness_analysis": "",
                "format_analysis": "",
                "quality_analysis": "",
                "organization_analysis": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 