from typing import Dict, Any, List
import json
from PIL import Image
import io
from ...core.base_agent import BaseReviewerAgent

class VisualPresentationAgentW8(BaseReviewerAgent):
    """Agent responsible for evaluating visual presentation elements in the manuscript."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "W8_Visual_Presentation_Agent"
        self.category = "Writing and Presentation"
    
    def analyze_visual_presentation(self, text: str, research_type: str,
                                  images: List[Dict[str, Any]] = None,
                                  tables: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyzes the quality, clarity, and effectiveness of visual elements in the manuscript.
        
        Args:
            text (str): The manuscript text
            research_type (str): Type of research paper
            images (List[Dict[str, Any]], optional): List of extracted images with metadata
            tables (List[Dict[str, Any]], optional): List of extracted tables with metadata
        """
        # Prepare image and table information for analysis
        image_info = self._format_image_info(images) if images else []
        table_info = self._format_table_info(tables) if tables else []
        
        prompt = f"""Analyze the visual presentation quality and effectiveness of the following manuscript.
        The manuscript contains {len(image_info)} figures and {len(table_info)} tables.
        
        Manuscript Text: {text}
        Research Type: {research_type}
        
        Figures Information:
        {json.dumps(image_info, indent=2)}
        
        Tables Information:
        {json.dumps(table_info, indent=2)}
        
        Focus on:
        1. Figure quality and clarity
        2. Table formatting and readability
        3. Visual element placement
        4. Caption completeness
        5. Color scheme appropriateness
        6. Data visualization effectiveness
        7. Visual hierarchy
        8. Accessibility considerations
        9. Consistency in visual style
        10. Integration with text
        
        For each section, provide specific improvement suggestions. Consider:
        - Figures: Quality, clarity, resolution, and effectiveness
        - Tables: Formatting, readability, and structure
        - Diagrams: Clarity and information density
        - Charts: Data representation and interpretation
        - Visual consistency: Style and formatting across elements
        - Accessibility: Color contrast and readability
        - Integration: How well visuals support the text
        - Captions: Completeness and clarity
        
        Provide a detailed analysis in the following JSON format:
        {{
            "visual_presentation_score": int,  # Single comprehensive score (1-10)
            
            "critical_remarks": [{{
                "category": str,  # Category of the issue
                "location": str,  # Specific figure/table reference
                "issue": str,  # Detailed description
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects reader understanding
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # Current caption/reference
                "improved_version": str,  # Suggested improvement
                "explanation": str,  # Why this helps
                "location": str,  # Where to apply
                "category": str,  # Element type
                "focus": str  # Aspect being improved
            }}],
            
            "detailed_feedback": {{
                "figure_quality": str,
                "table_formatting": str,
                "visual_placement": str,
                "caption_completeness": str,
                "color_scheme": str,
                "data_visualization": str,
                "visual_hierarchy": str,
                "accessibility": str,
                "visual_consistency": str,
                "text_integration": str
            }},
            
            "summary": str  # Overall assessment
        }}
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing visual presentation: {str(e)}")
    
    def _format_image_info(self, images: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format image information for analysis."""
        formatted_images = []
        for img in images:
            # Create PIL Image from image data if available
            image_stats = {}
            if img.get('image_data'):
                try:
                    pil_image = Image.open(io.BytesIO(img['image_data']))
                    image_stats = {
                        'size': pil_image.size,
                        'mode': pil_image.mode,
                        'format': pil_image.format
                    }
                except Exception:
                    image_stats = {'error': 'Failed to analyze image data'}
            
            formatted_images.append({
                'page': img.get('page'),
                'index': img.get('index'),
                'caption': img.get('caption', ''),
                'location': f"Page {img.get('page')}, Figure {img.get('index')}",
                'stats': image_stats
            })
        return formatted_images
    
    def _format_table_info(self, tables: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format table information for analysis."""
        formatted_tables = []
        for table in tables:
            formatted_tables.append({
                'page': table.get('page'),
                'index': table.get('index'),
                'caption': table.get('caption', ''),
                'location': f"Page {table.get('page')}, Table {table.get('index')}",
                'content_preview': table.get('text', '')[:200] + '...' if table.get('text') else ''
            })
        return formatted_tables
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generate a structured error report."""
        return {
            'visual_presentation_score': 0,
            'critical_remarks': [],
            'improvement_suggestions': [],
            'detailed_feedback': {
                'figure_quality': '',
                'table_formatting': '',
                'visual_placement': '',
                'caption_completeness': '',
                'color_scheme': '',
                'data_visualization': '',
                'visual_hierarchy': '',
                'accessibility': '',
                'visual_consistency': '',
                'text_integration': ''
            },
            'summary': f"Error in analysis: {error_message}",
            'error': True
        } 