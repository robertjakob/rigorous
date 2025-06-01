from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class TechnicalAccuracyAgent(BaseReviewerAgent):
    """Agent responsible for reviewing mathematical derivations, algorithms, and technical content."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "R6_Technical_Accuracy_Agent"
        self.category = "Scientific Rigor"
        
    def analyze_technical_accuracy(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes mathematical derivations, algorithms, and technical content."""
        prompt = f"""Analyze the following text for technical accuracy. Focus on:
        1. Mathematical derivation correctness
        2. Algorithm correctness and efficiency
        3. Technical terminology accuracy
        4. Equation clarity and presentation
        5. Technical content completeness
        6. Logical consistency
        7. Implementation details
        8. Edge case handling
        9. Complexity analysis
        10. Technical documentation

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Abstract: Technical approach summary
        - Introduction: Technical framework overview
        - Methodology: Technical methods description
        - Mathematical Framework: Derivation presentation
        - Algorithm Description: Implementation details
        - Technical Analysis: Complexity and efficiency
        - Results: Technical findings presentation
        - Discussion: Technical implications
        - Conclusion: Technical significance summary

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "technical_accuracy_score": int,  # Single comprehensive score (1-5)
            # IMPORTANT: The score MUST be between 1 and 5, where:
            # 1 = Poor: Major issues that significantly impact quality
            # 2 = Below Average: Several notable issues that need attention
            # 3 = Average: Some issues but generally acceptable
            # 4 = Good: Minor issues that don't significantly impact quality
            # 5 = Excellent: Very few or no issues, high quality
            
            "critical_remarks": [{{
                "category": str,  # "derivations", "algorithms", "terminology", "equations", "completeness", "consistency", "implementation", "edge_cases", "complexity", "documentation"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects technical accuracy
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "abstract", "introduction", "methodology", "mathematical_framework", "algorithm_description", "technical_analysis", "results", "discussion", "conclusion"
                "focus": str  # "derivations", "algorithms", "terminology", "equations", "completeness", "consistency", "implementation", "edge_cases", "complexity", "documentation"
            }}],
            
            "detailed_feedback": {{
                "derivation_correctness": str,  # Detailed paragraph about mathematical derivations
                "algorithm_accuracy": str,  # Detailed paragraph about algorithm correctness
                "terminology_accuracy": str,  # Detailed paragraph about technical terminology
                "equation_clarity": str,  # Detailed paragraph about equation presentation
                "content_completeness": str,  # Detailed paragraph about technical content
                "logical_consistency": str,  # Detailed paragraph about logical consistency
                "implementation_details": str,  # Detailed paragraph about implementation
                "edge_case_handling": str,  # Detailed paragraph about edge cases
                "complexity_analysis": str,  # Detailed paragraph about complexity
                "technical_documentation": str  # Detailed paragraph about documentation
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances technical accuracy.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing technical accuracy: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "technical_accuracy_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "derivation_correctness": "",
                "algorithm_accuracy": "",
                "terminology_accuracy": "",
                "equation_clarity": "",
                "content_completeness": "",
                "logical_consistency": "",
                "implementation_details": "",
                "edge_case_handling": "",
                "complexity_analysis": "",
                "technical_documentation": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 