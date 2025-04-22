from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class VisualPresentationAgentW8(BaseReviewerAgent):
    """Agent responsible for evaluating visual presentation elements in the manuscript."""
    
    def __init__(self, model="gpt-4"):
        super().__init__(model)
        self.name = "W8_Visual_Presentation_Agent"
        self.category = "Writing and Presentation"
        
    def analyze_visual_presentation(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the quality, clarity, and effectiveness of visual elements in the manuscript."""
        prompt = f"""Analyze the following text for visual presentation quality and effectiveness. Focus on:
        1. Figure quality and clarity
        2. Table formatting and readability
        3. Visual element placement
        4. Caption completeness
        5. Color scheme appropriateness
        6. Data visualization effectiveness
        7. Visual hierarchy
        8. Accessibility considerations
        9. Consistency in visual style
        10. Integration with text

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Figures: Quality, clarity, and effectiveness
        - Tables: Formatting, readability, and completeness
        - Diagrams: Clarity and information density
        - Charts: Data representation and interpretation
        - Visual consistency: Style and formatting
        - Accessibility: Color contrast and readability
        - Integration: How well visuals support the text
        - Captions: Completeness and clarity

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "visual_presentation_score": int,  # Single comprehensive score (1-10)
            
            "critical_remarks": [{{
                "category": str,  # "figure_quality", "table_formatting", "visual_placement", "caption_completeness", "color_scheme", "data_visualization", "visual_hierarchy", "accessibility", "visual_consistency", "text_integration"
                "location": str,  # Section/figure/table reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects reader understanding
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text or description
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "figure", "table", "diagram", "chart", "style", "accessibility", "integration", "caption"
                "focus": str  # "quality", "clarity", "formatting", "placement", "color", "visualization", "hierarchy", "accessibility", "consistency", "integration"
            }}],
            
            "detailed_feedback": {{
                "figure_quality": str,  # Detailed paragraph about figure quality
                "table_formatting": str,  # Detailed paragraph about table formatting
                "visual_placement": str,  # Detailed paragraph about visual element placement
                "caption_completeness": str,  # Detailed paragraph about caption completeness
                "color_scheme": str,  # Detailed paragraph about color scheme appropriateness
                "data_visualization": str,  # Detailed paragraph about data visualization effectiveness
                "visual_hierarchy": str,  # Detailed paragraph about visual hierarchy
                "accessibility": str,  # Detailed paragraph about accessibility considerations
                "visual_consistency": str,  # Detailed paragraph about visual style consistency
                "text_integration": str  # Detailed paragraph about integration with text
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 10-15 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances visual presentation.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing visual presentation: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "visual_presentation_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "figure_quality": "",
                "table_formatting": "",
                "visual_placement": "",
                "caption_completeness": "",
                "color_scheme": "",
                "data_visualization": "",
                "visual_hierarchy": "",
                "accessibility": "",
                "visual_consistency": "",
                "text_integration": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 