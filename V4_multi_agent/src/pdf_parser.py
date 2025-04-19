import os
import re
from typing import Dict, List, Tuple, Any, Optional
import PyPDF2

class PDFParser:
    """
    A class to parse PDF files and extract text content.
    """
    
    def __init__(self):
        """Initialize the PDF parser."""
        pass
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text content from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text content
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def get_metadata(self, pdf_path: str) -> Dict[str, Any]:
        """Extract metadata from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            Dict[str, Any]: Extracted metadata
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                metadata = reader.metadata
                return {
                    'title': metadata.get('/Title', ''),
                    'author': metadata.get('/Author', ''),
                    'subject': metadata.get('/Subject', ''),
                    'keywords': metadata.get('/Keywords', ''),
                    'creator': metadata.get('/Creator', ''),
                    'producer': metadata.get('/Producer', ''),
                    'creation_date': metadata.get('/CreationDate', ''),
                    'modification_date': metadata.get('/ModDate', ''),
                    'page_count': len(reader.pages)
                }
        except Exception as e:
            raise Exception(f"Error extracting metadata from PDF: {str(e)}")
    
    def detect_sections(self, pdf_path: str) -> Dict[str, List[str]]:
        """
        Detect sections in a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            Dict[str, List[str]]: Dictionary of section names and their content
        """
        text = self.extract_text(pdf_path)
        
        # Common section headers in academic papers
        section_patterns = {
            'abstract': r'abstract',
            'introduction': r'introduction',
            'methods': r'methods|methodology|materials and methods',
            'results': r'results|findings',
            'discussion': r'discussion',
            'conclusion': r'conclusion|conclusions',
            'references': r'references|bibliography',
            'acknowledgments': r'acknowledgments|acknowledgements'
        }
        
        sections = {name: [] for name in section_patterns.keys()}
        
        # Split text into lines
        lines = text.split('\n')
        
        current_section = None
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line is a section header
            found_section = False
            for section_name, pattern in section_patterns.items():
                if re.match(f'^{pattern}$', line_lower):
                    # Save previous section if exists
                    if current_section:
                        sections[current_section] = current_content
                    
                    # Start new section
                    current_section = section_name
                    current_content = [line]
                    found_section = True
                    break
            
            # If not a section header, add to current section
            if not found_section and current_section:
                current_content.append(line)
        
        # Save the last section
        if current_section:
            sections[current_section] = current_content
        
        return sections
    
    def get_references(self, pdf_path: str) -> List[str]:
        """
        Extract references from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            List[str]: List of references
        """
        text = self.extract_text(pdf_path)
        
        # Simple pattern for references (can be improved)
        reference_pattern = r'\[\d+\]|\(\d+\)'
        
        # Find the references section
        sections = self.detect_sections(pdf_path)
        references_text = '\n'.join(sections.get('references', []))
        
        if not references_text:
            return []
        
        # Extract references
        references = []
        lines = references_text.split('\n')
        
        for line in lines:
            if re.search(reference_pattern, line):
                references.append(line.strip())
        
        return references
    
    def get_figures_and_tables(self, pdf_path: str) -> Tuple[List[str], List[str]]:
        """
        Extract figures and tables from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            Tuple[List[str], List[str]]: Lists of figures and tables
        """
        text = self.extract_text(pdf_path)
        
        # Simple pattern matching for figures and tables
        figure_pattern = r'figure \d+|fig\. \d+'
        table_pattern = r'table \d+'
        
        figures = re.findall(figure_pattern, text.lower())
        tables = re.findall(table_pattern, text.lower())
        
        return figures, tables 