from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class TerminologyConsistencyAgent(BaseReviewerAgent):
    """Agent responsible for ensuring consistent use of terms, notations, and acronyms."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "W4_Terminology_Consistency_Agent"
        self.category = "Writing and Presentation"
        
    def analyze_terminology_consistency(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the consistency of terminology, notations, and acronyms in the text."""
        prompt = f"""Analyze the following text for terminology consistency. Focus on:
        1. Term usage consistency
        2. Notation consistency
        3. Acronym usage and definition
        4. Variable naming consistency
        5. Unit notation consistency
        6. Abbreviation consistency
        7. Technical term consistency
        8. Field-specific terminology
        9. Cross-reference consistency
        10. Definition consistency

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Abstract: Term introduction
        - Introduction: Field terminology
        - Literature Review: Citation terms
        - Methodology: Technical terms
        - Results: Variable names
        - Discussion: Term usage
        - Conclusion: Term consistency
        - Equations: Notation style

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "terminology_consistency_score": int,  # Single comprehensive score (1-5)
            # IMPORTANT: The score MUST be between 1 and 5, where:
            # 1 = Poor: Major issues that significantly impact quality
            # 2 = Below Average: Several notable issues that need attention
            # 3 = Average: Some issues but generally acceptable
            # 4 = Good: Minor issues that don't significantly impact quality
            # 5 = Excellent: Very few or no issues, high quality
            
            "critical_remarks": [{{
                "category": str,  # "term_usage", "notation", "acronyms", "variable_naming", "unit_notation", "abbreviations", "technical_terms", "field_terminology", "cross_references", "definitions"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects consistency
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "abstract", "introduction", "literature", "methodology", "results", "discussion", "conclusion", "equations"
                "focus": str  # "term_usage", "notation", "acronyms", "variable_naming", "unit_notation", "abbreviations", "technical_terms", "field_terminology", "cross_references", "definitions"
            }}],
            
            "detailed_feedback": {{
                "term_usage_consistency": str,  # Detailed paragraph about term usage consistency
                "notation_consistency": str,  # Detailed paragraph about notation consistency
                "acronym_usage": str,  # Detailed paragraph about acronym usage
                "variable_naming_consistency": str,  # Detailed paragraph about variable naming consistency
                "unit_notation_consistency": str,  # Detailed paragraph about unit notation consistency
                "abbreviation_consistency": str,  # Detailed paragraph about abbreviation consistency
                "technical_term_consistency": str,  # Detailed paragraph about technical term consistency
                "field_terminology": str,  # Detailed paragraph about field-specific terminology
                "cross_reference_consistency": str,  # Detailed paragraph about cross-reference consistency
                "definition_consistency": str  # Detailed paragraph about definition consistency
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances terminology consistency.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing terminology consistency: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "terminology_consistency_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "term_usage_consistency": "",
                "notation_consistency": "",
                "acronym_usage": "",
                "variable_naming_consistency": "",
                "unit_notation_consistency": "",
                "abbreviation_consistency": "",
                "technical_term_consistency": "",
                "field_terminology": "",
                "cross_reference_consistency": "",
                "definition_consistency": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 