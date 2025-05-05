import os
import re
from typing import Dict, List, Tuple
import PyPDF2

class PDFParser:
    """A class to parse PDF manuscripts and extract structured content."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize the PDF parser.
        
        Args:
            pdf_path (str): Path to the PDF file
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        self.pdf_path = pdf_path
        
    def extract_text(self) -> str:
        """
        Extract text from the PDF file.
        
        Returns:
            str: Extracted text
        """
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
            
    def detect_sections(self) -> Dict[str, List[str]]:
        """
        Detect and extract sections from the manuscript.
        
        Returns:
            Dict[str, List[str]]: Dictionary of section names and their content
        """
        text = self.extract_text()
        
        # Common section headers in academic papers
        section_patterns = {
            'Abstract': r'Abstract[\s\S]*?(?=\n\n|\n[A-Z][a-z]+:)',
            'Introduction': r'Introduction[\s\S]*?(?=\n\n|\n[A-Z][a-z]+:)',
            'Methods': r'(Methods|Methodology|Materials and Methods)[\s\S]*?(?=\n\n|\n[A-Z][a-z]+:)',
            'Results': r'Results[\s\S]*?(?=\n\n|\n[A-Z][a-z]+:)',
            'Discussion': r'Discussion[\s\S]*?(?=\n\n|\n[A-Z][a-z]+:)',
            'Conclusion': r'(Conclusion|Conclusions)[\s\S]*?(?=\n\n|\n[A-Z][a-z]+:)',
            'References': r'(References|Bibliography)[\s\S]*?(?=\n\n|\n[A-Z][a-z]+:|$)'
        }
        
        sections = {}
        for section_name, pattern in section_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                section_text = match.group(0).strip()
                # Clean up the section text
                section_text = re.sub(r'^\w+\s*', '', section_text)  # Remove section header
                sections[section_name] = section_text.split('\n')
                
        return sections
        
    def get_metadata(self) -> Dict[str, str]:
        """
        Extract metadata from the PDF.
        
        Returns:
            Dict[str, str]: Dictionary of metadata
        """
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                metadata = reader.metadata
                
                return {
                    'title': metadata.get('/Title', 'Unknown'),
                    'author': metadata.get('/Author', 'Unknown'),
                    'creation_date': metadata.get('/CreationDate', 'Unknown'),
                    'page_count': str(len(reader.pages))
                }
        except Exception as e:
            raise Exception(f"Failed to extract metadata from PDF: {str(e)}")
            
    def get_references(self) -> List[str]:
        """
        Extract references from the manuscript.
        
        Returns:
            List[str]: List of references
        """
        sections = self.detect_sections()
        if 'References' in sections:
            return sections['References']
        return []
        
    def get_figures_and_tables(self) -> Tuple[List[str], List[str]]:
        """
        Extract figures and tables from the manuscript.
        
        Returns:
            Tuple[List[str], List[str]]: Lists of figures and tables
        """
        text = self.extract_text()
        
        # Simple pattern matching for figures and tables
        figure_pattern = r'Figure \d+[.:].*?(?=\n\n|\n[A-Z][a-z]+:)'
        table_pattern = r'Table \d+[.:].*?(?=\n\n|\n[A-Z][a-z]+:)'
        
        figures = re.findall(figure_pattern, text, re.IGNORECASE | re.DOTALL)
        tables = re.findall(table_pattern, text, re.IGNORECASE | re.DOTALL)
        
        return figures, tables 