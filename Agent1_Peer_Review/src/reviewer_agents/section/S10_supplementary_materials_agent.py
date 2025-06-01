from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class SupplementaryMaterialsAgentS10(BaseReviewerAgent):
    """Agent responsible for evaluating the supplementary materials of a manuscript."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "S10_Supplementary_Materials_Agent"
        self.category = "Section Review"
        
    def analyze_supplementary_materials(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the supplementary materials of the manuscript."""
        prompt = f"""Analyze the following supplementary materials for quality and completeness. Focus on:
        1. Relevance to main text
        2. Clarity of presentation
        3. Consistency with main text
        4. Completeness of information
        5. Organization and structure
        6. Data presentation
        7. Methodological details
        8. Additional results
        9. Reference to main text
        10. Accessibility and usability

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Relevance: Connection to main text, value addition
        - Clarity: Presentation, organization, accessibility
        - Consistency: Alignment with main text, coherence
        - Completeness: Information detail, methodological thoroughness

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
                "category": str,  # "relevance", "clarity", "consistency", "completeness"
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
                "category": str,  # "relevance", "clarity", "consistency", "completeness"
                "focus": str  # "connection", "presentation", "organization", "accessibility", "alignment", "coherence", "detail", "thoroughness"
            }}],
            
            "detailed_feedback": {{
                "relevance_analysis": str,  # Detailed paragraph about relevance to main text
                "clarity_analysis": str,  # Detailed paragraph about presentation clarity
                "consistency_analysis": str,  # Detailed paragraph about consistency with main text
                "completeness_analysis": str,  # Detailed paragraph about information completeness
                "organization_analysis": str  # Detailed paragraph about structure and organization
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the supplementary materials.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing supplementary materials: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "relevance_analysis": "",
                "clarity_analysis": "",
                "consistency_analysis": "",
                "completeness_analysis": "",
                "organization_analysis": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 