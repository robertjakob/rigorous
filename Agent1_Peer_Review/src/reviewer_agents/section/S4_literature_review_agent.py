from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class LiteratureReviewAgentS4(BaseReviewerAgent):
    """Agent responsible for evaluating the literature review of a manuscript."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "S4_Literature_Review_Agent"
        self.category = "Section Review"
        
    def analyze_literature_review(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the literature review of the manuscript."""
        prompt = f"""Analyze the following literature review for quality and comprehensiveness. Focus on:
        1. Coverage breadth
        2. Historical context
        3. Current state
        4. Critical analysis
        5. Gap identification
        6. Theoretical framework
        7. Methodological review
        8. Citation quality
        9. Organization logic
        10. Synthesis depth

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Coverage: Breadth, depth, relevance
        - Analysis: Critical thinking, synthesis
        - Structure: Organization, flow
        - Citations: Quality, recency
        - Integration: Connection to research

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
                "category": str,  # "coverage", "analysis", "structure", "citations", "integration"
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
                "category": str,  # "coverage", "analysis", "structure", "citations", "integration"
                "focus": str  # "breadth", "depth", "synthesis", "organization", "relevance"
            }}],
            
            "detailed_feedback": {{
                "coverage_analysis": str,  # Detailed paragraph about literature coverage
                "analysis_quality": str,  # Detailed paragraph about critical analysis
                "structure_evaluation": str,  # Detailed paragraph about organization
                "citation_assessment": str,  # Detailed paragraph about citation quality
                "integration_review": str  # Detailed paragraph about research connection
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the literature review.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing literature review: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "coverage_analysis": "",
                "analysis_quality": "",
                "structure_evaluation": "",
                "citation_assessment": "",
                "integration_review": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 