import fitz  # PyMuPDF
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class TextBlock:
    """Represents a block of text with its properties."""
    text: str
    page: int
    font_size: float
    font_name: str
    is_bold: bool
    is_italic: bool
    bbox: Tuple[float, float, float, float]

class PDFParser:
    """A class to parse PDF manuscripts with advanced text extraction capabilities."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize the PDF parser.
        
        Args:
            pdf_path (str): Path to the PDF file
        """
        self.pdf_path = pdf_path
        self.doc = None
        self.text_blocks = []
        
    def extract_text(self) -> str:
        """
        Extract text from the PDF with structure preservation.
        
        Returns:
            str: Extracted and structured text
        """
        try:
            self.doc = fitz.open(self.pdf_path)
            self.text_blocks = []
            
            # Process first 10 pages or less
            max_pages = min(10, len(self.doc))
            
            for page_num in range(max_pages):
                page = self.doc[page_num]
                blocks = self._extract_page_blocks(page, page_num)
                self.text_blocks.extend(blocks)
            
            # Sort blocks by position and process
            self.text_blocks.sort(key=lambda b: (b.page, b.bbox[1], b.bbox[0]))
            
            # Combine blocks into structured text
            structured_text = self._combine_blocks()
            
            return structured_text
            
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
        finally:
            if self.doc:
                self.doc.close()
    
    def _extract_page_blocks(self, page: fitz.Page, page_num: int) -> List[TextBlock]:
        """
        Extract text blocks from a page with formatting information.
        
        Args:
            page (fitz.Page): PDF page
            page_num (int): Page number
            
        Returns:
            List[TextBlock]: List of text blocks with formatting
        """
        blocks = []
        
        # Get text with formatting information
        text_dict = page.get_text("dict")
        
        for block in text_dict.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    # Extract text and formatting
                    text = span.get("text", "").strip()
                    if not text:
                        continue
                        
                    font = span.get("font", "")
                    size = span.get("size", 0)
                    bbox = span.get("bbox", [0, 0, 0, 0])
                    
                    # Check for bold/italic
                    flags = span.get("flags", 0)
                    is_bold = bool(flags & 2**1)  # Check bold flag
                    is_italic = bool(flags & 2**0)  # Check italic flag
                    
                    blocks.append(TextBlock(
                        text=text,
                        page=page_num + 1,
                        font_size=size,
                        font_name=font,
                        is_bold=is_bold,
                        is_italic=is_italic,
                        bbox=tuple(bbox)
                    ))
        
        return blocks
    
    def _combine_blocks(self) -> str:
        """
        Combine text blocks into structured text.
        
        Returns:
            str: Structured text
        """
        structured_text = []
        current_section = None
        
        for block in self.text_blocks:
            text = block.text
            
            # Detect headers based on font size and style
            if block.font_size > 12 and block.is_bold:
                if current_section:
                    structured_text.append("\n")
                current_section = text
                structured_text.append(f"\n{text}\n")
            else:
                # Regular text
                structured_text.append(text)
                
                # Add space between paragraphs
                if text.endswith(('.', '!', '?')):
                    structured_text.append("\n")
        
        return " ".join(structured_text)
    
    def get_word_count(self, text: str) -> int:
        """
        Get the word count of the text.
        
        Args:
            text (str): Text to count words in
            
        Returns:
            int: Word count
        """
        return len(text.split())
    
    def detect_sections(self) -> Dict[str, List[str]]:
        """
        Detect major sections in the document.
        
        Returns:
            Dict[str, List[str]]: Dictionary of sections and their content
        """
        sections = {}
        current_section = "Introduction"
        current_content = []
        
        for block in self.text_blocks:
            # Detect section headers
            if block.font_size > 12 and block.is_bold:
                if current_content:
                    sections[current_section] = current_content
                current_section = block.text
                current_content = []
            else:
                current_content.append(block.text)
        
        # Add the last section
        if current_content:
            sections[current_section] = current_content
        
        return sections 