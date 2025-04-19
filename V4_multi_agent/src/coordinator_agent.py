from typing import Dict, List, Any
import json
from openai_client import OpenAIClient

class CoordinatorAgent:
    """Coordinator agent for synthesizing specialized reviews."""
    
    def __init__(self):
        self.client = OpenAIClient()
        self.paper_text = None  # Store paper text for use across methods
    
    def synthesize_reviews(self, specialized_reviews: Dict[str, Dict[str, Any]], paper_text: str) -> Dict[str, Any]:
        """Synthesize specialized reviews into a comprehensive report.
        
        Args:
            specialized_reviews (Dict[str, Dict[str, Any]]): Reviews from specialized agents
            paper_text (str): The text content of the paper
            
        Returns:
            Dict[str, Any]: Comprehensive review report
        """
        self.paper_text = paper_text  # Store paper text for use in other methods
        
        prompt = f"""Synthesize these specialized reviews into a comprehensive report.

Specialized Reviews:
{json.dumps(specialized_reviews, indent=2)}

Paper text:
{paper_text[:8000]}  # Limit text length to avoid token limits

Provide a comprehensive synthesis in the following JSON format:
{{
    "paper_overview": {{
        "domain": "Main domain of the paper",
        "key_contributions": ["List of key contributions"],
        "technical_areas": ["List of technical areas covered"]
    }},
    "specialized_reviews": {{
        "agent_id": {{
            "expertise": ["List of expertise areas"],
            "findings": "Summary of findings",
            "recommendations": ["List of recommendations"]
        }}
    }},
    "cross_domain_analysis": {{
        "interdependencies": ["List of interdependencies between domains"],
        "conflicts": ["List of conflicts between domains"],
        "synergies": ["List of synergies between domains"]
    }},
    "comprehensive_assessment": {{
        "overall_quality": 0,
        "key_strengths": ["List of key strengths"],
        "key_weaknesses": ["List of key weaknesses"],
        "critical_issues": ["List of critical issues"]
    }},
    "action_plan": {{
        "priority_actions": ["List of priority actions"],
        "timeline": "Estimated timeline for improvements",
        "resource_requirements": ["List of resource requirements"]
    }},
    "final_recommendation": {{
        "decision": "Accept/Minor Revision/Major Revision/Reject",
        "justification": "Detailed justification",
        "next_steps": ["List of next steps"]
    }}
}}

Ensure your response is valid JSON and includes all required fields."""

        try:
            response = self.client.analyze_manuscript(paper_text, {
                "role": "expert scientific editor synthesizing specialized reviews",
                "task": "synthesize reviews",
                "prompt": prompt
            })
            
            if "error" in response:
                raise Exception(f"Failed to synthesize reviews: {response['error']}")
            
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
                
            return response
            
        except Exception as e:
            print(f"Error synthesizing reviews: {e}")
            return {
                "error": "Failed to synthesize reviews",
                "details": str(e)
            }
    
    def generate_final_report(self, specialized_reviews: Dict[str, Dict[str, Any]], synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the final comprehensive report.
        
        Args:
            specialized_reviews (Dict[str, Dict[str, Any]]): Reviews from specialized agents
            synthesis (Dict[str, Any]): Synthesis of reviews
            
        Returns:
            Dict[str, Any]: Final comprehensive report
        """
        if not self.paper_text:
            raise ValueError("Paper text not available. Call synthesize_reviews first.")
            
        prompt = f"""Generate a final comprehensive report combining specialized reviews and synthesis.

Specialized Reviews:
{json.dumps(specialized_reviews, indent=2)}

Synthesis:
{json.dumps(synthesis, indent=2)}

Paper text:
{self.paper_text[:8000]}  # Limit text length to avoid token limits

Provide the final report in the following JSON format:
{{
    "executive_summary": {{
        "paper_overview": "Brief overview of the paper",
        "key_findings": ["List of key findings"],
        "recommendation": "Final recommendation"
    }},
    "detailed_reviews": {{
        "agent_id": {{
            "expertise": ["List of expertise areas"],
            "detailed_analysis": "Detailed analysis",
            "specific_recommendations": ["List of specific recommendations"]
        }}
    }},
    "cross_domain_analysis": {{
        "interdependencies": ["List of interdependencies"],
        "conflicts": ["List of conflicts"],
        "synergies": ["List of synergies"]
    }},
    "comprehensive_assessment": {{
        "overall_quality": 0,
        "key_strengths": ["List of key strengths"],
        "key_weaknesses": ["List of key weaknesses"],
        "critical_issues": ["List of critical issues"]
    }},
    "action_plan": {{
        "priority_actions": ["List of priority actions"],
        "timeline": "Estimated timeline",
        "resource_requirements": ["List of resource requirements"]
    }},
    "final_recommendation": {{
        "decision": "Accept/Minor Revision/Major Revision/Reject",
        "justification": "Detailed justification",
        "next_steps": ["List of next steps"]
    }}
}}

Ensure your response is valid JSON and includes all required fields."""

        try:
            response = self.client.analyze_manuscript(self.paper_text, {
                "role": "expert scientific editor generating final report",
                "task": "generate final report",
                "prompt": prompt
            })
            
            if "error" in response:
                raise Exception(f"Failed to generate final report: {response['error']}")
            
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
                
            return response
            
        except Exception as e:
            print(f"Error generating final report: {e}")
            return {
                "error": "Failed to generate final report",
                "details": str(e)
            } 