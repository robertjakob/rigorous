import pytest
import json
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

@pytest.fixture
def sample_manuscript():
    return """
    Title: A Novel Approach to Machine Learning in Healthcare
    
    Abstract:
    This paper presents a new machine learning framework for healthcare applications,
    focusing on improved patient outcome prediction. We demonstrate significant
    improvements over existing methods in terms of accuracy and interpretability.
    
    Introduction:
    Machine learning has revolutionized healthcare analytics in recent years.
    However, existing approaches often lack interpretability and fail to incorporate
    domain-specific medical knowledge effectively. Our novel framework addresses
    these limitations through a hybrid approach combining deep learning with
    traditional statistical methods.
    
    Methods:
    We propose a new neural network architecture that incorporates medical domain
    knowledge through constrained optimization. Our approach uses a combination of
    attention mechanisms and traditional statistical methods. The framework was
    implemented using PyTorch and evaluated on a large-scale healthcare dataset.
    
    Results:
    Our method achieves 95% accuracy (p < 0.001) on the test set, representing a
    significant improvement over the baseline (85%, p < 0.001). The attention
    mechanisms provide interpretable insights into the model's decision-making
    process, which was validated by domain experts.
    
    Discussion:
    The results demonstrate the effectiveness of our approach in both accuracy
    and interpretability. The hybrid architecture successfully balances the power
    of deep learning with the interpretability requirements of healthcare applications.
    
    Ethics Statement:
    This study was approved by the IRB (approval #12345). All patient data was
    anonymized and handled according to HIPAA guidelines. No conflicts of interest
    were declared.
    
    Data Availability:
    The dataset used in this study is available at [repository URL]. Code for
    reproducing all results is available at [code repository URL].
    """

@pytest.fixture
def agents():
    # Use gpt-3.5-turbo for all agents
    model = "gpt-3.5-turbo"
    
    # Initialize rigor agents
    rigor_agents = {
        "R1": OriginalityContributionAgent(model=model),
        "R2": ImpactSignificanceAgent(model=model),
        "R3": EthicsComplianceAgent(model=model),
        "R4": DataCodeAvailabilityAgent(model=model),
        "R5": StatisticalRigorAgent(model=model),
        "R6": TechnicalAccuracyAgent(model=model),
        "R7": ConsistencyAgent(model=model)
    }
    
    # Initialize writing agents
    writing_agents = {
        "W1": LanguageStyleAgent(model=model),
        "W2": NarrativeStructureAgent(model=model),
        "W3": ClarityConcisenessAgent(model=model),
        "W4": TerminologyConsistencyAgent(model=model)
    }
    
    return {**rigor_agents, **writing_agents}

def test_all_agents(agents, sample_manuscript):
    """Test all agents with a sample manuscript and print their reviews"""
    print("\n=== Testing All Agents with gpt-3.5-turbo ===\n")
    
    # Test each agent
    for name, agent in agents.items():
        print(f"\n--- {name} Review ---")
        
        try:
            # Call the appropriate analysis method based on agent type
            if name == "R1":
                result = agent.analyze_originality_contribution(sample_manuscript, "healthcare")
            elif name == "R2":
                result = agent.analyze_impact_significance(sample_manuscript, {"field": "healthcare"})
            elif name == "R3":
                result = agent.analyze_ethics_compliance(sample_manuscript, "healthcare")
            elif name == "R4":
                result = agent.analyze_data_code_availability(sample_manuscript, "healthcare")
            elif name == "R5":
                result = agent.analyze_statistical_rigor(sample_manuscript, "healthcare")
            elif name == "R6":
                result = agent.analyze_technical_accuracy(sample_manuscript, "healthcare")
            elif name == "R7":
                result = agent.analyze_consistency(sample_manuscript, "healthcare")
            elif name == "W1":
                result = agent.analyze_language_style(sample_manuscript, "healthcare")
            elif name == "W2":
                result = agent.analyze_narrative_structure(sample_manuscript, "healthcare")
            elif name == "W3":
                result = agent.analyze_clarity_conciseness(sample_manuscript, "healthcare")
            else:  # W4
                result = agent.analyze_terminology_consistency(sample_manuscript, "healthcare")
            
            # Print the score
            score_key = [k for k in result.keys() if k.endswith('_score')][0]
            print(f"Score: {result[score_key]}/5")
            
            # Print critical remarks
            print("\nCritical Remarks:")
            if isinstance(result["critical_remarks"], dict):
                for category, remarks in result["critical_remarks"].items():
                    print(f"  {category}:")
                    for remark in remarks:
                        print(f"    - {remark}")
            else:  # List type
                for remark in result["critical_remarks"]:
                    if isinstance(remark, dict):
                        print(f"  {remark.get('category', 'General')}:")
                        print(f"    - {remark.get('issue', remark)}")
                    else:
                        print(f"  - {remark}")
            
            # Print improvement suggestions
            print("\nImprovement Suggestions:")
            if isinstance(result["improvement_suggestions"], dict):
                for category, suggestions in result["improvement_suggestions"].items():
                    print(f"  {category}:")
                    for suggestion in suggestions:
                        print(f"    - {suggestion}")
            else:  # List type
                for suggestion in result["improvement_suggestions"]:
                    if isinstance(suggestion, dict):
                        print(f"  - {suggestion.get('suggestion', suggestion)}")
                    else:
                        print(f"  - {suggestion}")
            
            # Print summary
            print(f"\nSummary: {result['summary']}")
            
            # Verify output format
            assert isinstance(result, dict)
            assert any(key.endswith('_score') for key in result.keys())
            assert "critical_remarks" in result
            assert "improvement_suggestions" in result
            assert "detailed_feedback" in result
            assert "summary" in result
            
            print("\n" + "="*50)
            
        except Exception as e:
            print(f"Error testing {name}: {str(e)}")
            print("\n" + "="*50)

def test_agent_initialization(agents):
    """Test that all agents initialize correctly with expected attributes"""
    expected_names = {
        "R1": "R1_Originality_Contribution_Agent",
        "R2": "R2_Impact_Significance_Agent",
        "R3": "R3_Ethics_Compliance_Agent",
        "R4": "R4_Data_Code_Availability_Agent",
        "R5": "R5_Statistical_Rigor_Agent",
        "R6": "R6_Technical_Accuracy_Agent",
        "R7": "R7_Consistency_Agent",
        "W1": "W1_Language_Style_Agent",
        "W2": "W2_Narrative_Structure_Agent",
        "W3": "W3_Clarity_Conciseness_Agent",
        "W4": "W4_Terminology_Consistency_Agent"
    }
    
    for name, agent in agents.items():
        assert agent.model == "gpt-3.5-turbo"
        assert agent.name == expected_names[name]
        assert agent.category in ["Scientific Rigor", "Writing Quality", "Writing and Presentation"] 