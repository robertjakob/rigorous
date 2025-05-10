from typing import Dict, Any, List
import json
import os
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ..core.base_agent import BaseReviewerAgent

# Section agents
from .section.S1_title_keywords_agent import TitleKeywordsAgentS1
from .section.S2_abstract_agent import AbstractAgentS2
from .section.S3_introduction_agent import IntroductionAgentS3
from .section.S4_literature_review_agent import LiteratureReviewAgentS4
from .section.S5_methodology_agent import MethodologyAgentS5
from .section.S6_results_agent import ResultsAgentS6
from .section.S7_discussion_agent import DiscussionAgentS7
from .section.S8_conclusion_agent import ConclusionAgentS8
from .section.S9_references_agent import ReferencesAgentS9
from .section.S10_supplementary_materials_agent import SupplementaryMaterialsAgentS10

# Rigor agents
from .rigor.R1_originality_contribution_agent import OriginalityContributionAgent
from .rigor.R2_impact_significance_agent import ImpactSignificanceAgent
from .rigor.R3_ethics_compliance_agent import EthicsComplianceAgent
from .rigor.R4_data_code_availability_agent import DataCodeAvailabilityAgent
from .rigor.R5_statistical_rigor_agent import StatisticalRigorAgent
from .rigor.R6_technical_accuracy_agent import TechnicalAccuracyAgent
from .rigor.R7_consistency_agent import ConsistencyAgent

# Writing agents
from .writing.W1_language_style_agent import LanguageStyleAgent
from .writing.W2_narrative_structure_agent import NarrativeStructureAgent
from .writing.W3_clarity_conciseness_agent import ClarityConcisenessAgent
from .writing.W4_terminology_consistency_agent import TerminologyConsistencyAgent
from .writing.W5_inclusive_language_agent import InclusiveLanguageAgent
from .writing.W6_citation_formatting_agent import CitationFormattingAgent
from .writing.W7_target_audience_agent import TargetAudienceAlignmentAgent

class ControllerAgent:
    """Controller agent that coordinates all reviewer agents."""
    
    def __init__(self, model="gpt-4.1-nano"):
        self.model = model
        self.agents = {
            # Section agents
            'S1': TitleKeywordsAgentS1(model),
            'S2': AbstractAgentS2(model),
            'S3': IntroductionAgentS3(model),
            'S4': LiteratureReviewAgentS4(model),
            'S5': MethodologyAgentS5(model),
            'S6': ResultsAgentS6(model),
            'S7': DiscussionAgentS7(model),
            'S8': ConclusionAgentS8(model),
            'S9': ReferencesAgentS9(model),
            'S10': SupplementaryMaterialsAgentS10(model),
            
            # Rigor agents
            'R1': OriginalityContributionAgent(model),
            'R2': ImpactSignificanceAgent(model),
            'R3': EthicsComplianceAgent(model),
            'R4': DataCodeAvailabilityAgent(model),
            'R5': StatisticalRigorAgent(model),
            'R6': TechnicalAccuracyAgent(model),
            'R7': ConsistencyAgent(model),
            
            # Writing agents
            'W1': LanguageStyleAgent(model),
            'W2': NarrativeStructureAgent(model),
            'W3': ClarityConcisenessAgent(model),
            'W4': TerminologyConsistencyAgent(model),
            'W5': InclusiveLanguageAgent(model),
            'W6': CitationFormattingAgent(model),
            'W7': TargetAudienceAlignmentAgent(model)
        }
    
    def run_analysis(self, text: str) -> Dict[str, Any]:
        """Runs analyses using all agents."""
        try:
            # Determine research type
            research_type = self._determine_research_type(text)
            
            # Run analyses for each agent
            results = {}
            
            # Run section agent analyses
            results["S1"] = self.agents["S1"].analyze_title_keywords(text, research_type)
            results["S2"] = self.agents["S2"].analyze_abstract(text, research_type)
            results["S3"] = self.agents["S3"].analyze_introduction(text, research_type)
            results["S4"] = self.agents["S4"].analyze_literature_review(text, research_type)
            results["S5"] = self.agents["S5"].analyze_methodology(text, research_type)
            results["S6"] = self.agents["S6"].analyze_results(text, research_type)
            results["S7"] = self.agents["S7"].analyze_discussion(text, research_type)
            results["S8"] = self.agents["S8"].analyze_conclusion(text, research_type)
            results["S9"] = self.agents["S9"].analyze_references(text, research_type)
            results["S10"] = self.agents["S10"].analyze_supplementary_materials(text, research_type)
            
            # Run rigor agent analyses
            results["R1"] = self.agents["R1"].analyze_originality_contribution(text, research_type)
            results["R2"] = self.agents["R2"].analyze_impact_significance(text, research_type)
            results["R3"] = self.agents["R3"].analyze_ethics_compliance(text, research_type)
            results["R4"] = self.agents["R4"].analyze_data_code_availability(text, research_type)
            results["R5"] = self.agents["R5"].analyze_statistical_rigor(text, research_type)
            results["R6"] = self.agents["R6"].analyze_technical_accuracy(text, research_type)
            results["R7"] = self.agents["R7"].analyze_consistency(text, research_type)
            
            # Run writing agent analyses
            results["W1"] = self.agents["W1"].analyze_language_style(text, research_type)
            results["W2"] = self.agents["W2"].analyze_narrative_structure(text, research_type)
            results["W3"] = self.agents["W3"].analyze_clarity_conciseness(text, research_type)
            results["W4"] = self.agents["W4"].analyze_terminology_consistency(text, research_type)
            results["W5"] = self.agents["W5"].analyze_inclusive_language(text, research_type)
            results["W6"] = self.agents["W6"].analyze_citation_formatting(text, research_type)
            results["W7"] = self.agents["W7"].analyze_target_audience_alignment(text, research_type)
            
            return results
        except Exception as e:
            return self._generate_error_report(f"Error in analysis: {str(e)}")
    
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
        """Generates a structured error report."""
        return {
            "error": True,
            "message": f"Error in analysis: {error_message}",
            "score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {},
            "summary": f"Analysis failed due to error: {error_message}"
        } 