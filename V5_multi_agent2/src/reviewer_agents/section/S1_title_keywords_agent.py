from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class TitleKeywordsAgentS1(BaseReviewerAgent):
    """Agent responsible for evaluating the title and keywords of a manuscript."""
    
    def __init__(self, model="gpt-4"):
        super().__init__(model)
        self.name = "S1_Title_Keywords_Agent"
        self.category = "Section Review"
        
    def analyze_title_keywords(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the title of the manuscript and suggests an ideal improved version."""
        prompt = f"""Analyze ONLY the title of the manuscript. Do not analyze the abstract or any other sections.

        Focus on these five key aspects:
        1. Title clarity and conciseness
        2. SEO and discoverability
        3. Field-specific conventions
        4. Accuracy and specificity
        5. Impact and reader appeal

        Text to analyze: {text}
        Research type: {research_type}

        Your task is to:
        1. Identify the current title of the manuscript
        2. Evaluate it against the five key aspects above
        3. Create ONE ideal title that addresses all these aspects
        4. Provide detailed explanations about how your suggested title improves each aspect

        Provide a detailed analysis in the following JSON format:
        {{
            "title_keywords_score": int,  # Single comprehensive score for existing title (1-10)
            
            "critical_remarks": [{{
                "category": str,  # "clarity", "seo", "conventions", "accuracy", "impact"
                "location": str,  # "Title"
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects manuscript quality
            }}],
            
            "improvement_suggestions": [{{
                "original_title": str,  # The existing title
                "improved_title": str,  # Your ONE ideal title suggestion
                "explanation": str,  # Comprehensive explanation of all improvements
                "location": str,  # "Title"
                "category": str,  # "title"
                "focus": str  # "comprehensive"
            }}],
            
            "detailed_feedback": {{
                "clarity_conciseness": str,  # How the new title improves clarity and conciseness
                "seo_discoverability": str,  # How the new title enhances SEO and discoverability
                "field_conventions": str,  # How the new title aligns with field-specific conventions
                "accuracy_specificity": str,  # How the new title improves accuracy and specificity
                "impact_appeal": str  # How the new title increases impact and reader appeal
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: 
        1. ONLY analyze and improve the title, not keywords or other sections
        2. Create just ONE ideal title suggestion that addresses ALL five key aspects
        3. Provide detailed explanations for how your suggested title improves each aspect
        4. Make the title specific, accurate, concise, discoverable, and impactful
        5. Ensure the title follows field-specific conventions while being accessible
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing title: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "title_keywords_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "clarity_conciseness": "",
                "seo_discoverability": "",
                "field_conventions": "",
                "accuracy_specificity": "",
                "impact_appeal": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 