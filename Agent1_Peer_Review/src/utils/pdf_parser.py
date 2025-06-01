import os
import re
from typing import Dict, Any, List, Tuple
import PyPDF2
import fitz  # PyMuPDF for better PDF handling
import pytesseract
from PIL import Image
import io
import numpy as np
import requests
from io import BytesIO

class PDFParser:
    """Enhanced PDF parser with figure and table detection capabilities."""
    
    def __init__(self, pdf_source: str):
        """Initialize the PDF parser.
        
        Args:
            pdf_path (str): Path to the PDF file
        """
        if pdf_source.startswith("http://") or pdf_source.startswith("https://"):
            # Source is a URL
            response = requests.get(pdf_source)
            response.raise_for_status()
            pdf_file = BytesIO(response.content)
            self.doc = fitz.open("pdf", pdf_file)  # Open from bytes
        else:
            # Source is a local file path
            if not os.path.exists(pdf_source):
                raise FileNotFoundError(f"PDF file not found: {pdf_source}")
            self.doc = fitz.open(pdf_source)  # Open from file path
    
    def __del__(self):
        """Clean up by closing the document."""
        if hasattr(self, 'doc'):
            self.doc.close()
    
    def extract_text(self) -> str:
        """Extract text from the PDF using PyMuPDF for better accuracy."""
        text = ""
        try:
            for page in self.doc:
                text += page.get_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def get_metadata(self) -> Dict[str, str]:
        """Extract metadata from the PDF."""
        try:
            metadata = self.doc.metadata

            metadata_res = {
                'title': metadata.get('title', 'Unknown'),
                'author': metadata.get('author', 'Unknown'),
                'creation_date': metadata.get('creationDate', 'Unknown'),
                'page_count': str(self.doc.page_count)
            }            
            
            return metadata_res
        except Exception as e:
            raise Exception(f"Failed to extract metadata from PDF: {str(e)}")
    
    def extract_images(self) -> List[Dict[str, Any]]:
        """Extract images from the PDF with their locations and captions."""
        images = []
        try:
            for page_num, page in enumerate(self.doc):
                # Extract images
                image_list = page.get_images()
                
                for img_idx, img in enumerate(image_list):
                    xref = img[0]
                    base_image = self.doc.extract_image(xref)
                    
                    if base_image:
                        # Convert image data to PIL Image for analysis
                        image_data = base_image["image"]
                        image = Image.open(io.BytesIO(image_data))
                        
                        # Get image location on page
                        rect = page.get_image_rects(xref)[0]  # Get first occurrence
                        
                        # Try to find caption near the image
                        caption = self._find_caption_near_rect(page, rect, "Figure")
                        
                        images.append({
                            'page': page_num + 1,
                            'index': img_idx + 1,
                            'bbox': [rect.x0, rect.y0, rect.x1, rect.y1],  # Convert to list for JSON
                            'size': image.size,
                            'format': base_image["ext"],
                            'caption': caption,
                            'image_data': image_data  # Raw image data
                        })
            
            return images
        except Exception as e:
            raise Exception(f"Failed to extract images from PDF: {str(e)}")
    
    def extract_tables(self) -> List[Dict[str, Any]]:
        """Extract tables from the PDF using text analysis."""
        tables = []
        try:
            for page_num, page in enumerate(self.doc):
                # Find potential table regions using text analysis
                blocks = page.get_text("blocks")
                table_regions = self._identify_table_regions(blocks)
                
                for region_idx, region in enumerate(table_regions):
                    # Extract region text
                    table_text = page.get_text(clip=region)
                    
                    # Try to find caption near the table
                    caption = self._find_caption_near_rect(page, region, "Table")
                    
                    tables.append({
                        'page': page_num + 1,
                        'index': region_idx + 1,
                        'bbox': [region.x0, region.y0, region.x1, region.y1],  # Convert to list for JSON
                        'text': table_text,
                        'caption': caption
                    })
            
            return tables
        except Exception as e:
            raise Exception(f"Failed to extract tables from PDF: {str(e)}")
    
    def _identify_table_regions(self, blocks: List[Any]) -> List[fitz.Rect]:
        """Identify potential table regions using text block analysis."""
        table_regions = []
        current_region = None
        
        for block in blocks:
            text = block[4]
            rect = fitz.Rect(block[:4])
            
            # Heuristics for table detection
            if (self._looks_like_table_content(text) or
                self._looks_like_table_header(text)):
                if current_region is None:
                    current_region = rect
                else:
                    current_region = current_region | rect  # Union of rectangles
            elif current_region is not None:
                table_regions.append(current_region)
                current_region = None
        
        if current_region is not None:
            table_regions.append(current_region)
        
        return table_regions
    
    def _looks_like_table_content(self, text: str) -> bool:
        """Check if text block looks like table content."""
        # Heuristics for table content detection
        if not text.strip():
            return False
        
        # Check for regular patterns of numbers or short text segments
        lines = text.split('\n')
        if len(lines) < 2:
            return False
        
        # Check for consistent delimiters or spacing
        delimiter_pattern = re.compile(r'[\t|,]|\s{2,}')
        delimiter_counts = [len(re.findall(delimiter_pattern, line)) for line in lines]
        
        # If most lines have the same number of delimiters, likely a table
        return len(set(delimiter_counts)) <= 2
    
    def _looks_like_table_header(self, text: str) -> bool:
        """Check if text block looks like table header."""
        # Common table header indicators
        header_indicators = ['mean', 'std', 'min', 'max', 'total', 'average', 
                           'value', 'type', 'name', 'id', 'description']
        
        text_lower = text.lower()
        words = text_lower.split()
        
        # Check for header-like words
        return any(indicator in words for indicator in header_indicators)
    
    def _find_caption_near_rect(self, page: Any, rect: fitz.Rect, 
                               element_type: str) -> str:
        """Find caption near a given rectangle on the page."""
        # Create expanded search area
        margin = 20  # points
        search_rect = fitz.Rect(
            rect.x0 - margin,
            rect.y0 - margin,
            rect.x1 + margin,
            rect.y1 + margin
        )
        
        # Get text in the search area
        nearby_text = page.get_text("text", clip=search_rect)
        
        # Look for caption patterns
        caption_pattern = f"{element_type}\s*\d+[.:](.*?)(?:\n\n|$)"
        match = re.search(caption_pattern, nearby_text, re.IGNORECASE | re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return "" 