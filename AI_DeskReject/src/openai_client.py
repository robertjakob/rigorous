import os
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
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        self.client = OpenAI(api_key=self.api_key)
        
    def check_requirements(self, manuscript_text: str, requirements: List[str]) -> Dict[str, Any]:
        """
        Check if the manuscript meets the given requirements using GPT-4.
        
        Args:
            manuscript_text (str): The full text of the manuscript
            requirements (List[str]): List of editorial requirements to check
            
        Returns:
            Dict[str, Any]: Analysis results including requirement status and evidence
        """
        prompt = self._create_analysis_prompt(manuscript_text, requirements)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # Can be changed to gpt-3.5-turbo if needed
                messages=[
                    {"role": "system", "content": "You are an expert manuscript reviewer. "
                     "Analyze the manuscript against the given requirements and provide detailed feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return self._parse_response(response.choices[0].message.content)
            
        except Exception as e:
            raise Exception(f"Failed to analyze manuscript: {str(e)}")
    
    def _create_analysis_prompt(self, manuscript_text: str, requirements: List[str]) -> str:
        """Create the prompt for the GPT model."""
        return f"""Please analyze the following manuscript against these editorial requirements:

Requirements:
{chr(10).join(f'- {req}' for req in requirements)}

Manuscript:
{manuscript_text}

For each requirement, please provide:
1. Whether it is met (YES/NO)
2. If not met, provide the specific passage from the manuscript that shows this
3. Brief explanation of your assessment

Finally, provide a recommendation on whether the manuscript should be desk rejected (YES/NO) with justification.

Format your response as JSON with the following structure:
{{
    "requirements_analysis": [
        {{
            "requirement": "requirement text",
            "is_met": true/false,
            "evidence": "relevant passage if not met",
            "explanation": "brief explanation"
        }}
    ],
    "desk_rejection_recommendation": {{
        "should_reject": true/false,
        "justification": "explanation"
    }}
}}"""

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the GPT response into a structured format."""
        # In a real implementation, this would parse the JSON response
        # For now, we'll return a placeholder structure
        return {
            "requirements_analysis": [],
            "desk_rejection_recommendation": {
                "should_reject": False,
                "justification": "Placeholder"
            }
        } 