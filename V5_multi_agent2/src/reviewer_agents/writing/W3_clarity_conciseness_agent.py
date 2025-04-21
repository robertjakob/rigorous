from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class ClarityConcisenessAgent(BaseReviewerAgent):
    """Agent responsible for evaluating clarity and conciseness of the manuscript."""
    
    def __init__(self, model="gpt-4"):
        super().__init__(model)
        self.name = "W3_Clarity_Conciseness_Agent"
        self.category = "Writing and Presentation"
        
    def analyze_clarity_conciseness(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the clarity and conciseness of the text."""
        prompt = f"""Analyze the following text for clarity and conciseness. Focus on:
        1. Language simplicity
        2. Jargon usage
        3. Wordiness
        4. Sentence length
        5. Paragraph length
        6. Active vs. passive voice
        7. Redundancy
        8. Ambiguity
        9. Readability
        10. Information density

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "clarity_conciseness_score": int,  # Single comprehensive score (1-10)
            
            "critical_remarks": [{{
                "category": str,  # "language_simplicity", "jargon", "wordiness", "sentence_length", "paragraph_length", "voice", "redundancy", "ambiguity", "readability", "information_density"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects clarity
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str  # Where to apply this change
            }}],
            
            "detailed_feedback": {{
                "language_simplicity": str,  # Detailed paragraph about language simplicity
                "jargon_usage": str,  # Detailed paragraph about jargon usage
                "wordiness": str,  # Detailed paragraph about wordiness
                "sentence_length": str,  # Detailed paragraph about sentence length
                "paragraph_length": str,  # Detailed paragraph about paragraph length
                "active_passive_voice": str,  # Detailed paragraph about active vs. passive voice
                "redundancy": str,  # Detailed paragraph about redundancy
                "ambiguity": str,  # Detailed paragraph about ambiguity
                "readability": str,  # Detailed paragraph about readability
                "information_density": str  # Detailed paragraph about information density
            }},
            
            "summary": str  # Overall assessment paragraph
        }}
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing clarity and conciseness: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "clarity_conciseness_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "language_simplicity": "",
                "jargon_usage": "",
                "wordiness": "",
                "sentence_length": "",
                "paragraph_length": "",
                "active_passive_voice": "",
                "redundancy": "",
                "ambiguity": "",
                "readability": "",
                "information_density": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 