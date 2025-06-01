from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class StatisticalRigorAgent(BaseReviewerAgent):
    """Agent responsible for evaluating statistical methods appropriateness and correctness."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "R5_Statistical_Rigor_Agent"
        self.category = "Scientific Rigor"
        
    def analyze_statistical_rigor(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes statistical methods appropriateness and correctness."""
        prompt = f"""Analyze the following text for statistical methods appropriateness and correctness. Focus on:
        1. Statistical test selection
        2. Assumption verification
        3. Sample size justification
        4. Multiple comparison handling
        5. Effect size reporting
        6. Confidence intervals
        7. P-value interpretation
        8. Statistical power
        9. Missing data handling
        10. Outlier treatment

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Abstract: Statistical approach summary
        - Introduction: Statistical framework overview
        - Methodology: Statistical methods description
        - Data Preparation: Assumption checks, data cleaning
        - Analysis: Statistical test implementation
        - Results: Statistical findings presentation
        - Discussion: Statistical interpretation
        - Conclusion: Statistical significance summary

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "statistical_rigor_score": int,  # Single comprehensive score (1-5)
            # IMPORTANT: The score MUST be between 1 and 5, where:
            # 1 = Poor: Major issues that significantly impact quality
            # 2 = Below Average: Several notable issues that need attention
            # 3 = Average: Some issues but generally acceptable
            # 4 = Good: Minor issues that don't significantly impact quality
            # 5 = Excellent: Very few or no issues, high quality
            
            "critical_remarks": [{{
                "category": str,  # "test_selection", "assumptions", "sample_size", "multiple_comparisons", "effect_size", "confidence_intervals", "p_value", "power", "missing_data", "outliers"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects statistical validity
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "abstract", "introduction", "methodology", "data_preparation", "analysis", "results", "discussion", "conclusion"
                "focus": str  # "test_selection", "assumptions", "sample_size", "multiple_comparisons", "effect_size", "confidence_intervals", "p_value", "power", "missing_data", "outliers"
            }}],
            
            "detailed_feedback": {{
                "test_selection": str,  # Detailed paragraph about statistical test selection
                "assumption_verification": str,  # Detailed paragraph about assumption verification
                "sample_size_justification": str,  # Detailed paragraph about sample size
                "multiple_comparison_handling": str,  # Detailed paragraph about multiple comparisons
                "effect_size_reporting": str,  # Detailed paragraph about effect size
                "confidence_intervals": str,  # Detailed paragraph about confidence intervals
                "p_value_interpretation": str,  # Detailed paragraph about p-value interpretation
                "statistical_power": str,  # Detailed paragraph about statistical power
                "missing_data_handling": str,  # Detailed paragraph about missing data
                "outlier_treatment": str  # Detailed paragraph about outlier treatment
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances statistical rigor.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing statistical rigor: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "statistical_rigor_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "test_selection": "",
                "assumption_verification": "",
                "sample_size_justification": "",
                "multiple_comparison_handling": "",
                "effect_size_reporting": "",
                "confidence_intervals": "",
                "p_value_interpretation": "",
                "statistical_power": "",
                "missing_data_handling": "",
                "outlier_treatment": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 