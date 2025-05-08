from typing import List, Dict, Any
from pdf_parser import PDFParser
from openai_client import OpenAIClient

class RequirementsChecker:
    """A class to check manuscript requirements using OpenAI's GPT model."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the requirements checker.
        
        Args:
            api_key (str, optional): OpenAI API key
        """
        self.openai_client = OpenAIClient(api_key)
    
    def check_manuscript(self, pdf_path: str, requirements: List[str]) -> Dict[str, Any]:
        """
        Check if a manuscript meets the given requirements.
        
        Args:
            pdf_path (str): Path to the PDF manuscript
            requirements (List[str]): List of requirements to check
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        # Parse PDF with structure preservation
        pdf_parser = PDFParser(pdf_path)
        manuscript_text = pdf_parser.extract_text()
        
        # Get sections for better context
        sections = pdf_parser.detect_sections()
        
        # Calculate word count
        word_count = len(manuscript_text.split())
        
        # Add metadata and section information to the text
        structured_text = f"""Document Metadata:
Word Count: {word_count} words

Document Structure:
"""
        for section, content in sections.items():
            section_text = ' '.join(content)
            section_word_count = len(section_text.split())
            structured_text += f"\n{section} ({section_word_count} words):\n{section_text}\n"
        
        # Check requirements using OpenAI
        analysis = self.openai_client.check_requirements(structured_text, requirements)
        
        return analysis
    
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
            output.append(f"Evidence: {req_analysis['evidence']}")
            output.append(f"Explanation: {req_analysis['explanation']}\n")
            
        # Format desk rejection recommendation
        rejection = results["desk_rejection_recommendation"]
        output.append("=== Final Recommendation ===")
        output.append(f"Desk Rejection: {'Yes' if rejection['should_reject'] else 'No'}")
        output.append(f"Justification: {rejection['justification']}")
        
        return "\n".join(output) 