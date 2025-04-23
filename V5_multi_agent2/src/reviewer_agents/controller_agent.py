from typing import Dict, Any, List
import json
import os
from datetime import datetime
from ..core.base_agent import BaseReviewerAgent
from src.core.report_template import ReportTemplate
from .rigor.R1_originality_contribution_agent import OriginalityContributionAgent
from .rigor.R2_impact_significance_agent import ImpactSignificanceAgent
from .rigor.R3_ethics_compliance_agent import EthicsComplianceAgent
from .rigor.R4_data_code_availability_agent import DataCodeAvailabilityAgent
from .rigor.R5_statistical_rigor_agent import StatisticalRigorAgent
from .rigor.R6_technical_accuracy_agent import TechnicalAccuracyAgent
from .rigor.R7_consistency_agent import ConsistencyAgent
from .writing.W1_language_style_agent import LanguageStyleAgent
from .writing.W2_narrative_structure_agent import NarrativeStructureAgent
from .writing.W3_clarity_conciseness_agent import ClarityConcisenessAgent
from .writing.W4_terminology_consistency_agent import TerminologyConsistencyAgent
from .writing.W5_inclusive_language_agent import InclusiveLanguageAgent
from .writing.W6_citation_formatting_agent import CitationFormattingAgent
from .writing.W7_target_audience_agent import TargetAudienceAlignmentAgent
from .writing.W8_visual_presentation_agent import VisualPresentationAgentW8

class ControllerAgent:
    """Controller agent that coordinates all reviewer agents."""
    
    def __init__(self, model="gpt-4"):
        self.model = model
        self.agents = {
            'R1': OriginalityContributionAgent(model),
            'R2': ImpactSignificanceAgent(model),
            'R3': EthicsComplianceAgent(model),
            'R4': DataCodeAvailabilityAgent(model),
            'R5': StatisticalRigorAgent(model),
            'R6': TechnicalAccuracyAgent(model),
            'R7': ConsistencyAgent(model),
            'W1': LanguageStyleAgent(model),
            'W2': NarrativeStructureAgent(model),
            'W3': ClarityConcisenessAgent(model),
            'W4': TerminologyConsistencyAgent(model),
            'W5': InclusiveLanguageAgent(model),
            'W6': CitationFormattingAgent(model),
            'W7': TargetAudienceAlignmentAgent(model),
            'W8': VisualPresentationAgentW8(model)
        }
    
    def run_analysis(self, text: str, metadata: Dict[str, str] = None, 
                    images: List[Dict[str, Any]] = None, 
                    tables: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run analysis using all agents.
        
        Args:
            text (str): The manuscript text
            metadata (Dict[str, str], optional): Manuscript metadata
            images (List[Dict[str, Any]], optional): Extracted images with metadata
            tables (List[Dict[str, Any]], optional): Extracted tables with metadata
            
        Returns:
            Dict[str, Any]: Combined results from all agents
        """
        results = {}
        research_type = self._determine_research_type(text)
        
        # Run each agent's analysis
        for agent_id, agent in self.agents.items():
            try:
                if agent_id == 'W8':  # Visual Presentation Agent
                    results[agent_id] = agent.analyze_visual_presentation(
                        text=text,
                        research_type=research_type,
                        images=images,
                        tables=tables
                    )
                else:
                    # Call the appropriate analysis method for each agent
                    if isinstance(agent, OriginalityContributionAgent):
                        results[agent_id] = agent.analyze_originality_contribution(text, research_type)
                    elif isinstance(agent, ImpactSignificanceAgent):
                        results[agent_id] = agent.analyze_impact_significance(text, research_type)
                    elif isinstance(agent, EthicsComplianceAgent):
                        results[agent_id] = agent.analyze_ethics_compliance(text, research_type)
                    elif isinstance(agent, DataCodeAvailabilityAgent):
                        results[agent_id] = agent.analyze_data_code_availability(text, research_type)
                    elif isinstance(agent, StatisticalRigorAgent):
                        results[agent_id] = agent.analyze_statistical_rigor(text, research_type)
                    elif isinstance(agent, TechnicalAccuracyAgent):
                        results[agent_id] = agent.analyze_technical_accuracy(text, research_type)
                    elif isinstance(agent, ConsistencyAgent):
                        results[agent_id] = agent.analyze_consistency(text, research_type)
                    elif isinstance(agent, LanguageStyleAgent):
                        results[agent_id] = agent.analyze_language_style(text, research_type)
                    elif isinstance(agent, NarrativeStructureAgent):
                        results[agent_id] = agent.analyze_narrative_structure(text, research_type)
                    elif isinstance(agent, ClarityConcisenessAgent):
                        results[agent_id] = agent.analyze_clarity_conciseness(text, research_type)
                    elif isinstance(agent, TerminologyConsistencyAgent):
                        results[agent_id] = agent.analyze_terminology_consistency(text, research_type)
                    elif isinstance(agent, InclusiveLanguageAgent):
                        results[agent_id] = agent.analyze_inclusive_language(text, research_type)
                    elif isinstance(agent, CitationFormattingAgent):
                        results[agent_id] = agent.analyze_citation_formatting(text, research_type)
                    elif isinstance(agent, TargetAudienceAlignmentAgent):
                        results[agent_id] = agent.analyze_target_audience_alignment(text, research_type)
            except Exception as e:
                print(f"Error in {agent_id}: {str(e)}")
                results[agent_id] = self._generate_error_report(str(e))
        
        return results
    
    def _determine_research_type(self, text: str) -> str:
        """Determine the type of research paper."""
        # Simple heuristic based on keywords
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['experiment', 'methodology', 'data collection']):
            return 'experimental'
        elif any(word in text_lower for word in ['review', 'literature', 'meta-analysis']):
            return 'review'
        elif any(word in text_lower for word in ['theory', 'framework', 'model']):
            return 'theoretical'
        else:
            return 'general'
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generate a structured error report."""
        return {
            'error': True,
            'error_message': error_message,
            'score': 0,
            'critical_remarks': [],
            'improvement_suggestions': [],
            'detailed_feedback': {},
            'summary': f"Error in analysis: {error_message}"
        }

    def _generate_error_report(self, agent_id: str, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report for an agent."""
        return {
            "error": True,
            "message": f"Error in analysis: {error_message}",
            "score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {},
            "summary": f"Analysis failed due to error: {error_message}"
        } 