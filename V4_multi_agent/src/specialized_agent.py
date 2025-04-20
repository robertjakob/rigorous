from typing import Dict, List, Any
import json
from openai_client import OpenAIClient

class SpecializedReviewAgent:
    """Specialized review agent for domain-specific paper evaluation."""
    
    def __init__(self, agent_config: Dict[str, Any]):
        """Initialize the specialized review agent.
        
        Args:
            agent_config (Dict[str, Any]): Agent configuration including role and expertise
        """
        self.client = OpenAIClient()
        self.role = agent_config["role"]
        self.expertise = agent_config["expertise"]
        self.focus_areas = agent_config["focus_areas"]
        self.review_criteria = agent_config["review_criteria"]
        self.criteria_description = agent_config.get("criteria_description", "Review criteria for this domain")
        self.required_background = agent_config["required_background"]
    
    def _create_review_template(self) -> Dict[str, Any]:
        """Create the review template based on agent's expertise.
        
        Returns:
            Dict[str, Any]: Review template structure
        """
        return {
            "agent_info": {
                "role": self.role,
                "expertise": self.expertise,
                "focus_areas": self.focus_areas
            },
            "technical_review": {
                "methodology_assessment": "...",
                "technical_quality": "...",
                "innovation_analysis": "...",
                "comparative_analysis": "..."
            },
            "domain_specific_analysis": {
                "strengths": [],
                "weaknesses": [],
                "improvements": [],
                "technical_recommendations": []
            },
            "score": {
                "value": 0,
                "justification": "...",
                "comparative_context": "..."
            },
            "detailed_feedback": {
                "critical_issues": [],
                "suggestions": [],
                "references": []
            }
        }
    
    def perform_review(self, paper_text: str) -> Dict[str, Any]:
        """Perform a specialized review of the paper.
        
        Args:
            paper_text (str): The text content of the paper
            
        Returns:
            Dict[str, Any]: Detailed review results
        """
        prompt = f"""You are an expert {self.role} with deep knowledge in {', '.join(self.expertise)}.
Review this paper focusing on your areas of expertise and the following criteria:

Focus Areas:
{json.dumps(self.focus_areas, indent=2)}

Review Criteria Description:
{self.criteria_description}

Specific Review Criteria:
{json.dumps(self.review_criteria, indent=2)}

Required Background Knowledge:
{json.dumps(self.required_background, indent=2)}

Paper text:
{paper_text[:8000]}  # Limit text length to avoid token limits

Provide your review in the following JSON format:
{
    "strengths": [
        {
            "point": "Specific strength identified",
            "location": "Section/paragraph where this strength appears",
            "explanation": "Detailed explanation of why this is a strength",
            "impact": "How this strength contributes to the paper's quality"
        }
    ],
    "weaknesses": [
        {
            "point": "Specific weakness identified",
            "location": "Section/paragraph where this weakness appears",
            "explanation": "Detailed explanation of why this is a weakness",
            "impact": "How this weakness affects the paper's quality"
        }
    ],
    "improvements": [
        {
            "area": "Specific area needing improvement",
            "current_state": "Description of the current state",
            "suggestion": "Detailed, actionable suggestion for improvement",
            "example": "Specific example or reference to support the suggestion",
            "expected_impact": "How this improvement would enhance the paper"
        }
    ],
    "summary": {
        "overall_assessment": "Overall assessment of the paper from your expertise perspective",
        "key_points": ["Key points that need attention"],
        "priority_improvements": ["Most important improvements to address first"]
    }
}

Ensure your response is valid JSON and includes all required fields. Provide specific, detailed feedback with concrete examples and actionable suggestions."""

        try:
            response = self.client.analyze_manuscript(paper_text, {
                "role": f"expert {self.role}",
                "expertise": self.expertise,
                "focus_areas": self.focus_areas,
                "review_criteria": self.review_criteria,
                "criteria_description": self.criteria_description,
                "required_background": self.required_background,
                "prompt": prompt
            })
            
            if "error" in response:
                raise Exception(f"Failed to perform review: {response['error']}")
            
            # Extract JSON from response if needed
            if isinstance(response, str):
                try:
                    start_idx = response.find('{')
                    end_idx = response.rfind('}') + 1
                    if start_idx >= 0 and end_idx > start_idx:
                        response = json.loads(response[start_idx:end_idx])
                    else:
                        raise ValueError("No JSON found in response")
                except json.JSONDecodeError as e:
                    raise Exception(f"Failed to parse JSON response: {str(e)}")
                
            # Add agent info to response
            response["agent_info"] = {
                "role": self.role,
                "expertise": self.expertise,
                "focus_areas": self.focus_areas
            }
                
            return response
            
        except Exception as e:
            print(f"Error performing review: {e}")
            return {
                "error": "Failed to perform review",
                "details": str(e),
                "agent_info": {
                    "role": self.role,
                    "expertise": self.expertise,
                    "focus_areas": self.focus_areas
                }
            }
    
    def provide_detailed_feedback(self, paper_text: str, initial_review: Dict[str, Any]) -> Dict[str, Any]:
        """Provide detailed feedback based on initial review.
        
        Args:
            paper_text (str): The text content of the paper
            initial_review (Dict[str, Any]): Initial review results
            
        Returns:
            Dict[str, Any]: Detailed feedback
        """
        prompt = f"""Based on your initial review, provide detailed feedback focusing on your expertise areas.

Initial Review:
{json.dumps(initial_review, indent=2)}

Review Criteria Description:
{self.criteria_description}

Specific Review Criteria:
{json.dumps(self.review_criteria, indent=2)}

Paper text:
{paper_text[:8000]}  # Limit text length to avoid token limits

Provide detailed feedback in the following JSON format:
{{
    "detailed_analysis": {{
        "technical_details": "In-depth technical analysis",
        "methodology_issues": "Detailed methodology issues",
        "improvement_suggestions": "Specific improvement suggestions"
    }},
    "specific_recommendations": [
        {{
            "area": "Specific area",
            "issue": "Detailed issue description",
            "suggestion": "Specific suggestion",
            "expected_impact": "Expected impact of change"
        }}
    ],
    "references_and_examples": [
        {{
            "reference": "Relevant reference",
            "application": "How it applies to this paper",
            "suggestion": "How to incorporate it"
        }}
    ]
}}

Ensure your response is valid JSON and includes all required fields."""

        try:
            response = self.client.analyze_manuscript(paper_text, {
                "role": f"expert {self.role} providing detailed feedback",
                "expertise": self.expertise,
                "focus_areas": self.focus_areas,
                "review_criteria": self.review_criteria,
                "criteria_description": self.criteria_description,
                "initial_review": initial_review,
                "prompt": prompt
            })
            
            if "error" in response:
                raise Exception(f"Failed to provide detailed feedback: {response['error']}")
            
            # Extract JSON from response if needed
            if isinstance(response, str):
                try:
                    start_idx = response.find('{')
                    end_idx = response.rfind('}') + 1
                    if start_idx >= 0 and end_idx > start_idx:
                        response = json.loads(response[start_idx:end_idx])
                    else:
                        raise ValueError("No JSON found in response")
                except json.JSONDecodeError as e:
                    raise Exception(f"Failed to parse JSON response: {str(e)}")
                
            # Add agent info to response
            response["agent_info"] = {
                "role": self.role,
                "expertise": self.expertise,
                "focus_areas": self.focus_areas
            }
                
            return response
            
        except Exception as e:
            print(f"Error providing detailed feedback: {e}")
            return {
                "error": "Failed to provide detailed feedback",
                "details": str(e),
                "agent_info": {
                    "role": self.role,
                    "expertise": self.expertise,
                    "focus_areas": self.focus_areas
                }
            } 