import os
import json
import re
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

class OpenAIClient:
    """A class to handle interactions with the OpenAI API for peer review."""
    
    def __init__(self):
        """Initialize the OpenAI client with API key from environment."""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        
    def _clean_json_string(self, json_str: str) -> str:
        """Clean up common JSON formatting issues.
        
        Args:
            json_str (str): The JSON string to clean
            
        Returns:
            str: The cleaned JSON string
        """
        # Remove trailing commas in objects and arrays
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        
        # Remove any text before the first { and after the last }
        start_idx = json_str.find('{')
        end_idx = json_str.rfind('}') + 1
        if start_idx >= 0 and end_idx > start_idx:
            json_str = json_str[start_idx:end_idx]
        
        return json_str
        
    def analyze_manuscript(self, manuscript_text: str, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a manuscript using GPT-3.5-turbo.
        
        Args:
            manuscript_text (str): The text content of the manuscript
            criteria (Dict[str, Any]): The review criteria to use
            
        Returns:
            Dict[str, Any]: The analysis results
        """
        prompt = self._create_review_prompt(manuscript_text, criteria)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using GPT-3.5-turbo for testing
                messages=[
                    {"role": "system", "content": """You are an expert peer reviewer for scientific manuscripts. 
Your task is to provide detailed, constructive feedback using the specified criteria.
IMPORTANT: You must format your entire response as a valid JSON object.
Do not include any text outside the JSON object.
All property names must be enclosed in double quotes.
All string values must be enclosed in double quotes.
Use square brackets for arrays.
Use proper JSON syntax for nested objects.
Do not use trailing commas."""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000  # Reduced token limit for GPT-3.5-turbo
            )
            
            # Parse the response into the expected format
            review_text = response.choices[0].message.content
            try:
                # Clean and parse the JSON
                cleaned_json = self._clean_json_string(review_text)
                return json.loads(cleaned_json)
            except Exception as e:
                print(f"Error parsing review response: {e}")
                print(f"Raw response: {review_text}")
                print(f"Cleaned JSON: {cleaned_json}")
                return {
                    "error": "Failed to parse review response",
                    "raw_response": review_text
                }
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return {
                "error": "Failed to get review from OpenAI",
                "details": str(e)
            }
            
    def _create_review_prompt(self, manuscript_text: str, criteria: Dict[str, Any]) -> str:
        """
        Create a prompt for the review request.
        
        Args:
            manuscript_text (str): The text content of the manuscript
            criteria (Dict[str, Any]): The review criteria to use
            
        Returns:
            str: The formatted prompt
        """
        return f"""IMPORTANT: Your response must be a single, valid JSON object. Do not include any text outside the JSON.
All property names and string values must be enclosed in double quotes.
Do not use trailing commas in objects or arrays.

Review the following manuscript according to these criteria:

{json.dumps(criteria, indent=2)}

Manuscript text:
{manuscript_text[:4000]}  # Further limit text length for GPT-3.5-turbo

Provide your review as a JSON object with exactly this structure:
{{
    "ratings": {{
        "originality": {{"score": <1-10>, "justification": "text"}},
        "significance": {{"score": <1-10>, "justification": "text"}},
        "technical_quality": {{"score": <1-10>, "justification": "text"}},
        "clarity": {{"score": <1-10>, "justification": "text"}},
        "related_work": {{"score": <1-10>, "justification": "text"}},
        "results": {{"score": <1-10>, "justification": "text"}},
        "relevance": {{"score": <1-10>, "justification": "text"}},
        "ethics": {{"score": <1-10>, "justification": "text"}}
    }},
    "major_remarks": ["remark1", "remark2"],
    "minor_remarks": ["remark1", "remark2"],
    "concrete_suggestions": ["suggestion1", "suggestion2"],
    "recommendation": "accept/minor_revision/major_revision/reject",
    "summary": "overall summary of the review"
}}

Remember:
1. Your entire response must be a single JSON object
2. All property names must be in double quotes
3. All string values must be in double quotes
4. Use square brackets for arrays
5. Do not include any text outside the JSON object
6. Do not use trailing commas in objects or arrays""" 