from typing import List, Dict, Any
from pdf_parser import PDFParser
from openai_client import OpenAIClient

class RequirementsChecker:
    """A class to orchestrate the manuscript requirements checking process."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the requirements checker.
        
        Args:
            api_key (str, optional): OpenAI API key
        """
        self.openai_client = OpenAIClient(api_key)
        
    def analyze_manuscript(self, pdf_path: str, requirements: List[str]) -> Dict[str, Any]:
        """
        Analyze a manuscript against the given requirements.
        
        Args:
            pdf_path (str): Path to the manuscript PDF file
            requirements (List[str]): List of editorial requirements to check
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        # Extract text from PDF
        pdf_parser = PDFParser(pdf_path)
        try:
            manuscript_text = pdf_parser.extract_text()
        finally:
            pdf_parser.close()
            
        # Analyze requirements using OpenAI
        analysis_results = self.openai_client.check_requirements(manuscript_text, requirements)
        
        return analysis_results
    
    def format_results(self, results: Dict[str, Any]) -> str:
        """
        Format the analysis results into a readable string.
        
        Args:
            results (Dict[str, Any]): Analysis results from OpenAI
            
        Returns:
            str: Formatted results
        """
        output = []
        output.append("=== Manuscript Requirements Analysis ===\n")
        
        # Format requirements analysis
        for req_analysis in results["requirements_analysis"]:
            output.append(f"Requirement: {req_analysis['requirement']}")
            output.append(f"Status: {'✓ Met' if req_analysis['is_met'] else '✗ Not Met'}")
            if not req_analysis['is_met']:
                output.append(f"Evidence: {req_analysis['evidence']}")
            output.append(f"Explanation: {req_analysis['explanation']}\n")
            
        # Format desk rejection recommendation
        rejection = results["desk_rejection_recommendation"]
        output.append("=== Final Recommendation ===")
        output.append(f"Desk Rejection: {'Yes' if rejection['should_reject'] else 'No'}")
        output.append(f"Justification: {rejection['justification']}")
        
        return "\n".join(output) 