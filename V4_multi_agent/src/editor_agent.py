from typing import Dict, List, Any
import json
import os
from openai_client import OpenAIClient

class EditorAgent:
    """Editor agent that analyzes papers and creates specialized review teams."""
    
    def __init__(self, model_config: Dict[str, str] = None):
        """Initialize the editor agent with configurable model settings.
        
        Args:
            model_config (Dict[str, str], optional): Configuration for different models. Defaults to:
                {
                    "default": "gpt-3.5-turbo",  # Cheap model for testing
                    "production": "gpt-4-turbo-preview",  # More expensive model for production
                    "current": "default"  # Which model to use currently
                }
        """
        try:
        self.client = OpenAIClient()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OpenAI client: {str(e)}")
        
        # Default model configuration
        self.model_config = {
            "default": "gpt-3.5-turbo",  # Cheap model for testing
            "production": "gpt-4-turbo-preview",  # More expensive model for production
            "current": "default"  # Which model to use currently
        }
        
        # Update with any provided configuration
        if model_config:
            self.model_config.update(model_config)
        
        # Core reviewers that are always included
        self.core_reviewers = [
            {
                "id": "audience_terminology_reviewer",
                "role": "Audience and Terminology Expert",
                "expertise": [
                    "Audience Analysis",
                    "Field-Specific Terminology",
                    "Technical Language",
                    "Communication Strategy"
                ],
                "focus_areas": [
                    "Audience Appropriateness",
                    "Terminology Usage",
                    "Technical Language Clarity",
                    "Communication Effectiveness"
                ],
                "review_criteria": [
                    "Audience targeting",
                    "Terminology accuracy",
                    "Technical language appropriateness",
                    "Communication strategy effectiveness"
                ],
                "required_background": [
                    "Audience analysis",
                    "Field-specific terminology",
                    "Technical communication",
                    "Communication strategies"
                ]
            },
            {
                "id": "grammar_structure_reviewer",
                "role": "Grammar and Structure Expert",
                "expertise": [
                    "Grammar",
                    "Sentence Structure",
                    "Paragraph Organization",
                    "Text Flow"
                ],
                "focus_areas": [
                    "Grammatical Correctness",
                    "Sentence Construction",
                    "Paragraph Coherence",
                    "Text Flow and Transitions"
                ],
                "review_criteria": [
                    "Grammar accuracy",
                    "Sentence structure",
                    "Paragraph organization",
                    "Text flow and coherence"
                ],
                "required_background": [
                    "Grammar rules",
                    "Sentence construction",
                    "Paragraph organization",
                    "Text flow principles"
                ]
            },
            {
                "id": "spelling_mechanics_reviewer",
                "role": "Spelling and Mechanics Expert",
                "expertise": [
                    "Spelling",
                    "Punctuation",
                    "Capitalization",
                    "Formatting"
                ],
                "focus_areas": [
                    "Spelling Accuracy",
                    "Punctuation Usage",
                    "Capitalization Rules",
                    "Formatting Consistency"
                ],
                "review_criteria": [
                    "Spelling correctness",
                    "Punctuation accuracy",
                    "Capitalization appropriateness",
                    "Formatting consistency"
                ],
                "required_background": [
                    "Spelling rules",
                    "Punctuation guidelines",
                    "Capitalization standards",
                    "Formatting conventions"
                ]
            },
            {
                "id": "visual_presentation_reviewer",
                "role": "Visual Presentation Expert",
                "expertise": [
                    "Figure Design",
                    "Table Layout",
                    "Visual Communication",
                    "Publication Format"
                ],
                "focus_areas": [
                    "Figure Clarity and Design",
                    "Table Organization",
                    "Visual Communication Effectiveness",
                    "Publication Format Compliance"
                ],
                "review_criteria": [
                    "Figure clarity and design",
                    "Table organization",
                    "Visual communication effectiveness",
                    "Publication format compliance"
                ],
                "required_background": [
                    "Figure design principles",
                    "Table layout standards",
                    "Visual communication",
                    "Publication guidelines"
                ]
            },
            {
                "id": "literature_review_expert",
                "role": "Literature Review Expert",
                "expertise": [
                    "Literature Synthesis",
                    "Citation Analysis",
                    "Reference Management",
                    "Literature Coverage"
                ],
                "focus_areas": [
                    "Citation Accuracy",
                    "Literature Coverage",
                    "Reference Consistency",
                    "Literature Gaps"
                ],
                "review_criteria": [
                    "Citation completeness",
                    "Literature coverage",
                    "Reference formatting",
                    "Literature gap identification"
                ],
                "required_background": [
                    "Citation standards",
                    "Literature review methodologies",
                    "Reference management",
                    "Literature analysis"
                ]
            },
            {
                "id": "data_analysis_expert",
                "role": "Data Analysis Expert",
                "expertise": [
                    "Statistical Methods",
                    "Data Interpretation",
                    "Analytical Rigor",
                    "Statistical Validity"
                ],
                "focus_areas": [
                    "Statistical Validity",
                    "Data Interpretation Accuracy",
                    "Analytical Methods",
                    "Statistical Rigor"
                ],
                "review_criteria": [
                    "Statistical appropriateness",
                    "Data interpretation quality",
                    "Analytical rigor",
                    "Statistical validity"
                ],
                "required_background": [
                    "Statistical analysis",
                    "Data interpretation",
                    "Analytical methodologies",
                    "Statistical validation"
                ]
            },
            {
                "id": "results_presentation_expert",
                "role": "Results Presentation Expert",
                "expertise": [
                    "Results Organization",
                    "Data Visualization",
                    "Findings Presentation",
                    "Results Clarity"
                ],
                "focus_areas": [
                    "Results Clarity",
                    "Data Presentation",
                    "Findings Organization",
                    "Results Impact"
                ],
                "review_criteria": [
                    "Results presentation quality",
                    "Data visualization effectiveness",
                    "Findings clarity",
                    "Results impact"
                ],
                "required_background": [
                    "Results presentation",
                    "Data visualization",
                    "Scientific communication",
                    "Impact assessment"
                ]
            },
            {
                "id": "discussion_quality_expert",
                "role": "Discussion Quality Expert",
                "expertise": [
                    "Discussion Depth",
                    "Interpretation Quality",
                    "Implications Analysis",
                    "Discussion Structure"
                ],
                "focus_areas": [
                    "Discussion Thoroughness",
                    "Interpretation Accuracy",
                    "Implications Clarity",
                    "Discussion Flow"
                ],
                "review_criteria": [
                    "Discussion quality",
                    "Interpretation depth",
                    "Implications presentation",
                    "Discussion structure"
                ],
                "required_background": [
                    "Discussion methodologies",
                    "Interpretation frameworks",
                    "Implications analysis",
                    "Discussion structure"
                ]
            },
            {
                "id": "conclusion_strength_expert",
                "role": "Conclusion Strength Expert",
                "expertise": [
                    "Conclusion Formulation",
                    "Summary Quality",
                    "Future Directions",
                    "Conclusion Impact"
                ],
                "focus_areas": [
                    "Conclusion Clarity",
                    "Summary Completeness",
                    "Future Directions Relevance",
                    "Conclusion Impact"
                ],
                "review_criteria": [
                    "Conclusion strength",
                    "Summary quality",
                    "Future directions appropriateness",
                    "Conclusion impact"
                ],
                "required_background": [
                    "Conclusion writing",
                    "Summary techniques",
                    "Future research planning",
                    "Impact assessment"
                ]
            },
            {
                "id": "abstract_quality_expert",
                "role": "Abstract Quality Expert",
                "expertise": [
                    "Abstract Writing",
                    "Summary Skills",
                    "Key Points Extraction",
                    "Abstract Structure"
                ],
                "focus_areas": [
                    "Abstract Clarity",
                    "Summary Completeness",
                    "Key Points Presentation",
                    "Abstract Impact"
                ],
                "review_criteria": [
                    "Abstract quality",
                    "Summary accuracy",
                    "Key points clarity",
                    "Abstract impact"
                ],
                "required_background": [
                    "Abstract writing",
                    "Summary techniques",
                    "Key points extraction",
                    "Impact assessment"
                ]
            },
            {
                "id": "introduction_quality_expert",
                "role": "Introduction Quality Expert",
                "expertise": [
                    "Introduction Writing",
                    "Context Setting",
                    "Research Gap Identification",
                    "Introduction Structure"
                ],
                "focus_areas": [
                    "Introduction Clarity",
                    "Context Completeness",
                    "Research Gap Presentation",
                    "Introduction Flow"
                ],
                "review_criteria": [
                    "Introduction quality",
                    "Context setting",
                    "Research gap clarity",
                    "Introduction flow"
                ],
                "required_background": [
                    "Introduction writing",
                    "Context setting",
                    "Research gap identification",
                    "Introduction structure"
                ]
            },
            {
                "id": "limitations_analysis_expert",
                "role": "Limitations Analysis Expert",
                "expertise": [
                    "Limitations Identification",
                    "Constraint Analysis",
                    "Boundary Assessment",
                    "Limitations Impact"
                ],
                "focus_areas": [
                    "Limitations Completeness",
                    "Constraint Clarity",
                    "Boundary Definition",
                    "Limitations Impact"
                ],
                "review_criteria": [
                    "Limitations coverage",
                    "Constraint presentation",
                    "Boundary clarity",
                    "Limitations impact"
                ],
                "required_background": [
                    "Limitations analysis",
                    "Constraint assessment",
                    "Boundary definition",
                    "Impact assessment"
                ]
            },
            {
                "id": "future_work_expert",
                "role": "Future Work Expert",
                "expertise": [
                    "Future Research Planning",
                    "Extension Identification",
                    "Direction Setting",
                    "Future Impact"
                ],
                "focus_areas": [
                    "Future Work Clarity",
                    "Extension Relevance",
                    "Direction Appropriateness",
                    "Future Impact"
                ],
                "review_criteria": [
                    "Future work quality",
                    "Extension value",
                    "Direction clarity",
                    "Future impact"
                ],
                "required_background": [
                    "Future research planning",
                    "Extension assessment",
                    "Direction setting",
                    "Impact assessment"
                ]
            },
            {
                "id": "cross_reference_expert",
                "role": "Cross-Reference Expert",
                "expertise": [
                    "Cross-Reference Accuracy",
                    "Internal Consistency",
                    "Reference Linking",
                    "Reference Management"
                ],
                "focus_areas": [
                    "Cross-Reference Completeness",
                    "Internal Consistency",
                    "Reference Linking",
                    "Reference Accuracy"
                ],
                "review_criteria": [
                    "Cross-reference accuracy",
                    "Internal consistency",
                    "Reference linking quality",
                    "Reference accuracy"
                ],
                "required_background": [
                    "Cross-reference standards",
                    "Internal consistency",
                    "Reference linking",
                    "Reference management"
                ]
            },
            {
                "id": "methodology_reviewer",
                "role": "Research Methodology Expert",
                "expertise": [
                    "Research Design",
                    "Statistical Analysis",
                    "Experimental Methods",
                    "Data Collection",
                    "Reproducibility"
                ],
                "focus_areas": [
                    "Research Design Quality",
                    "Statistical Rigor",
                    "Experimental Protocol",
                    "Data Collection Methods",
                    "Reproducibility Standards"
                ],
                "review_criteria": [
                    "Methodological soundness",
                    "Statistical analysis appropriateness",
                    "Experimental design quality",
                    "Data collection rigor",
                    "Reproducibility potential"
                ],
                "required_background": [
                    "Research methodology",
                    "Statistical analysis",
                    "Experimental design",
                    "Data collection standards",
                    "Reproducibility frameworks"
                ]
            },
            {
                "id": "ethics_compliance_reviewer",
                "role": "Ethics and Compliance Expert",
                "expertise": [
                    "Research Ethics",
                    "Data Privacy",
                    "Informed Consent",
                    "Conflict of Interest",
                    "Regulatory Compliance"
                ],
                "focus_areas": [
                    "Ethical Considerations",
                    "Data Protection",
                    "Participant Rights",
                    "Conflict Management",
                    "Regulatory Requirements"
                ],
                "review_criteria": [
                    "Ethical compliance",
                    "Data privacy measures",
                    "Informed consent process",
                    "Conflict of interest disclosure",
                    "Regulatory adherence"
                ],
                "required_background": [
                    "Research ethics",
                    "Data protection regulations",
                    "Human subjects research",
                    "Conflict of interest guidelines",
                    "Research compliance"
                ]
            },
            {
                "id": "technical_implementation_reviewer",
                "role": "Technical Implementation Expert",
                "expertise": [
                    "Technical Architecture",
                    "Implementation Quality",
                    "Code/Algorithm Review",
                    "System Design",
                    "Performance Optimization"
                ],
                "focus_areas": [
                    "Technical Architecture",
                    "Implementation Details",
                    "Code/Algorithm Quality",
                    "System Design",
                    "Performance Considerations"
                ],
                "review_criteria": [
                    "Technical architecture soundness",
                    "Implementation quality",
                    "Code/algorithm efficiency",
                    "System design appropriateness",
                    "Performance optimization"
                ],
                "required_background": [
                    "Software architecture",
                    "Implementation best practices",
                    "Code review standards",
                    "System design principles",
                    "Performance optimization"
                ]
            },
            {
                "id": "impact_significance_reviewer",
                "role": "Impact and Significance Expert",
                "expertise": [
                    "Field Impact Assessment",
                    "Scientific Contribution",
                    "Practical Applications",
                    "Future Research Directions",
                    "Knowledge Advancement"
                ],
                "focus_areas": [
                    "Scientific Impact",
                    "Field Contribution",
                    "Practical Relevance",
                    "Future Implications",
                    "Knowledge Gap Addressing"
                ],
                "review_criteria": [
                    "Scientific contribution significance",
                    "Field impact potential",
                    "Practical application value",
                    "Future research implications",
                    "Knowledge advancement"
                ],
                "required_background": [
                    "Impact assessment",
                    "Scientific contribution evaluation",
                    "Practical application analysis",
                    "Future research trends",
                    "Knowledge gap identification"
                ]
            },
            {
                "id": "literature_coverage_expert",
                "role": "Literature Coverage Expert",
                "expertise": [
                    "Literature Comprehensiveness",
                    "Related Work Analysis",
                    "Citation Completeness",
                    "Field Coverage",
                    "Recent Developments"
                ],
                "focus_areas": [
                    "Literature Coverage Completeness",
                    "Related Work Analysis",
                    "Citation Appropriateness",
                    "Field Coverage Breadth",
                    "Recent Literature Integration"
                ],
                "review_criteria": [
                    "Literature coverage completeness",
                    "Related work analysis depth",
                    "Citation appropriateness",
                    "Field coverage breadth",
                    "Recent literature integration"
                ],
                "required_background": [
                    "Literature review methodologies",
                    "Citation analysis",
                    "Field coverage assessment",
                    "Recent developments tracking",
                    "Related work analysis"
                ]
            },
            {
                "id": "research_gap_contribution_expert",
                "role": "Research Gap and Contribution Expert",
                "expertise": [
                    "Research Gap Analysis",
                    "Contribution Positioning",
                    "Literature Synthesis",
                    "Field Impact Assessment",
                    "Academic Diplomacy"
                ],
                "focus_areas": [
                    "Research Gap Identification",
                    "Contribution Significance",
                    "Literature Positioning",
                    "Field Impact Balance",
                    "Academic Tone Management"
                ],
                "review_criteria": [
                    "Research gap clarity and justification",
                    "Contribution significance and uniqueness",
                    "Literature positioning accuracy",
                    "Field impact balance",
                    "Academic tone appropriateness"
                ],
                "required_background": [
                    "Research gap analysis methodologies",
                    "Contribution assessment frameworks",
                    "Literature synthesis techniques",
                    "Field impact evaluation",
                    "Academic communication strategies"
                ]
            }
        ]
    
    def get_current_model(self) -> str:
        """Get the currently configured model to use."""
        model_key = self.model_config["current"]
        return self.model_config[model_key]

    def set_model(self, model_key: str) -> None:
        """Set which model configuration to use.
        
        Args:
            model_key (str): Key of the model to use ("default" or "production")
        """
        if model_key not in self.model_config:
            raise ValueError(f"Unknown model key: {model_key}. Must be one of: {list(self.model_config.keys())}")
        self.model_config["current"] = model_key
    
    def analyze_paper(self, paper_text: str) -> Dict[str, Any]:
        """Analyze the paper to determine required expertise and review criteria.
        
        Args:
            paper_text (str): The text content of the paper
            
        Returns:
            Dict[str, Any]: Analysis of paper requirements and review team structure
        """
        try:
            response = self.client.analyze_manuscript(paper_text, {
                "role": "expert scientific editor",
                "task": "analyze paper",
                "model": self.get_current_model(),
                "prompt": """Analyze this scientific paper and provide:
                1. Main domain and subdomains
                2. Technical areas requiring expertise
                3. Required review team composition
                4. Key evaluation criteria
                
                Return the analysis in JSON format with these exact keys:
                {
                    "domains": {
                        "main_domain": "string",
                        "subdomains": ["string"]
                    },
                    "technical_areas": ["string"],
                    "required_expertise": ["string"],
                    "evaluation_criteria": ["string"]
                }"""
            })
            
            if "error" in response:
                raise Exception(response["error"])
                
            return response
            
        except Exception as e:
            print(f"Error analyzing paper: {str(e)}")
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
                "prompt": prompt,
                "model": self.get_current_model()  # Use configured model
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
    
    def identify_key_scientists(self, paper_content: str) -> List[Dict[str, Any]]:
        """Identify key scientists in the field based on paper content and citations."""
        try:
            response = self.client.analyze_manuscript(paper_content, {
                "role": "expert scientific editor",
                "task": "identify key scientists",
                "model": self.get_current_model(),
                "prompt": """Identify the key scientists mentioned or relevant to this paper.
                For each scientist provide:
                {
                    "name": "string",
                    "research_focus": "string",
                    "review_style": "string",
                    "potential_concerns": ["string"],
                    "appreciated_areas": ["string"]
                }
                
                Return the list in JSON format."""
            })
            
            if "error" in response:
                raise Exception(response["error"])
            
            return response.get("scientists", [])
            
        except Exception as e:
            print(f"Error identifying scientists: {str(e)}")
            return []

    def simulate_scientist_feedback(self, paper_content: str, scientist: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate feedback from a specific scientist."""
        try:
            response = self.client.analyze_manuscript(paper_content, {
                "role": "expert scientific editor",
                "task": "simulate scientist feedback",
                "model": self.get_current_model(),
                "prompt": f"""As {scientist['name']}, an expert in {scientist['research_focus']},
                review this paper and provide feedback in this JSON format:
                {{
                    "overall_assessment": "string",
                    "strengths": ["string"],
                    "concerns": ["string"],
                    "recommendations": ["string"],
                    "final_verdict": "string"
                }}"""
            })
            
            if "error" in response:
                raise Exception(response["error"])
            
            return response
            
        except Exception as e:
            print(f"Error simulating feedback: {str(e)}")
            return {
                "error": f"Failed to simulate feedback for {scientist['name']}",
                "details": str(e)
            }

    def generate_final_report(self, review_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive final report including all reviewer feedback.
        
        Args:
            review_plan (Dict[str, Any]): The complete review plan including all feedback
            
        Returns:
            Dict[str, Any]: Comprehensive final report
        """
        try:
            response = self.client.analyze_manuscript(str(review_plan), {
                "role": "expert scientific editor",
                "task": "generate final report",
                "model": self.get_current_model(),
                "prompt": """Generate a comprehensive final report in this JSON format:
                {
                    "executive_summary": {
                        "overall_assessment": "string",
                        "key_strengths": ["string"],
                        "key_concerns": ["string"],
                        "main_recommendations": ["string"]
                    },
                    "thematic_analysis": {
                        "common_themes": ["string"],
                        "conflicting_feedback": ["string"],
                        "consensus_points": ["string"]
                    },
                    "final_assessment": {
                        "overall_rating": "string",
                        "publication_readiness": "string",
                        "required_changes": ["string"],
                        "estimated_timeline": "string"
                    }
                }"""
            })
            
            if "error" in response:
                raise Exception(response["error"])
            
            return response
            
        except Exception as e:
            print(f"Error generating final report: {str(e)}")
            return {
                "error": "Failed to generate final report",
                "details": str(e)
            }

    def generate_review_plan(self, paper_content: str) -> Dict[str, Any]:
        """Generate a complete review plan including simulated expert feedback."""
        try:
            # Get basic paper analysis
            paper_analysis = self.analyze_paper(paper_content)
            if "error" in paper_analysis:
                raise Exception(paper_analysis["error"])
            
            # Identify key scientists
            key_scientists = self.identify_key_scientists(paper_content)
            
            # Simulate feedback from each scientist
            simulated_feedback = {}
            for scientist in key_scientists:
                feedback = self.simulate_scientist_feedback(paper_content, scientist)
                if "error" not in feedback:
                    simulated_feedback[scientist['name']] = feedback
            
            # Generate the complete review plan
            review_plan = {
                "paper_analysis": paper_analysis,
                "key_scientists": key_scientists,
                "simulated_feedback": simulated_feedback
            }
            
            # Generate the final report
            final_report = self.generate_final_report(review_plan)
            
            return {
                "review_plan": review_plan,
                "final_report": final_report
            }
            
        except Exception as e:
            print(f"Error generating review plan: {str(e)}")
            return {
                "error": "Failed to generate review plan",
                "details": str(e),
                "review_plan": {
                    "paper_analysis": paper_analysis if 'paper_analysis' in locals() else {"error": "Analysis failed"},
                    "key_scientists": key_scientists if 'key_scientists' in locals() else [],
                    "simulated_feedback": simulated_feedback if 'simulated_feedback' in locals() else {}
                },
                "final_report": {
                    "error": "Report generation failed",
                    "executive_summary": {"error": "Generation failed"},
                    "thematic_analysis": {"error": "Generation failed"},
                    "final_assessment": {"error": "Generation failed"}
                }
            }

    def get_agent_feedback(self, agent_name, paper):
        """Get detailed feedback from a specific specialized reviewer agent."""
        # Find the agent in the core reviewers
        agent = next((a for a in self.core_reviewers if a['id'] == agent_name), None)
        if not agent:
            return {"error": f"Agent {agent_name} not found in review team"}
        
        # Create the prompt for the specific agent
        prompt = f"""As a {agent['role']} reviewer specializing in {', '.join(agent['expertise'])}, 
        please provide detailed feedback on the following paper:

        {paper}

        Focus specifically on:
        {', '.join(agent['review_criteria'])}

        Provide your feedback in the following JSON format:
        {{
            "overall_assessment": "Detailed assessment of the paper from your expertise perspective",
            "strengths": [
                "List of specific strengths identified"
            ],
            "areas_for_improvement": [
                "List of areas needing improvement"
            ],
            "specific_recommendations": [
                "List of actionable recommendations"
            ],
            "final_verdict": "Your final verdict on the paper"
        }}

        Base your review on your expertise in {', '.join(agent['required_background'])}.
        Ensure your response is valid JSON.
        """

        # Get the feedback from the agent
        response = self.client.analyze_manuscript(paper, {
            "role": "expert scientific editor",
            "task": "get agent feedback",
            "model": self.get_current_model(),
            "prompt": prompt
        })

        # Extract JSON from response if needed
        if isinstance(response, str):
            try:
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    response = json.loads(response[start_idx:end_idx])
            except json.JSONDecodeError:
                response = {"error": "Failed to parse feedback"}

        return {
            "agent_name": agent_name,
            "role": agent['role'],
            "expertise": agent['expertise'],
            "focus_areas": agent['focus_areas'],
            "feedback": response
            } 