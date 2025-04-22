from typing import Dict, Any, List
import json
import os
from datetime import datetime
from src.core.base_agent import BaseReviewerAgent
from src.core.report_template import ReportTemplate
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
from src.reviewer_agents.writing.W5_inclusive_language_agent import InclusiveLanguageAgent
from src.reviewer_agents.writing.W6_citation_formatting_agent import CitationFormattingAgent
from src.reviewer_agents.writing.W7_target_audience_agent import TargetAudienceAlignmentAgent
from src.reviewer_agents.writing.W8_visual_presentation_agent import VisualPresentationAgentW8

class ControllerAgent:
    """Coordinates the review process across all reviewer agents."""
    
    def __init__(self, model="gpt-4"):
        # Initialize research quality agents
        self.r1_agent = OriginalityContributionAgent(model)
        self.r2_agent = ImpactSignificanceAgent(model)
        self.r3_agent = EthicsComplianceAgent(model)
        self.r4_agent = DataCodeAvailabilityAgent(model)
        self.r5_agent = StatisticalRigorAgent(model)
        self.r6_agent = TechnicalAccuracyAgent(model)
        self.r7_agent = ConsistencyAgent(model)
        
        # Initialize writing and presentation agents
        self.w1_agent = LanguageStyleAgent(model)
        self.w2_agent = NarrativeStructureAgent(model)
        self.w3_agent = ClarityConcisenessAgent(model)
        self.w4_agent = TerminologyConsistencyAgent(model)
        self.w5_agent = InclusiveLanguageAgent(model)
        self.w6_agent = CitationFormattingAgent(model)
        self.w7_agent = TargetAudienceAlignmentAgent(model)
        self.w8_agent = VisualPresentationAgentW8(model)
        
        # Create results directory if it doesn't exist
        os.makedirs("results", exist_ok=True)
    
    def run_analysis(self, manuscript_text: str) -> Dict[str, Any]:
        """Run the complete manuscript analysis using all agents."""
        results = {}
        research_type = "research"  # Default research type
        
        # Run analysis with research quality agents
        try:
            results["R1"] = self.r1_agent.analyze_originality_contribution(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in R1: {str(e)}")
            results["R1"] = self._generate_error_report("R1", str(e))
            
        try:
            results["R2"] = self.r2_agent.analyze_impact_significance(manuscript_text, {"field": research_type})
        except Exception as e:
            print(f"Error in R2: {str(e)}")
            results["R2"] = self._generate_error_report("R2", str(e))
            
        try:
            results["R3"] = self.r3_agent.analyze_ethics_compliance(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in R3: {str(e)}")
            results["R3"] = self._generate_error_report("R3", str(e))
            
        try:
            results["R4"] = self.r4_agent.analyze_data_code_availability(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in R4: {str(e)}")
            results["R4"] = self._generate_error_report("R4", str(e))
            
        try:
            results["R5"] = self.r5_agent.analyze_statistical_rigor(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in R5: {str(e)}")
            results["R5"] = self._generate_error_report("R5", str(e))
            
        try:
            results["R6"] = self.r6_agent.analyze_technical_accuracy(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in R6: {str(e)}")
            results["R6"] = self._generate_error_report("R6", str(e))
            
        try:
            results["R7"] = self.r7_agent.analyze_consistency(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in R7: {str(e)}")
            results["R7"] = self._generate_error_report("R7", str(e))
        
        # Run analysis with writing and presentation agents
        try:
            results["W1"] = self.w1_agent.analyze_language_style(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in W1: {str(e)}")
            results["W1"] = self._generate_error_report("W1", str(e))
            
        try:
            results["W2"] = self.w2_agent.analyze_narrative_structure(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in W2: {str(e)}")
            results["W2"] = self._generate_error_report("W2", str(e))
            
        try:
            results["W3"] = self.w3_agent.analyze_clarity_conciseness(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in W3: {str(e)}")
            results["W3"] = self._generate_error_report("W3", str(e))
            
        try:
            results["W4"] = self.w4_agent.analyze_terminology_consistency(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in W4: {str(e)}")
            results["W4"] = self._generate_error_report("W4", str(e))
            
        try:
            results["W5"] = self.w5_agent.analyze_inclusive_language(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in W5: {str(e)}")
            results["W5"] = self._generate_error_report("W5", str(e))
            
        try:
            results["W6"] = self.w6_agent.analyze_citation_formatting(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in W6: {str(e)}")
            results["W6"] = self._generate_error_report("W6", str(e))
            
        try:
            results["W7"] = self.w7_agent.analyze_target_audience_alignment(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in W7: {str(e)}")
            results["W7"] = self._generate_error_report("W7", str(e))
            
        try:
            results["W8"] = self.w8_agent.analyze_visual_presentation(manuscript_text, research_type)
        except Exception as e:
            print(f"Error in W8: {str(e)}")
            results["W8"] = self._generate_error_report("W8", str(e))
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"results/combined_results_{timestamp}.json", "w") as f:
            json.dump(results, f, indent=2)
            
        return results
    
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