import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

class OpenAIClient:
    """A class to handle interactions with the OpenAI API."""
    
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
        
    def check_requirements(self, manuscript_text: str, requirements: List[str]) -> Dict[str, Any]:
        """
        Check if the manuscript meets the given requirements using GPT-3.5-turbo.
        
        Args:
            manuscript_text (str): The full text of the manuscript
            requirements (List[str]): List of editorial requirements to check
            
        Returns:
            Dict[str, Any]: Analysis results including requirement status and evidence
        """
        # Truncate manuscript text to first 4000 words to reduce token usage
        words = manuscript_text.split()
        truncated_text = ' '.join(words[:4000]) if len(words) > 4000 else manuscript_text
        
        prompt = self._create_analysis_prompt(truncated_text, requirements)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using standard model instead of 16k for cost efficiency
                messages=[
                    {"role": "system", "content": "You are an expert manuscript reviewer. Analyze manuscripts against requirements. Be strict and thorough. Only mark requirements as met with clear evidence. Provide specific quotes and exact numbers when applicable. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000  # Limit response length
            )
            
            response_content = response.choices[0].message.content
            print(f"OpenAI Response: {response_content}")  # Debug print
            
            return self._parse_response(response_content)
            
        except Exception as e:
            raise Exception(f"Failed to analyze manuscript: {str(e)}")
    
    def _create_analysis_prompt(self, manuscript_text: str, requirements: List[str]) -> str:
        """
        Create a prompt for the requirements analysis.
        
        Args:
            manuscript_text (str): The manuscript text
            requirements (List[str]): List of requirements to check
            
        Returns:
            str: Formatted prompt for the OpenAI API
        """
        requirements_section = "\n".join([f"{i+1}. {req}" for i, req in enumerate(requirements)])
        
        return f"""Please analyze the following manuscript against these requirements:

{requirements_section}

For each requirement:
1. Determine if it is met (YES/NO)
2. Provide evidence from the text
3. Give a brief explanation

Manuscript text:
{manuscript_text}

Please format your response as a JSON object with the following structure:
{{
    "requirements_analysis": [
        {{
            "requirement": "<requirement text>",
            "is_met": <true/false>,
            "evidence": "<specific evidence from the text>",
            "explanation": "<brief explanation>"
        }}
    ],
    "desk_rejection_recommendation": {{
        "should_reject": <true/false>,
        "justification": "<detailed explanation of the recommendation>"
    }}
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
            # Remove code block markers if present
            cleaned_response = response.strip()
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.split("\n", 1)[1]  # Remove first line
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response.rsplit("\n", 1)[0]  # Remove last line
            if cleaned_response.startswith("json"):
                cleaned_response = cleaned_response.split("\n", 1)[1]  # Remove "json" line
            
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {str(e)}")  # Debug print
            print(f"Response content: {response}")  # Debug print
            raise Exception("Failed to parse OpenAI response as JSON") 