import json
import os
from typing import Dict, Any, List

class ReviewCriteriaParser:
    """Parser for review criteria from a text file."""
    
    def __init__(self):
        """Initialize the review criteria parser."""
        pass
    
    def _load_criteria(self, criteria_path: str) -> dict:
        """Load and parse the criteria file.
        
        Args:
            criteria_path (str): Path to the criteria file
            
        Returns:
            dict: Parsed criteria
        """
        if not os.path.exists(criteria_path):
            raise FileNotFoundError(f"Criteria file not found: {criteria_path}")
            
        with open(criteria_path, 'r') as f:
            content = f.read()
            
        # Initialize criteria sections
        criteria = {
            "general": {
                "description": "General review criteria applicable to all manuscripts",
                "criteria": []
            },
            "technical": {
                "description": "Technical review criteria for methodology and implementation",
                "criteria": []
            },
            "domain": {
                "description": "Domain-specific review criteria",
                "criteria": []
            },
            "impact": {
                "description": "Impact and significance review criteria",
                "criteria": []
            },
            "ethics": {
                "description": "Ethical considerations review criteria",
                "criteria": []
            }
        }
        
        # Split content into sections
        sections = content.split('\n\n')
        
        for section in sections:
            lines = section.strip().split('\n')
            if not lines:
                continue
                
            # Identify section header
            header = lines[0].strip()
            
            # Map header to criteria section
            if "technical" in header.lower() or "methodology" in header.lower():
                target = "technical"
            elif "domain" in header.lower() or "field" in header.lower():
                target = "domain"
            elif "impact" in header.lower() or "significance" in header.lower():
                target = "impact"
            elif "ethic" in header.lower():
                target = "ethics"
            else:
                target = "general"
                
            # Add criteria points to the appropriate section
            for line in lines[1:]:
                line = line.strip()
                if line and not line.startswith('#'):
                    criteria[target]["criteria"].append(line)
                    
        return criteria
    
    def get_criteria(self, criteria_path: str) -> dict:
        """Get the parsed criteria.
        
        Args:
            criteria_path (str): Path to the criteria file
            
        Returns:
            dict: Parsed criteria
        """
        return self._load_criteria(criteria_path)
    
    def get_agent_criteria(self, criteria_path: str, agent_role: str) -> dict:
        """Get criteria specific to an agent's role.
        
        Args:
            criteria_path (str): Path to the criteria file
            agent_role (str): The role of the agent
            
        Returns:
            dict: Criteria specific to the agent's role
        """
        all_criteria = self._load_criteria(criteria_path)
        
        # Map agent roles to criteria sections
        role_to_section = {
            "methodology": "technical",
            "technical": "technical",
            "domain": "domain",
            "impact": "impact",
            "ethics": "ethics"
        }
        
        # Determine which section to use based on the agent's role
        section = "general"  # Default to general criteria
        
        for role_key, criteria_section in role_to_section.items():
            if role_key in agent_role.lower():
                section = criteria_section
                break
                
        # Return the appropriate criteria
        return {
            "role": agent_role,
            "criteria": all_criteria[section]["criteria"],
            "description": all_criteria[section]["description"]
        }
    
    def validate_criteria(self, criteria_path: str) -> bool:
        """Validate the structure of the criteria file.
        
        Args:
            criteria_path (str): Path to the criteria file
            
        Returns:
            bool: True if the criteria file is valid, False otherwise
        """
        try:
            criteria = self._load_criteria(criteria_path)
            
            # Check that all required sections are present
            required_sections = ["general", "technical", "domain", "impact", "ethics"]
            for section in required_sections:
                if section not in criteria:
                    return False
                    
            # Check that each section has criteria
            for section in criteria.values():
                if not section["criteria"]:
                    return False
                    
            return True
            
        except Exception:
            return False 