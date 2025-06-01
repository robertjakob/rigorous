from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class LanguageStyleAgent(BaseReviewerAgent):
    """Agent responsible for reviewing grammar, spelling, and punctuation."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "W1_Language_Style_Agent"
        self.category = "Writing and Presentation"
        
    def analyze_language_style(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes grammar, spelling, and punctuation in the text."""
        prompt = f"""Analyze the following text for grammar, spelling, and punctuation issues. Focus on:
        1. Grammar correctness
        2. Spelling accuracy
        3. Punctuation usage
        4. Sentence structure
        5. Verb tense consistency
        6. Subject-verb agreement
        7. Article usage
        8. Preposition usage
        9. Conjunction usage
        10. Academic writing conventions

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Abstract: Conciseness and clarity
        - Introduction: Academic tone and flow
        - Literature Review: Citation language
        - Methodology: Technical description
        - Results: Data presentation
        - Discussion: Argument structure
        - Conclusion: Summary language
        - References: Citation format

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "language_style_score": int,  # Single comprehensive score (1-5)
            
            "critical_remarks": [{{
                "category": str,  # "grammar", "spelling", "punctuation", "sentence_structure", "verb_tense", "subject_verb", "articles", "prepositions", "conjunctions", "academic_conventions"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects readability
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "abstract", "introduction", "literature", "methodology", "results", "discussion", "conclusion", "references"
                "focus": str  # "grammar", "spelling", "punctuation", "sentence_structure", "verb_tense", "subject_verb", "articles", "prepositions", "conjunctions", "academic_conventions"
            }}],
            
            "detailed_feedback": {{
                "grammar_correctness": str,  # Detailed paragraph about grammar issues
                "spelling_accuracy": str,  # Detailed paragraph about spelling issues
                "punctuation_usage": str,  # Detailed paragraph about punctuation issues
                "sentence_structure": str,  # Detailed paragraph about sentence structure
                "verb_tense_consistency": str,  # Detailed paragraph about verb tense consistency
                "subject_verb_agreement": str,  # Detailed paragraph about subject-verb agreement
                "article_usage": str,  # Detailed paragraph about article usage
                "preposition_usage": str,  # Detailed paragraph about preposition usage
                "conjunction_usage": str,  # Detailed paragraph about conjunction usage
                "academic_conventions": str  # Detailed paragraph about academic writing conventions
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the language and style.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing language style: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "language_style_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "grammar_correctness": "",
                "spelling_accuracy": "",
                "punctuation_usage": "",
                "sentence_structure": "",
                "verb_tense_consistency": "",
                "subject_verb_agreement": "",
                "article_usage": "",
                "preposition_usage": "",
                "conjunction_usage": "",
                "academic_conventions": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 