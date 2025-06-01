from typing import Dict, Any, List
import json
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from .config import DEFAULT_MODEL
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class BaseReviewerAgent:
    """Base class for all reviewer agents."""
    
    def __init__(self, model=DEFAULT_MODEL):
        """
        Initialize the base reviewer agent.
        
        Args:
            model (str): The language model to use
            name (str): Name of the agent
            category (str): Category of the agent (scientific_rigor)
        """
        self.name = self.__class__.__name__
        self.category = "Unknown"
        self.model = model
        
        # Initialize OpenAI client with API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(f"OPENAI_API_KEY environment variable not set. Please check {env_path}")
        
        # Print debug info
        print(f"{self.name} using model: {model}", f"API key found: {'Yes' if api_key else 'No'}")
        
        self.client = OpenAI(api_key=api_key)
        
    def llm(self, prompt: str) -> str:
        """Call OpenAI API with the given prompt."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert academic reviewer. Provide detailed analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error calling language model: {str(e)}")
    
    def analyze_section(self, text: str, section_name: str) -> Dict[str, Any]:
        """Analyze a specific section of the manuscript.
        
        Args:
            text (str): Text content to analyze
            section_name (str): Name of the section being analyzed
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        prompt = f"""As a {self.name}, analyze the following {section_name} section:

{text}

Provide your analysis in the following JSON format:
{{
    "score": <1-5>,
    "remarks": [
        "List of specific issues, questions, or observations"
    ],
    "concrete_suggestions": [
        "List of actionable steps for improvement"
    ],
    "automated_improvements": [
        "List of AI-generated improvements"
    ]
}}

Ensure your response is valid JSON and includes all required fields."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a {self.name} reviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                analysis = json.loads(content[start_idx:end_idx])
            else:
                raise ValueError("No JSON found in response")
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing section: {e}")
            return {"score": 0, "remarks": [], "concrete_suggestions": [], "automated_improvements": []} 