from typing import Dict, Any, List
from pdf_parser import PDFParser
from openai_client import OpenAIClient

class PeerReviewChecker:
    """A class to coordinate the peer review process."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the peer review checker.
        
        Args:
            api_key (str, optional): OpenAI API key
        """
        self.openai_client = OpenAIClient(api_key)
        
    def review_manuscript(self, pdf_path: str, review_criteria: Dict[str, str]) -> Dict[str, Any]:
        """
        Review a manuscript using the specified criteria.
        
        Args:
            pdf_path (str): Path to the PDF manuscript
            review_criteria (Dict[str, str]): Dictionary of review criteria and their descriptions
            
        Returns:
            Dict[str, Any]: Review results
        """
        # Parse PDF
        pdf_parser = PDFParser(pdf_path)
        
        # Get manuscript metadata
        metadata = pdf_parser.get_metadata()
        
        # Extract text and structure
        manuscript_text = pdf_parser.extract_text()
        sections = pdf_parser.detect_sections()
        
        # Get references and figures/tables
        references = pdf_parser.get_references()
        figures, tables = pdf_parser.get_figures_and_tables()
        
        # Add metadata and structure information to the text
        structured_text = f"""Document Metadata:
Title: {metadata['title']}
Author: {metadata['author']}
Pages: {metadata['page_count']}
Creation Date: {metadata['creation_date']}

Document Structure:
"""
        for section, content in sections.items():
            section_text = ' '.join(content)
            section_word_count = len(section_text.split())
            structured_text += f"\n{section} ({section_word_count} words):\n{section_text}\n"
            
        # Add references and figures/tables information
        structured_text += f"\nReferences ({len(references)}):\n" + "\n".join(references)
        structured_text += f"\n\nFigures ({len(figures)}):\n" + "\n".join(figures)
        structured_text += f"\n\nTables ({len(tables)}):\n" + "\n".join(tables)
        
        # Analyze manuscript using OpenAI
        analysis = self.openai_client.analyze_manuscript(structured_text, review_criteria)
        
        # Add metadata to the analysis results
        analysis['metadata'] = metadata
        analysis['statistics'] = {
            'total_references': len(references),
            'total_figures': len(figures),
            'total_tables': len(tables),
            'total_sections': len(sections)
        }
        
        return analysis
        
    def format_results(self, results: Dict[str, Any]) -> str:
        """
        Format the review results into a readable string.
        
        Args:
            results (Dict[str, Any]): Review results
            
        Returns:
            str: Formatted results
        """
        output = []
        
        # Add metadata section
        output.append("=== Manuscript Metadata ===")
        for key, value in results['metadata'].items():
            output.append(f"{key}: {value}")
            
        # Add statistics section
        output.append("\n=== Document Statistics ===")
        for key, value in results['statistics'].items():
            output.append(f"{key}: {value}")
            
        # Add overall assessment
        output.append("\n=== Overall Assessment ===")
        output.append(f"Score: {results['overall_assessment']['score']}/5")
        output.append(f"Summary: {results['overall_assessment']['summary']}")
        output.append(f"Recommendation: {results['recommendation']}")
        output.append(f"Confidence: {results['confidence']*100:.1f}%")
        
        # Add criteria assessments
        output.append("\n=== Detailed Assessment ===")
        for criterion, assessment in results['criteria_assessments'].items():
            output.append(f"\n{criterion}")
            output.append(f"Score: {assessment['score']}/5")
            output.append(f"Feedback: {assessment['feedback']}")
            
            if assessment['examples']:
                output.append("\nExamples:")
                for example in assessment['examples']:
                    output.append(f"- {example}")
                    
            if assessment['suggestions']:
                output.append("\nSuggestions for Improvement:")
                for suggestion in assessment['suggestions']:
                    output.append(f"- {suggestion}")
                    
        return "\n".join(output) 