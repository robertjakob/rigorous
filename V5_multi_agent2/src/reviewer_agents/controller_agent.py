from typing import Dict, Any, List
import json
from src.core.base_agent import BaseReviewerAgent
from src.reviewer_agents.rigor.R1_originality_contribution_agent import OriginalityContributionAgent
from src.reviewer_agents.rigor.R2_impact_significance_agent import ImpactSignificanceAgent
from src.reviewer_agents.rigor.R3_ethics_compliance_agent import EthicsComplianceAgent
from src.reviewer_agents.rigor.R4_data_code_availability_agent import DataCodeAvailabilityAgent
from src.reviewer_agents.rigor.R5_statistical_rigor_agent import StatisticalRigorAgent
from src.reviewer_agents.rigor.R6_technical_accuracy_agent import TechnicalAccuracyAgent
from src.reviewer_agents.rigor.R7_consistency_agent import ConsistencyAgent
from src.reviewer_agents.writing.W1_language_style_agent import LanguageStyleAgent
from src.reviewer_agents.writing.W2_narrative_structure_agent import NarrativeStructureAgent
from src.reviewer_agents.writing.W3_clarity_conciseness_agent import ClarityConcisenessAgent
from src.reviewer_agents.writing.W4_terminology_consistency_agent import TerminologyConsistencyAgent

class ControllerAgent(BaseReviewerAgent):
    """Controller agent that orchestrates the review process."""
    
    def __init__(self, model: str = "gpt-3.5-turbo"):
        super().__init__(model=model)
        self.name = "Controller_Agent"
        self.category = "Controller"
        
        # Initialize all reviewer agents
        self.agents = {
            "R1": OriginalityContributionAgent(model=model),
            "R2": ImpactSignificanceAgent(model=model),
            "R3": EthicsComplianceAgent(model=model),
            "R4": DataCodeAvailabilityAgent(model=model),
            "R5": StatisticalRigorAgent(model=model),
            "R6": TechnicalAccuracyAgent(model=model),
            "R7": ConsistencyAgent(model=model),
            "W1": LanguageStyleAgent(model=model),
            "W2": NarrativeStructureAgent(model=model),
            "W3": ClarityConcisenessAgent(model=model),
            "W4": TerminologyConsistencyAgent(model=model)
        }
    
    def run_analysis(self, manuscript_text: str) -> Dict[str, Any]:
        """Run the complete manuscript analysis using all agents."""
        results = {}
        research_type = "research"  # Default research type
        
        # Run analysis with each agent
        for agent_id, agent in self.agents.items():
            try:
                if agent_id.startswith("R"):
                    # Rigor agents
                    if agent_id == "R1":
                        results[agent_id] = agent.analyze_originality_contribution(manuscript_text, research_type)
                    elif agent_id == "R2":
                        results[agent_id] = agent.analyze_impact_significance(manuscript_text, {"field": research_type})
                    elif agent_id == "R3":
                        results[agent_id] = agent.analyze_ethics_compliance(manuscript_text, research_type)
                    elif agent_id == "R4":
                        results[agent_id] = agent.analyze_data_code_availability(manuscript_text, research_type)
                    elif agent_id == "R5":
                        results[agent_id] = agent.analyze_statistical_rigor(manuscript_text, research_type)
                    elif agent_id == "R6":
                        results[agent_id] = agent.analyze_technical_accuracy(manuscript_text, research_type)
                    elif agent_id == "R7":
                        results[agent_id] = agent.analyze_consistency(manuscript_text, research_type)
                else:
                    # Writing agents
                    if agent_id == "W1":
                        results[agent_id] = agent.analyze_language_style(manuscript_text, research_type)
                    elif agent_id == "W2":
                        results[agent_id] = agent.analyze_narrative_structure(manuscript_text, research_type)
                    elif agent_id == "W3":
                        results[agent_id] = agent.analyze_clarity_conciseness(manuscript_text, research_type)
                    elif agent_id == "W4":
                        results[agent_id] = agent.analyze_terminology_consistency(manuscript_text, research_type)
            except Exception as e:
                print(f"Error in {agent_id}: {str(e)}")
                results[agent_id] = {
                    "error": True,
                    "message": f"Error in analysis: {str(e)}",
                    "score": 0,
                    "critical_remarks": [],
                    "improvement_suggestions": [],
                    "detailed_feedback": {},
                    "summary": f"Analysis failed due to error: {str(e)}"
                }
        
        return results 