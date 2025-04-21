from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class EthicsComplianceAgent(BaseReviewerAgent):
    """Agent responsible for reviewing ethical considerations and research standards."""
    
    def __init__(self, model="gpt-4"):
        super().__init__(model)
        self.name = "R3_Ethics_Compliance_Agent"
        self.category = "Scientific Rigor"
        
    def analyze_ethics_compliance(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes ethical considerations and compliance with research standards."""
        prompt = f"""Analyze the following text for ethical considerations and research standards compliance. Focus on:
        1. Conflicts of interest
        2. Data privacy and protection
        3. Informed consent procedures
        4. Research integrity
        5. Adherence to ethical guidelines

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "ethics_compliance_score": int,  # Single comprehensive score (1-10)
            
            "critical_remarks": [{{
                "category": str,  # "conflicts", "privacy", "consent", "integrity", "guidelines"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects ethical compliance
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str  # Where to apply this change
            }}],
            
            "detailed_feedback": {{
                "conflicts_assessment": str,  # Detailed paragraph about conflicts of interest
                "privacy_compliance": str,  # Detailed paragraph about data privacy
                "consent_procedures": str,  # Detailed paragraph about informed consent
                "research_integrity": str,  # Detailed paragraph about research integrity
                "guidelines_adherence": str  # Detailed paragraph about ethical guidelines
            }},
            
            "summary": str  # Overall assessment paragraph
        }}
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing ethics and compliance: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "ethics_compliance_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "conflicts_assessment": "",
                "privacy_compliance": "",
                "consent_procedures": "",
                "research_integrity": "",
                "guidelines_adherence": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 