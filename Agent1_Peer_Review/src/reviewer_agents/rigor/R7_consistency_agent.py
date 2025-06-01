from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class ConsistencyAgent(BaseReviewerAgent):
    """Agent responsible for checking logical coherence across sections."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "R7_Consistency_Agent"
        self.category = "Scientific Rigor"
        
    def analyze_consistency(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes logical coherence across sections."""
        prompt = f"""Analyze the following text for logical coherence and consistency across sections. Focus on:
        1. Alignment between methods and results
        2. Consistency between results and conclusions
        3. Logical flow between sections
        4. Terminology consistency
        5. Hypothesis-testing alignment
        6. Data interpretation consistency
        7. Citation consistency
        8. Figure-text alignment
        9. Table-text alignment
        10. Supplementary material consistency

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Abstract: Consistency with main text
        - Introduction: Alignment with methodology
        - Literature Review: Citation consistency
        - Methodology: Methods-results alignment
        - Results: Results-conclusions alignment
        - Discussion: Interpretation consistency
        - Conclusion: Overall coherence
        - Figures/Tables: Text alignment
        - Supplementary: Main text consistency

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "consistency_score": int,  # Single comprehensive score (1-5)
            
            "critical_remarks": [{{
                "category": str,  # "methods_results", "results_conclusions", "logical_flow", "terminology", "hypothesis", "interpretation", "citations", "figures", "tables", "supplementary"
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
                "category": str,  # "abstract", "introduction", "literature", "methodology", "results", "discussion", "conclusion", "figures_tables", "supplementary"
                "focus": str  # "methods_results", "results_conclusions", "logical_flow", "terminology", "hypothesis", "interpretation", "citations", "figures", "tables", "supplementary"
            }}],
            
            "detailed_feedback": {{
                "methods_results_alignment": str,  # Detailed paragraph about methods-results alignment
                "results_conclusions_alignment": str,  # Detailed paragraph about results-conclusions alignment
                "logical_flow": str,  # Detailed paragraph about logical flow
                "terminology_consistency": str,  # Detailed paragraph about terminology consistency
                "hypothesis_testing": str,  # Detailed paragraph about hypothesis-testing alignment
                "interpretation_consistency": str,  # Detailed paragraph about interpretation consistency
                "citation_consistency": str,  # Detailed paragraph about citation consistency
                "figure_text_alignment": str,  # Detailed paragraph about figure-text alignment
                "table_text_alignment": str,  # Detailed paragraph about table-text alignment
                "supplementary_consistency": str  # Detailed paragraph about supplementary material consistency
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances logical coherence and consistency.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing consistency: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "consistency_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "methods_results_alignment": "",
                "results_conclusions_alignment": "",
                "logical_flow": "",
                "terminology_consistency": "",
                "hypothesis_testing": "",
                "interpretation_consistency": "",
                "citation_consistency": "",
                "figure_text_alignment": "",
                "table_text_alignment": "",
                "supplementary_consistency": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 