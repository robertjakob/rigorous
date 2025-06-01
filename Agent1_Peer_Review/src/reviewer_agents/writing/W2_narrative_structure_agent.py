from typing import Dict, Any, List
import json
from ...core.base_agent import BaseReviewerAgent
from ...core.report_template import ReportTemplate

class NarrativeStructureAgent(BaseReviewerAgent):
    """Agent responsible for evaluating the overall flow, coherence, and logical organization of the paper."""
    
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model)
        self.name = "W2_Narrative_Structure_Agent"
        self.category = "Writing and Presentation"
        
    def analyze_narrative_structure(self, text: str, research_type: str) -> Dict[str, Any]:
        """Analyzes the narrative flow and structural organization of the text."""
        prompt = f"""Analyze the following text for narrative flow and structural organization. Focus on:
        1. Overall narrative coherence
        2. Logical progression of ideas
        3. Section transitions
        4. Paragraph organization
        5. Topic sentence effectiveness
        6. Supporting evidence integration
        7. Conclusion alignment with introduction
        8. Research question/hypothesis tracking
        9. Visual element integration
        10. Reader engagement

        For each section, provide at least 2-3 improvement suggestions. Consider these categories:
        - Abstract: Research narrative overview
        - Introduction: Research context and flow
        - Literature Review: Evidence synthesis
        - Methodology: Process description
        - Results: Finding presentation
        - Discussion: Argument development
        - Conclusion: Research story closure
        - Figures/Tables: Visual narrative

        Text to analyze: {text}
        Research type: {research_type}

        Provide a detailed analysis in the following JSON format:
        {{
            "narrative_structure_score": int,  # Single comprehensive score (1-5)
            
            "critical_remarks": [{{
                "category": str,  # "narrative_coherence", "logical_progression", "transitions", "paragraph_organization", "topic_sentences", "evidence_integration", "conclusion_alignment", "hypothesis_tracking", "visual_integration", "reader_engagement"
                "location": str,  # Section/paragraph reference
                "issue": str,  # Detailed description of the issue
                "severity": str,  # "high", "medium", "low"
                "impact": str  # How this affects the narrative
            }}],
            
            "improvement_suggestions": [{{
                "original_text": str,  # The problematic text
                "improved_version": str,  # AI-generated improvement
                "explanation": str,  # Why this improvement helps
                "location": str,  # Where to apply this change
                "category": str,  # "abstract", "introduction", "literature", "methodology", "results", "discussion", "conclusion", "figures_tables"
                "focus": str  # "narrative_coherence", "logical_progression", "transitions", "paragraph_organization", "topic_sentences", "evidence_integration", "conclusion_alignment", "hypothesis_tracking", "visual_integration", "reader_engagement"
            }}],
            
            "detailed_feedback": {{
                "narrative_coherence": str,  # Detailed paragraph about narrative coherence
                "logical_progression": str,  # Detailed paragraph about logical progression
                "section_transitions": str,  # Detailed paragraph about section transitions
                "paragraph_organization": str,  # Detailed paragraph about paragraph organization
                "topic_sentence_effectiveness": str,  # Detailed paragraph about topic sentence effectiveness
                "supporting_evidence_integration": str,  # Detailed paragraph about supporting evidence integration
                "conclusion_alignment": str,  # Detailed paragraph about conclusion alignment
                "hypothesis_tracking": str,  # Detailed paragraph about hypothesis tracking
                "visual_element_integration": str,  # Detailed paragraph about visual element integration
                "reader_engagement": str  # Detailed paragraph about reader engagement
            }},
            
            "summary": str  # Overall assessment paragraph
        }}

        Important: Generate at least 5-10 improvement suggestions across different sections and categories.
        Each suggestion should be specific, actionable, and include clear explanations of how it enhances the narrative structure.
        """
        
        try:
            response = self.llm(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            return self._generate_error_report(f"Error analyzing narrative structure: {str(e)}")
    
    def _generate_error_report(self, error_message: str) -> Dict[str, Any]:
        """Generates a structured error report."""
        return {
            "narrative_structure_score": 0,
            "critical_remarks": [],
            "improvement_suggestions": [],
            "detailed_feedback": {
                "narrative_coherence": "",
                "logical_progression": "",
                "section_transitions": "",
                "paragraph_organization": "",
                "topic_sentence_effectiveness": "",
                "supporting_evidence_integration": "",
                "conclusion_alignment": "",
                "hypothesis_tracking": "",
                "visual_element_integration": "",
                "reader_engagement": ""
            },
            "summary": f"Error in analysis: {error_message}",
            "error": True
        } 