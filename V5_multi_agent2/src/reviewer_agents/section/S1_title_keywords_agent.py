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
        """Analyzes the title and keywords of the manuscript."""
        prompt = f"""Analyze ONLY the title and keywords section of the manuscript. Do not analyze the abstract or any other sections.

        Focus on:
        1. Title clarity and conciseness
        2. Title accuracy and specificity
        3. Title impact and appeal
        4. Keywords relevance
        5. Keywords coverage
        6. Keywords specificity
        7. Field-specific conventions
        8. Search engine optimization
        9. International accessibility
        10. Technical accuracy

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Clarity: Language, readability, technical terms
        - Accuracy: Content representation, methodology indication
        - Impact: Significance, appeal to readers
        - SEO: Discoverability, searchability
        - Standards: Field conventions, journal requirements

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "title_keywords_score": int,  # Single comprehensive score (1-10)
            
            "critical_remarks": [{{
                "category": str,  # "title_clarity", "title_length", "keywords_relevance", "keywords_coverage", "guidelines", "discoverability"
                "location": str,  # "Title" or "Keywords"
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects manuscript quality
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # "Title" or "Keywords"
                "category": str,  # "title", "keywords", "guidelines", "discoverability"
                "focus": str  # "clarity", "conciseness", "accuracy", "impact", "relevance", "coverage"
            }}],
            
            "detailed_feedback": {{
                "title_analysis": str,  # Detailed paragraph about title quality
                "keywords_analysis": str,  # Detailed paragraph about keywords quality
                "guidelines_compliance": str,  # Detailed paragraph about field conventions
                "discoverability_assessment": str,  # Detailed paragraph about search optimization
                "audience_alignment": str  # Detailed paragraph about appeal and significance
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: 
        1. ONLY analyze the title and keywords section, not the abstract or other sections
        2. Generate at least 10-15 improvement suggestions across different categories
        3. Each suggestion should be specific, actionable, and include clear explanations
        4. All locations should be either "Title" or "Keywords", never "Abstract"
        5. Focus on improving discoverability and search optimization
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing title and keywords: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "title_keywords_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "title_analysis": "",
                "keywords_analysis": "",
                "guidelines_compliance": "",
                "discoverability_assessment": "",
                "audience_alignment": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 