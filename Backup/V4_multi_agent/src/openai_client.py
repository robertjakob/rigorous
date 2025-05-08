import os
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import json
import re

class OpenAIClient:
    """Client for interacting with OpenAI's API."""
    
    def __init__(self):
        """Initialize the OpenAI client."""
        # Load environment variables from .env file
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        print(f"\nLooking for .env file at: {env_path}")
        print(f"File exists: {os.path.exists(env_path)}")
        
        # Try to load the .env file
        if load_dotenv(env_path):
            print("Successfully loaded .env file")
        else:
            print("Failed to load .env file")
        
        # Get API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        else:
            # Mask most of the API key for security
            masked_key = f"{api_key[:7]}...{api_key[-4:]}"
            print(f"Found API key: {masked_key}")
        
        try:
            self.client = OpenAI(api_key=api_key)
            print("Successfully initialized OpenAI client")
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")
    
    def _extract_json_from_text(self, text: str) -> Dict[str, Any]:
        """Extract JSON from text that might contain other content."""
        # Find the first { and last } to extract the JSON object
        start = text.find('{')
        end = text.rfind('}')
        
        if start == -1 or end == -1:
            return {"error": "No JSON found in response"}
        
        json_str = text[start:end+1]
        
        # Clean up common JSON formatting issues
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)  # Remove trailing commas
        json_str = re.sub(r'\\n\s*', ' ', json_str)  # Remove newlines
        json_str = re.sub(r'\s+', ' ', json_str)  # Normalize whitespace
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            return {
                "error": "Failed to parse JSON",
                "details": str(e),
                "raw_text": text
            }
    
    def analyze_manuscript(self, content: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze manuscript content using OpenAI's API."""
        try:
            # Print request details for debugging
            print(f"\nMaking API call with model: {params.get('model', 'gpt-3.5-turbo')}")
            print(f"Task: {params.get('task', 'unknown')}")
            
            # Construct the messages for the chat completion
            messages = [
                {
                    "role": "system",
                    "content": (
                        f"You are an {params.get('role', 'expert scientific editor')}. "
                        "Your response must be a valid JSON object. "
                        "Do not include any text outside the JSON object. "
                        "Do not use markdown formatting. "
                        "Ensure all property names and string values are properly quoted."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"{params.get('prompt', '')}\n\n"
                        "Remember to return ONLY a valid JSON object with no additional text.\n\n"
                        f"Content:\n{content}"
                    )
                }
            ]
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=params.get('model', 'gpt-3.5-turbo'),
                messages=messages,
                temperature=0.3,
                response_format={"type": "json_object"}  # Request JSON response
            )
            
            # Extract and parse the response
            response_text = response.choices[0].message.content
            return self._extract_json_from_text(response_text)
            
        except Exception as e:
            return {
                "error": f"API call failed: {str(e)}",
                "details": {
                    "model": params.get('model', 'gpt-3.5-turbo'),
                    "role": params.get('role', 'expert scientific editor'),
                    "exception": str(e)
                }
            } 