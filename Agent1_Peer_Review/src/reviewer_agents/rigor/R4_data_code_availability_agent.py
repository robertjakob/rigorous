from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class DataCodeAvailabilityAgent(BaseReviewerAgent):
    """Agent responsible for evaluating data and code availability."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "R4_Data_Code_Availability_Agent"
        self.category = "Scientific Rigor"
        
    def analyze_data_code_availability(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes data and code availability."""
        prompt = f"""Analyze the following text for data and code availability. Focus on:
        1. Data sharing practices
        2. Code repository availability
        3. Documentation completeness
        4. Access restrictions justification
        5. Reproducibility support

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Abstract: Data/code availability statement
        - Introduction: Research transparency approach
        - Methodology: Data collection details, code implementation
        - Data Description: Dataset structure, access methods
        - Code Documentation: Implementation details, usage instructions
        - Results: Data presentation, code results
        - Discussion: Reproducibility considerations
        - Conclusion: Availability summary, access information

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "data_code_availability_score": int,  # Single comprehensive score (1-5)
            # IMPORTANT: The score MUST be between 1 and 5, where:
            # 1 = Poor: Major issues that significantly impact quality
            # 2 = Below Average: Several notable issues that need attention
            # 3 = Average: Some issues but generally acceptable
            # 4 = Good: Minor issues that don't significantly impact quality
            # 5 = Excellent: Very few or no issues, high quality
            
            "critical_remarks": [{{
                "category": str,  # "data_sharing", "code_availability", "documentation", "restrictions", "reproducibility"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects research transparency
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "abstract", "introduction", "methodology", "data_description", "code_documentation", "results", "discussion", "conclusion"
                "focus": str  # "data_sharing", "code_availability", "documentation", "restrictions", "reproducibility"
            }}],
            
            "detailed_feedback": {{
                "data_sharing_assessment": str,  # Detailed paragraph about data sharing
                "code_availability": str,  # Detailed paragraph about code availability
                "documentation_completeness": str,  # Detailed paragraph about documentation
                "restrictions_justification": str,  # Detailed paragraph about access restrictions
                "reproducibility_support": str  # Detailed paragraph about reproducibility
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances data and code availability.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing data and code availability: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "data_code_availability_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "data_sharing_assessment": "",
                "code_availability": "",
                "documentation_completeness": "",
                "restrictions_justification": "",
                "reproducibility_support": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 