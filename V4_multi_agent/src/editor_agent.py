from typing import Dict, List, Any
import json
from openai_client import OpenAIClient

class EditorAgent:
    """Editor agent that analyzes papers and creates specialized review teams."""
    
    def __init__(self):
        self.client = OpenAIClient()
        
        # Define core reviewer agents that are always included
        self.core_reviewers = [
            {
                "id": "language_reviewer",
                "role": "Language and Clarity Expert",
                "expertise": ["Scientific Writing", "Grammar", "Clarity", "Style"],
                "focus_areas": ["Writing Quality", "Clarity of Expression", "Grammar and Style", "Figure and Table Clarity"],
                "review_criteria": ["Clarity of writing", "Grammar and style", "Figure and table clarity", "Overall presentation"],
                "required_background": ["Scientific writing standards", "Publication guidelines", "Visual communication"]
            },
            {
                "id": "methodology_reviewer",
                "role": "Methodology Expert",
                "expertise": ["Research Methods", "Statistical Analysis", "Experimental Design", "Reproducibility"],
                "focus_areas": ["Research Design", "Data Collection", "Analysis Methods", "Reproducibility"],
                "review_criteria": ["Methodological soundness", "Statistical rigor", "Experimental design", "Reproducibility"],
                "required_background": ["Research methodology", "Statistical analysis", "Experimental design principles"]
            },
            {
                "id": "ethics_reviewer",
                "role": "Ethics and Compliance Expert",
                "expertise": ["Research Ethics", "Data Privacy", "Informed Consent", "Conflict of Interest"],
                "focus_areas": ["Ethical Considerations", "Data Privacy", "Informed Consent", "Conflict of Interest"],
                "review_criteria": ["Ethical compliance", "Data privacy", "Informed consent", "Conflict of interest"],
                "required_background": ["Research ethics", "Data protection regulations", "Publication ethics"]
            }
        ]
    
    def analyze_paper(self, paper_text: str) -> Dict[str, Any]:
        """Analyze the paper to determine required expertise and review criteria.
        
        Args:
            paper_text (str): The text content of the paper
            
        Returns:
            Dict[str, Any]: Analysis of paper requirements and review team structure
        """
        prompt = f"""You are an expert scientific editor. Analyze this paper and determine:
1. The main domain and subdomains
2. Technical areas requiring expertise
3. Specialized knowledge requirements
4. Required review team composition

Paper text:
{paper_text[:8000]}  # Limit text length to avoid token limits

Provide your analysis in the following JSON format:
{{
    "paper_analysis": {{
        "main_domain": "Primary field of study",
        "subdomains": ["List of subdomains"],
        "technical_areas": ["List of technical areas"],
        "specialized_requirements": ["List of specialized knowledge needed"]
    }},
    "review_team": {{
        "required_expertise": [
            {{
                "domain": "Specific domain",
                "expertise_areas": ["List of required expertise"],
                "focus_areas": ["List of areas to focus on"],
                "review_criteria": ["List of specific criteria"]
            }}
        ]
    }}
}}

Ensure your response is valid JSON and includes all required fields."""

        try:
            response = self.client.analyze_manuscript(paper_text, {
                "role": "expert scientific editor",
                "task": "analyze paper requirements",
                "prompt": prompt
            })
            
            if "error" in response:
                raise Exception(f"Failed to analyze paper: {response['error']}")
            
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
            print(f"Error analyzing paper: {e}")
            return {
                "error": "Failed to analyze paper",
                "details": str(e)
            }
    
    def create_review_team(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create a specialized review team based on paper analysis.
        
        Args:
            analysis (Dict[str, Any]): Paper analysis from analyze_paper
            
        Returns:
            Dict[str, Any]: Review team configuration
        """
        prompt = f"""Based on this paper analysis, create a specialized review team with specific expertise and focus areas.

Analysis:
{json.dumps(analysis, indent=2)}

Provide the review team configuration in the following JSON format:
{{
    "review_team": {{
        "agents": [
            {{
                "id": "unique_agent_id",
                "role": "Specific role (e.g., Computer Vision Expert)",
                "expertise": ["List of expertise areas"],
                "focus_areas": ["List of focus areas"],
                "review_criteria": ["List of specific criteria"],
                "required_background": ["List of required background knowledge"]
            }}
        ],
        "review_process": {{
            "sequence": ["Order of review steps"],
            "dependencies": ["Review dependencies"],
            "coordination_points": ["Points where agents need to coordinate"]
        }}
    }}
}}

Ensure your response is valid JSON and includes all required fields."""

        try:
            response = self.client.analyze_manuscript("", {
                "role": "expert scientific editor",
                "task": "create review team",
                "analysis": analysis,
                "prompt": prompt
            })
            
            if "error" in response:
                raise Exception(f"Failed to create review team: {response['error']}")
            
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
            print(f"Error creating review team: {e}")
            return {
                "error": "Failed to create review team",
                "details": str(e)
            }
    
    def generate_review_plan(self, paper_text: str) -> Dict[str, Any]:
        """Generate a complete review plan for a paper.
        
        Args:
            paper_text (str): The text content of the paper
            
        Returns:
            Dict[str, Any]: Complete review plan including team and process
        """
        try:
            # Analyze paper requirements
            analysis = self.analyze_paper(paper_text)
            if "error" in analysis:
                raise Exception(f"Failed to analyze paper: {analysis['error']}")
            
            # Create review team
            team_config = self.create_review_team(analysis)
            if "error" in team_config:
                raise Exception(f"Failed to create review team: {team_config['error']}")
            
            # Add core reviewers to the team
            domain_specific_agents = team_config.get("review_team", {}).get("agents", [])
            all_agents = self.core_reviewers.copy()
            
            # Add domain-specific agents, ensuring no duplicate IDs
            for agent in domain_specific_agents:
                if not any(core_agent["id"] == agent["id"] for core_agent in all_agents):
                    all_agents.append(agent)
            
            # Create the complete review plan
            review_plan = {
                "paper_analysis": analysis.get("paper_analysis", {}),
                "review_team": {
                    "agents": all_agents,
                    "review_process": team_config.get("review_team", {}).get("review_process", {
                        "sequence": [
                            "Initial paper analysis",
                            "Core reviews (language, methodology, ethics)",
                            "Domain-specific reviews",
                            "Cross-domain analysis",
                            "Final synthesis"
                        ],
                        "dependencies": [],
                        "coordination_points": []
                    })
                }
            }
            
            return review_plan
            
        except Exception as e:
            print(f"Error generating review plan: {e}")
            return {
                "error": "Failed to generate review plan",
                "details": str(e)
            } 