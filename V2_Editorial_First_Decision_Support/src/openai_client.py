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
        load_dotenv()
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
                    {"role": "system", "content": "You are an expert manuscript reviewer. Analyze manuscripts against requirements. Be strict and thorough. Only mark requirements as met with clear evidence. Provide specific quotes and exact numbers when applicable."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000  # Limit response length
            )
            
            return self._parse_response(response.choices[0].message.content)
            
        except Exception as e:
            raise Exception(f"Failed to analyze manuscript: {str(e)}")
    
    def _create_analysis_prompt(self, manuscript_text: str, requirements: List[str]) -> str:
        """Create the prompt for the GPT model."""
        return f"""Analyze this manuscript against these requirements. For each requirement:
1. Mark as met ONLY with clear evidence from the text
2. For quantitative requirements (e.g., word count, DPI), provide exact numbers
3. For structural requirements (e.g., sections, formatting), quote specific examples
4. For missing requirements, mark as NOT MET and state "Requirement not found in manuscript"
5. Be consistent: if something is not found, it should be marked as NOT MET

Requirements:
{chr(10).join(f'- {req}' for req in requirements)}

Manuscript:
{manuscript_text}

Format response as JSON:
{{
    "requirements_analysis": [
        {{
            "requirement": "requirement text",
            "is_met": true/false,
            "evidence": "REQUIRED: For met requirements - quote the relevant text or provide exact numbers. For unmet requirements - state 'Requirement not found in manuscript'",
            "explanation": "Detailed explanation with specific references. For met requirements - explain what was found. For unmet requirements - explain what was missing."
        }}
    ],
    "desk_rejection_recommendation": {{
        "should_reject": true/false,
        "justification": "Detailed explanation with specific references to unmet requirements"
    }}
}}"""

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the GPT response into a structured format."""
        try:
            # Find the JSON part of the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[start_idx:end_idx]
            parsed_response = json.loads(json_str)
            
            # Ensure all required fields are present
            if "requirements_analysis" not in parsed_response:
                raise ValueError("Missing requirements_analysis in response")
                
            if "desk_rejection_recommendation" not in parsed_response:
                raise ValueError("Missing desk_rejection_recommendation in response")
                
            # Ensure each requirement has all required fields
            for req in parsed_response["requirements_analysis"]:
                if "requirement" not in req:
                    req["requirement"] = "Unknown requirement"
                if "is_met" not in req:
                    req["is_met"] = False
                if "evidence" not in req:
                    req["evidence"] = "No evidence provided"
                if "explanation" not in req:
                    req["explanation"] = "No explanation provided"
            
            # Ensure desk rejection recommendation has all required fields
            rejection = parsed_response["desk_rejection_recommendation"]
            if "should_reject" not in rejection:
                rejection["should_reject"] = False
            if "justification" not in rejection:
                rejection["justification"] = "No justification provided"
            
            return parsed_response
            
        except Exception as e:
            print(f"Warning: Failed to parse response as JSON: {str(e)}")
            print("Raw response:", response)
            # Return a default structure if parsing fails
            return {
                "requirements_analysis": [],
                "desk_rejection_recommendation": {
                    "should_reject": False,
                    "justification": "Failed to parse response"
                }
            } 