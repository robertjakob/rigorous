import fitz  # PyMuPDF
from typing import List, Dict, Optional

class PDFParser:
    """A class to handle PDF document parsing and text extraction."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize the PDF parser with a path to the PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file to be parsed
        """
        self.pdf_path = pdf_path
        self.doc = None
        
    def open_document(self) -> None:
        """Open the PDF document."""
        try:
            self.doc = fitz.open(self.pdf_path)
        except Exception as e:
            raise Exception(f"Failed to open PDF file: {str(e)}")
            
    def extract_text(self) -> str:
        """
        Extract all text from the PDF document.
        
        Returns:
            str: Extracted text from all pages
        """
        if not self.doc:
            self.open_document()
            
        text = ""
        for page in self.doc:
            text += page.get_text()
        return text
    
    def extract_text_with_positions(self) -> List[Dict[str, any]]:
        """
        Extract text from the PDF with position information for each block.
        
        Returns:
            List[Dict]: List of dictionaries containing text blocks with their positions
        """
        if not self.doc:
            self.open_document()
            
        blocks = []
        for page_num, page in enumerate(self.doc):
            blocks_dict = page.get_text("dict")
            for block in blocks_dict.get("blocks", []):
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        blocks.append({
                            "text": span.get("text", ""),
                            "page": page_num + 1,
                            "bbox": span.get("bbox", []),
                            "font": span.get("font", ""),
                            "size": span.get("size", 0)
                        })
        return blocks
    
    def close(self) -> None:
        """Close the PDF document."""
        if self.doc:
            self.doc.close()
            self.doc = None 