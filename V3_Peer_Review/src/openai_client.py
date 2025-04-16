import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

class OpenAIClient:
    """A class to handle interactions with the OpenAI API for peer review."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the OpenAI client.
        
        Args:
            api_key (str, optional): OpenAI API key. If not provided, will try to load from environment.
        """
        # Try to load .env from the current directory
        load_dotenv()
        
        # If API key is not found, try to load from parent directory
        if not os.getenv("OPENAI_API_KEY"):
            # Get the path to the parent directory (two levels up from this file)
            parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            env_path = os.path.join(parent_dir, ".env")
            if os.path.exists(env_path):
                load_dotenv(env_path)
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        self.client = OpenAI(api_key=self.api_key)
        
    def analyze_manuscript(self, manuscript_text: str, review_criteria: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze a manuscript using GPT-4 for comprehensive peer review.
        
        Args:
            manuscript_text (str): The full text of the manuscript
            review_criteria (Dict[str, str]): Dictionary of review criteria and their descriptions
            
        Returns:
            Dict[str, Any]: Analysis results including scores and detailed feedback
        """
        # Truncate manuscript text to first 4000 words to reduce token usage
        words = manuscript_text.split()
        truncated_text = ' '.join(words[:4000]) if len(words) > 4000 else manuscript_text
        
        prompt = self._create_review_prompt(truncated_text, review_criteria)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # Using GPT-4 for more sophisticated analysis
                messages=[
                    {"role": "system", "content": "You are an expert peer reviewer with extensive experience in academic publishing. Analyze manuscripts thoroughly and provide detailed, constructive feedback. Be objective and evidence-based in your assessment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000  # Increased token limit for detailed feedback
            )
            
            return self._parse_response(response.choices[0].message.content)
            
        except Exception as e:
            raise Exception(f"Failed to analyze manuscript: {str(e)}")
            
    def _create_review_prompt(self, manuscript_text: str, review_criteria: Dict[str, str]) -> str:
        """
        Create a prompt for the peer review analysis.
        
        Args:
            manuscript_text (str): The manuscript text
            review_criteria (Dict[str, str]): Review criteria and descriptions
            
        Returns:
            str: Formatted prompt for the OpenAI API
        """
        criteria_section = "\n".join([f"- {criterion}: {description}" 
                                    for criterion, description in review_criteria.items()])
        
        return f"""Please analyze the following manuscript according to these criteria:

{criteria_section}

For each criterion:
1. Provide a score from 1-5 (1 being lowest, 5 being highest)
2. Give detailed, constructive feedback
3. Support your assessment with specific examples from the text
4. Suggest specific improvements where applicable

Manuscript text:
{manuscript_text}

Please format your response as a JSON object with the following structure:
{{
    "overall_assessment": {{
        "score": <1-5>,
        "summary": "<brief summary of overall assessment>"
    }},
    "criteria_assessments": {{
        "<criterion_name>": {{
            "score": <1-5>,
            "feedback": "<detailed feedback>",
            "examples": ["<specific example 1>", "<specific example 2>"],
            "suggestions": ["<improvement suggestion 1>", "<improvement suggestion 2>"]
        }}
    }},
    "recommendation": "<accept/revise/reject>",
    "confidence": <0-1>
}}"""
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the OpenAI API response into a structured format.
        
        Args:
            response (str): Raw response from the API
            
        Returns:
            Dict[str, Any]: Parsed response
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            raise Exception("Failed to parse OpenAI response as JSON") 