from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class TitleKeywordsAgentS1(BaseReviewerAgent):
    """Agent responsible for evaluating the title and keywords of a manuscript."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "S1_Title_Keywords_Agent"
        self.category = "Section Review"
        
    def analyze_title_keywords(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the title and keywords of the manuscript."""
        prompt = f"""Analyze the title and keywords section of the manuscript. Follow these steps:

        1. FIRST, check if there is a dedicated "Keywords:" or "Keywords" section in the text.
           - Look for a line that starts with "Keywords:" or "Keywords"
           - If no such section is found, set has_keywords = false
           - If found, set has_keywords = true and extract the keywords

        2. For the title analysis:
           - Analyze the current title considering ALL aspects simultaneously:
             * Clarity: Is it clear and understandable?
             * Accuracy: Does it accurately represent the content?
             * Impact: Does it capture attention and significance?
             * SEO: Is it optimized for search engines?
             * Standards: Does it follow field conventions?
           - Generate ONE comprehensive improvement suggestion that addresses all these aspects
           - The improved title should be the optimal balance of all these factors

        3. For keywords analysis (ONLY if has_keywords = true):
           - Analyze relevance, coverage, and specificity
           - Provide improvement suggestions
           - Consider search engine optimization

        4. If has_keywords = false:
           - Set all keyword-related fields to empty or null
           - Do not generate any keyword-related feedback
           - Do not make assumptions about keywords from other text

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "title_keywords_score": int,  # Single comprehensive score (1-5)
            
            "critical_remarks": [{{
                "category": str,  # "title_clarity", "title_length", "keywords_relevance", "keywords_coverage", "guidelines", "discoverability"
                "location": str,  # "Title" or "Keywords"
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects manuscript quality
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The current title
                "improved_version": str,  # ONE comprehensive improved title that balances all aspects
                "explanation": str,  # Detailed explanation of how the improved title addresses clarity, accuracy, impact, SEO, and standards
                "location": str,  # "Title"
                "category": str,  # "title"
                "focus": str  # "comprehensive_improvement"
            }}],
            
            "detailed_feedback": {{
                "title_analysis": str,  # Detailed paragraph about title quality
                "keywords_analysis": str,  # "No keywords section found" if has_keywords = false
                "guidelines_compliance": str,  # Detailed paragraph about field conventions
                "discoverability_assessment": str,  # Detailed paragraph about search optimization
                "audience_alignment": str  # Detailed paragraph about appeal and significance
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: 
        1. ONLY analyze the title and keywords section
        2. If no "Keywords:" or "Keywords" section is found:
           - Set keywords_analysis to "No keywords section found"
           - Do not include any keyword-related critical remarks
           - Do not include any keyword-related improvement suggestions
           - Do not make assumptions about keywords from other text
        3. Generate ONE comprehensive title improvement that considers all aspects simultaneously
        4. The title improvement should balance clarity, accuracy, impact, SEO, and standards
        5. All locations should be either "Title" or "Keywords", never "Abstract"
        6. Focus on improving discoverability and search optimization
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