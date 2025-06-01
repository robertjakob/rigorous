import json
import os
from typing import Dict, List, Any
import openai
import PyPDF2
import requests
from io import BytesIO
from ...core.base_agent import BaseReviewerAgent

class QualityControlAgent(BaseReviewerAgent):
    """
    Quality Control Agent that reviews and validates the outputs from all other agents.
    It ensures the quality and consistency of the review process and provides a final,
    streamlined report.
    """
    
    def __init__(self, model: str = "gpt-4.1"):
        super().__init__(model)
        self.required_inputs = {
            'manuscript_path': str,
            'context_path': str,
            'rigor_results_path': str,
            'section_results_path': str,
            'writing_results_path': str
        }
        
        # Define section mappings with full names
        self.section_mappings = {
            'section_results': {
                'S1': 'Title and Keywords',
                'S2': 'Abstract',
                'S3': 'Introduction',
                'S4': 'Literature Review',
                'S5': 'Methodology',
                'S6': 'Results',
                'S7': 'Discussion',
                'S8': 'Conclusion',
                'S9': 'References',
                'S10': 'Supplementary Materials'
            },
            'rigor_results': {
                'R1': 'Originality and Contribution',
                'R2': 'Impact and Significance',
                'R3': 'Ethics and Compliance',
                'R4': 'Data and Code Availability',
                'R5': 'Statistical Rigor',
                'R6': 'Technical Accuracy',
                'R7': 'Consistency'
            },
            'writing_results': {
                'W1': 'Language and Style',
                'W2': 'Narrative and Structure',
                'W3': 'Clarity and Conciseness',
                'W4': 'Terminology Consistency',
                'W5': 'Inclusive Language',
                'W6': 'Citation Formatting',
                'W7': 'Target Audience Alignment'
            }
        }

    def load_json_file(self, file_path: str) -> Dict:
        """Load and parse a JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def extract_pdf_text(self, pdf_source: str) -> str:
        """Extract text from a PDF file or URL."""
        text = ""
    
        if pdf_source.startswith("http://") or pdf_source.startswith("https://"):
            # Source is a URL
            response = requests.get(pdf_source)
            response.raise_for_status()  # Raises error if the download failed
            pdf_file = BytesIO(response.content)
        else:
            # Source is a local file path
            pdf_file = open(pdf_source, 'rb')
        
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
        finally:
            if not isinstance(pdf_file, BytesIO):
                pdf_file.close()
        
        return text

    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing method that:
        1. Validates inputs
        2. Loads and analyzes all review outputs
        3. Produces a quality-controlled final report
        """              
        
        # Load all input data
        context = inputs['context']
        rigor_results = inputs['rigor_results']
        section_results = inputs['section_results']
        writing_results = inputs['writing_results']
                
        # Extract manuscript text
        manuscript_text = self.extract_pdf_text(inputs['manuscript_src'])       
        
        # Process each category separately
        final_results = {}
        
        # Process section results        
        print("Processing section results...")
        section_prompt = self.generate_category_prompt(
            'section_results',
            section_results,
            manuscript_text,
            context
        )
        section_analysis = json.loads(self.llm(section_prompt))
        final_results['section_results'] = section_analysis.get('section_results', {})
        
        # Process rigor results
        print("Processing rigor results...")
        rigor_prompt = self.generate_category_prompt(
            'rigor_results',
            rigor_results,
            manuscript_text,
            context
        )
        rigor_analysis = json.loads(self.llm(rigor_prompt))
        final_results['rigor_results'] = rigor_analysis.get('rigor_results', {})
        
        # Process writing results
        print("Processing writing results...")
        writing_prompt = self.generate_category_prompt(
            'writing_results',
            writing_results,
            manuscript_text,
            context
        )
        writing_analysis = json.loads(self.llm(writing_prompt))
        final_results['writing_results'] = writing_analysis.get('writing_results', {})
        
        # Format the output
        formatted_output = self.format_output(final_results)
        
        return formatted_output

    def generate_category_prompt(self, category: str, results: Dict, manuscript_text: str, context: Dict) -> str:
        """
        Generate a prompt for analyzing a specific category of results.
        """
        # Get section mappings for this category
        sections = self.section_mappings[category]
        
        # Create section headers
        section_headers = []
        for code, name in sections.items():
            section_headers.append(f"o   {code} – {name}")
        
        # Create example JSON structure for this category
        example_json = {
            category: {
                list(sections.keys())[0]: {
                    "section_name": sections[list(sections.keys())[0]],
                    "score": 4,
                    "summary": "Critical remarks, tips, and positive aspects...",
                    "suggestions": [
                        {
                            "remarks": "Issue description",
                            "original_text": "Original text from manuscript",
                            "improved_version": "Suggested improvement",
                            "explanation": "Explanation for the improvement"
                        }
                    ]
                }
            }
        }
        
        prompt = f"""You are a Quality Control Agent responsible for reviewing and validating the outputs from AI review agents. Your task is to analyze the {category.replace('_', ' ')} category:

Category Sections:
{''.join(section_headers)}

For each section, you should:
1. Validate the accuracy and relevance of the feedback
2. Identify the most critical and helpful suggestions (aim for ~3 per section)
3. Add any additional valuable insights
4. Note if any section is not applicable
5. Reassess the 1-5 score for each section

Structure your analysis in the following format for each section:
- A summary paragraph highlighting:
  * Critical remarks
  * Tips for improvement
  * Positive aspects of the manuscript
- For each suggestion (up to 3 per section):
  * Remarks
  * Original Text
  * Improved Version
  * Explanation for the improvement

Important guidelines:
- Avoid duplicate issues
- Focus on the most severe and helpful remarks
- Clearly mark non-applicable sections
- Maintain the existing JSON structure
- Ensure all feedback is constructive and actionable

Please analyze the following inputs:

Manuscript Text (Preview):
{manuscript_text[:1000]}...

Context:
{json.dumps(context, indent=2)}

{category.replace('_', ' ').title()} Results:
{json.dumps(results, indent=2)}

Provide your analysis in a structured JSON format that exactly matches this structure:
{json.dumps(example_json, indent=2)}

For each section:
1. Include the full section name
2. Provide a score (1-5)
3. Include a summary paragraph
4. Include up to 3 suggestions with remarks, original text, improved version, and explanation
5. If a section is not applicable, set status to "not_applicable" and include an appropriate message

Ensure your response is valid JSON and includes all required fields."""

        return prompt

    def format_output(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the analysis results into the required JSON structure.
        """
        try:
            # Validate the structure
            if not isinstance(analysis_results, dict):
                raise ValueError("Analysis results must be a dictionary")
            
            # Ensure all required sections are present with full names
            for category, sections in self.section_mappings.items():
                if category not in analysis_results:
                    raise ValueError(f"Missing category: {category}")
                
                for code, name in sections.items():
                    if code not in analysis_results[category]:
                        analysis_results[category][code] = {
                            'status': 'not_applicable',
                            'message': f'Not applicable - no {name} content detected',
                            'score': 0,
                            'section_name': name
                        }
                    else:
                        # Add section name to existing results
                        analysis_results[category][code]['section_name'] = name
            
            return analysis_results
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error formatting output: {str(e)}',
                'results': analysis_results
            } 