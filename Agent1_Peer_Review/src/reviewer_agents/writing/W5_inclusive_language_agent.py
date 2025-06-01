from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class InclusiveLanguageAgent(BaseReviewerAgent):
    """Agent responsible for evaluating inclusive, unbiased language usage."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "W5_Inclusive_Language_Agent"
        self.category = "Writing and Presentation"
        
    def analyze_inclusive_language(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the use of inclusive and unbiased language in the text."""
        prompt = f"""Analyze the following text for inclusive and unbiased language usage. Focus on:
        1. Gender-neutral language
        2. Cultural sensitivity
        3. Age-appropriate terminology
        4. Disability-inclusive language
        5. Socioeconomic sensitivity
        6. Geographic inclusivity
        7. Professional title usage
        8. Stereotype avoidance
        9. Identity-first vs. person-first language
        10. Historical context sensitivity

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Abstract: Overall tone and inclusivity
        - Introduction: Background description
        - Literature Review: Participant descriptions
        - Methodology: Sample descriptions
        - Results: Participant representation
        - Discussion: Interpretation language
        - Conclusion: Generalizability statements
        - References: Author representation

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "inclusive_language_score": int,  # Single comprehensive score (1-5)
            # IMPORTANT: The score MUST be between 1 and 5, where:
            # 1 = Poor: Major issues that significantly impact quality
            # 2 = Below Average: Several notable issues that need attention
            # 3 = Average: Some issues but generally acceptable
            # 4 = Good: Minor issues that don't significantly impact quality
            # 5 = Excellent: Very few or no issues, high quality
            
            "critical_remarks": [{{
                "category": str,  # "gender_neutrality", "cultural_sensitivity", "age_terminology", "disability_inclusion", "socioeconomic_sensitivity", "geographic_inclusivity", "professional_titles", "stereotypes", "identity_language", "historical_context"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects inclusivity
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "abstract", "introduction", "literature", "methodology", "results", "discussion", "conclusion", "references"
                "focus": str  # "gender_neutrality", "cultural_sensitivity", "age_terminology", "disability_inclusion", "socioeconomic_sensitivity", "geographic_inclusivity", "professional_titles", "stereotypes", "identity_language", "historical_context"
            }}],
            
            "detailed_feedback": {{
                "gender_neutral_language": str,  # Detailed paragraph about gender-neutral language
                "cultural_sensitivity": str,  # Detailed paragraph about cultural sensitivity
                "age_appropriate_terminology": str,  # Detailed paragraph about age-appropriate terminology
                "disability_inclusive_language": str,  # Detailed paragraph about disability-inclusive language
                "socioeconomic_sensitivity": str,  # Detailed paragraph about socioeconomic sensitivity
                "geographic_inclusivity": str,  # Detailed paragraph about geographic inclusivity
                "professional_title_usage": str,  # Detailed paragraph about professional title usage
                "stereotypes": str,  # Detailed paragraph about stereotype avoidance
                "identity_language": str,  # Detailed paragraph about identity-first vs. person-first language
                "historical_context": str  # Detailed paragraph about historical context sensitivity
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances inclusivity.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing inclusive language: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "inclusive_language_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "gender_neutral_language": "",
                "cultural_sensitivity": "",
                "age_appropriate_terminology": "",
                "disability_inclusive_language": "",
                "socioeconomic_sensitivity": "",
                "geographic_inclusivity": "",
                "professional_title_usage": "",
                "stereotypes": "",
                "identity_language": "",
                "historical_context": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 