from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class TargetAudienceAlignmentAgent(BaseReviewerAgent):
    """Agent responsible for evaluating writing style and formatting alignment with target audience."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "W7_Target_Audience_Alignment_Agent"
        self.category = "Writing and Presentation"
        
    def analyze_target_audience_alignment(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes how well the writing style and formatting align with the target audience."""
        prompt = f"""Analyze the following text for target audience alignment and writing style appropriateness. Focus on:
        1. Technical depth and complexity
        2. Field-specific terminology usage
        3. Writing style formality
        4. Section organization
        5. Visual element integration
        6. Reference style and depth
        7. Methodology description detail
        8. Results presentation
        9. Discussion depth
        10. Conclusion format

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Abstract: Conciseness and technical level
        - Introduction: Background depth
        - Literature Review: Reference depth
        - Methodology: Technical detail
        - Results: Data presentation
        - Discussion: Analysis depth
        - Conclusion: Summary style
        - Visual Elements: Integration and complexity

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "audience_alignment_score": int,  # Single comprehensive score (1-5)
            # IMPORTANT: The score MUST be between 1 and 5, where:
            # 1 = Poor: Major issues that significantly impact quality
            # 2 = Below Average: Several notable issues that need attention
            # 3 = Average: Some issues but generally acceptable
            # 4 = Good: Minor issues that don't significantly impact quality
            # 5 = Excellent: Very few or no issues, high quality
            
            "critical_remarks": [{{
                "category": str,  # "technical_depth", "terminology", "formality", "organization", "visuals", "references", "methodology", "results", "discussion", "conclusion"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects audience engagement
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "abstract", "introduction", "literature", "methodology", "results", "discussion", "conclusion", "visuals"
                "focus": str  # "technical_depth", "terminology", "formality", "organization", "visuals", "references", "methodology", "results", "discussion", "conclusion"
            }}],
            
            "detailed_feedback": {{
                "technical_depth": str,  # Detailed paragraph about technical depth appropriateness
                "terminology_usage": str,  # Detailed paragraph about field-specific terminology
                "writing_formality": str,  # Detailed paragraph about writing style formality
                "section_organization": str,  # Detailed paragraph about section organization
                "visual_integration": str,  # Detailed paragraph about visual element integration
                "reference_style": str,  # Detailed paragraph about reference style and depth
                "methodology_detail": str,  # Detailed paragraph about methodology description
                "results_presentation": str,  # Detailed paragraph about results presentation
                "discussion_depth": str,  # Detailed paragraph about discussion depth
                "conclusion_format": str  # Detailed paragraph about conclusion format
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances audience alignment.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing target audience alignment: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "audience_alignment_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "technical_depth": "",
                "terminology_usage": "",
                "writing_formality": "",
                "section_organization": "",
                "visual_integration": "",
                "reference_style": "",
                "methodology_detail": "",
                "results_presentation": "",
                "discussion_depth": "",
                "conclusion_format": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 