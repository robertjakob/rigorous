import json
import os
from typing import Dict, Any
import PyPDF2
import requests
from io import BytesIO
from ..core.base_agent import BaseReviewerAgent

class ExecutiveSummaryAgent(BaseReviewerAgent):
    """
    Executive Summary Agent that generates a high-level summary of the review results
    and calculates overall scores based on the quality control results.
    """
    
    def __init__(self, model: str = "gpt-4.1"):
        super().__init__(model)
        self.required_inputs = {
            'manuscript_path': str,
            'context_path': str,
            'quality_control_results_path': str
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

    def extract_title(self, pdf_path: str) -> str:
        """Extract title from the first page of the PDF."""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            first_page = pdf_reader.pages[0]
            text = first_page.extract_text()
            # Assuming title is in the first few lines
            lines = text.split('\n')
            for line in lines[:5]:  # Check first 5 lines
                if line.strip() and len(line.strip()) > 10:  # Basic title validation
                    return line.strip()
        return "Title not found"

    def calculate_scores(self, quality_control_results: Dict) -> Dict[str, float]:
        """Calculate overall scores from quality control results."""
        scores = {
            'section_score': 0.0,
            'rigor_score': 0.0,
            'writing_score': 0.0,
            'final_score': 0.0
        }
        
        # Calculate section score (S1-S10)
        section_scores = []
        for i in range(1, 11):
            section_key = f'S{i}'
            if section_key in quality_control_results.get('section_results', {}):
                section_scores.append(quality_control_results['section_results'][section_key]['score'])
        if section_scores:
            scores['section_score'] = sum(section_scores) / len(section_scores)
        
        # Calculate rigor score (R1-R7)
        rigor_scores = []
        for i in range(1, 8):
            rigor_key = f'R{i}'
            if rigor_key in quality_control_results.get('rigor_results', {}):
                rigor_scores.append(quality_control_results['rigor_results'][rigor_key]['score'])
        if rigor_scores:
            scores['rigor_score'] = sum(rigor_scores) / len(rigor_scores)
        
        # Calculate writing score (W1-W7)
        writing_scores = []
        for i in range(1, 8):
            writing_key = f'W{i}'
            if writing_key in quality_control_results.get('writing_results', {}):
                writing_scores.append(quality_control_results['writing_results'][writing_key]['score'])
        if writing_scores:
            scores['writing_score'] = sum(writing_scores) / len(writing_scores)
        
        # Calculate final score
        category_scores = [scores['section_score'], scores['rigor_score'], scores['writing_score']]
        if category_scores:
            scores['final_score'] = sum(category_scores) / len(category_scores)
        
        return scores

    def validate_context(self, context: Dict) -> Dict:
        """Validate and sanitize context data, providing defaults for missing or invalid values."""
        # Initialize default values
        sanitized_context = {
            'target_publication_outlets': {
                'user_input': 'the target journal'
            },
            'review_focus_areas': {
                'user_input': 'general aspects'
            }
        }
        
        # Validate target publication outlets
        if isinstance(context.get('target_publication_outlets'), dict):
            user_input = context['target_publication_outlets'].get('user_input')
            if isinstance(user_input, str) and user_input.strip():
                sanitized_context['target_publication_outlets']['user_input'] = user_input.strip()
        
        # Validate review focus areas
        if isinstance(context.get('review_focus_areas'), dict):
            user_input = context['review_focus_areas'].get('user_input')
            if isinstance(user_input, str) and user_input.strip():
                sanitized_context['review_focus_areas']['user_input'] = user_input.strip()
        
        return sanitized_context

    def generate_independent_review(self, manuscript_text: str, context: Dict) -> str:
        """Generate an independent high-level review of the manuscript using GPT-4.1."""
        # Sanitize context
        sanitized_context = self.validate_context(context)
        target_journal = sanitized_context['target_publication_outlets']['user_input']
        focus_areas = sanitized_context['review_focus_areas']['user_input']
        
        prompt = f"""You are an expert reviewer for {target_journal}. Read the following manuscript content and user priorities, then independently write a high-level review in three paragraphs:

Manuscript Content:
{manuscript_text[:6000]}

User Priorities:
- Target Journal: {target_journal}
- Focus Areas: {focus_areas}

Write:
1. A summary of what the manuscript is about
2. The main strengths and weaknesses, with special attention to {focus_areas}
3. The most critical suggestions for improvement, considering {target_journal} standards

Be concise, professional, and focus on the most important points. Do not reference any other reviews or JSON files yet."""
        response = self.llm(prompt)
        return response.strip()

    def generate_balanced_summary(self, independent_review: str, quality_control_results: Dict, context: Dict) -> str:
        """Balance the agent's own review with the quality-controlled review JSON."""
        # Sanitize context
        sanitized_context = self.validate_context(context)
        target_journal = sanitized_context['target_publication_outlets']['user_input']
        focus_areas = sanitized_context['review_focus_areas']['user_input']
        
        prompt = f"""You are an Executive Summary Agent for {target_journal}. You have two sources:
1. Your own independent review of the manuscript (below)
2. The quality-controlled review JSON (below)

First, extract the manuscript's title from the content. Then, write a unified executive summary in three paragraphs that:
- Provides a clear, concise overview of the manuscript
- Presents a balanced assessment of strengths and weaknesses
- Offers specific, actionable recommendations for improvement

IMPORTANT: While the quality-controlled review JSON provides valuable insights, your executive summary should:
- Draw naturally from both your independent review and the quality control findings
- Focus on the most significant and impactful points, regardless of source
- Present a cohesive narrative that flows naturally
- Avoid mechanically listing points from either source

Your Own Review:
{independent_review}

User Priorities:
- Target Journal: {target_journal}
- Focus Areas: {focus_areas}

Quality-Controlled Review (JSON):
{json.dumps(quality_control_results, indent=2)}

First, extract the manuscript's title. Then write a cohesive executive summary that:
1. Summarizes the manuscript's content and contribution, highlighting its key insights and significance
2. Evaluates its strengths and weaknesses, with special attention to {focus_areas}
3. Provides clear, actionable recommendations for improvement

Format your response as a JSON object with two fields:
1. "title": The extracted manuscript title
2. "executive_summary": The three-paragraph summary

Keep the summary within half a page (about 250 words), use professional language, and be specific and constructive. Write as a single, unified document that flows naturally while incorporating insights from both sources."""
        response = self.llm(prompt)
        return response.strip()

    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing method that:
        1. Validates inputs
        2. Extracts necessary information
        3. Generates an independent review
        4. Synthesizes a balanced executive summary
        5. Calculates scores
        6. Produces final output
        """        
        
        
        context = inputs['context']
        quality_control_results = inputs['quality_control_results']
        
        # Extract manuscript text       
        manuscript_text = self.extract_pdf_text(inputs['manuscript_src'])
        
        # Step 1: Generate independent review
        independent_review = self.generate_independent_review(manuscript_text, context)
        
        # Step 2: Synthesize balanced executive summary and extract title
        summary_response = self.generate_balanced_summary(independent_review, quality_control_results, context)
        try:
            summary_data = json.loads(summary_response)
            title = summary_data.get('title', 'Title not found')
            summary = summary_data.get('executive_summary', '')
        except json.JSONDecodeError:
            print("Warning: Could not parse summary response as JSON. Using raw response.")
            title = 'Title not found'
            summary = summary_response
        
        # Calculate scores
        scores = self.calculate_scores(quality_control_results)
        
        # Prepare output
        output = {
            'manuscript_title': title,
            'executive_summary': summary,
            'publication_outlets': context['target_publication_outlets']['user_input'],
            'review_focus': context['review_focus_areas']['user_input'],
            'independent_review': independent_review,
            'scores': scores
        }
        
        return output

    def save_results(self, results: Dict[str, Any], output_path: str) -> None:
        """Save the results to a JSON file."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Executive summary results saved to {output_path}") 