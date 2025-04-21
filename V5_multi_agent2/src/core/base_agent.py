from typing import Dict, Any, List
import json
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from .config import REPORT_TEMPLATE, DEFAULT_MODEL

# Get the absolute path to the .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')

# Load environment variables from the correct path
load_dotenv(dotenv_path=env_path)

class BaseReviewerAgent:
    """Base class for all reviewer agents."""
    
    def __init__(self, model: str = "gpt-4"):
        """
        Initialize the base reviewer agent.
        
        Args:
            model (str): The language model to use
            name (str): Name of the agent
            category (str): Category of the agent (scientific_rigor)
        """
        self.model = model
        self.name = "Base_Reviewer_Agent"
        self.category = "Scientific Rigor"
        
        # Initialize OpenAI client with API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(f"OPENAI_API_KEY environment variable not set. Please check {env_path}")
        
        # Print debug info
        print(f"Using model: {model}")
        print(f"API key found: {'Yes' if api_key else 'No'}")
        
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
    
    def create_report_template(self) -> Dict[str, Any]:
        """Create a new report template."""
        template = REPORT_TEMPLATE.copy()
        template["metadata"].update({
            "agent_name": self.name,
            "category": self.category,
            "model_used": self.model,
            "timestamp": datetime.now().isoformat()
        })
        return template
    
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
    "score": <1-10>,
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
            
            # Create report with analysis
            report = self.create_report_template()
            report.update(analysis)
            
            return report
            
        except Exception as e:
            print(f"Error analyzing section: {e}")
            return self.create_report_template()
    
    def save_report(self, report: Dict[str, Any], output_path: str) -> None:
        """Save the report to a file.
        
        Args:
            report (Dict[str, Any]): Report to save
            output_path (str): Path to save the report
        """
        try:
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
        except Exception as e:
            print(f"Error saving report: {e}")
    
    def load_report(self, input_path: str) -> Dict[str, Any]:
        """Load a report from a file.
        
        Args:
            input_path (str): Path to load the report from
            
        Returns:
            Dict[str, Any]: Loaded report
        """
        try:
            with open(input_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading report: {e}")
            return self.create_report_template() 