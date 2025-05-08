import pytest
import json
from src.reviewer_agents.rigor.R1_originality_contribution_agent import OriginalityContributionAgent
from src.reviewer_agents.rigor.R2_impact_significance_agent import ImpactSignificanceAgent
from src.reviewer_agents.rigor.R3_ethics_compliance_agent import EthicsComplianceAgent
from src.reviewer_agents.rigor.R4_data_code_availability_agent import DataCodeAvailabilityAgent
from src.reviewer_agents.rigor.R5_statistical_rigor_agent import StatisticalRigorAgent
from src.reviewer_agents.rigor.R6_technical_accuracy_agent import TechnicalAccuracyAgent
from src.reviewer_agents.rigor.R7_consistency_agent import ConsistencyAgent

@pytest.fixture
def sample_manuscript():
    return """
    Title: A Novel Approach to Machine Learning in Healthcare
    
    Abstract:
    This paper presents a new machine learning framework for healthcare applications,
    focusing on improved patient outcome prediction. We demonstrate significant
    improvements over existing methods in terms of accuracy and interpretability.
    
    Methods:
    We propose a new neural network architecture that incorporates medical domain
    knowledge through constrained optimization. Our approach uses a combination of
    attention mechanisms and traditional statistical methods.
    
    Results:
    Our method achieves 95% accuracy (p < 0.001) on the test set. All data and code
    are available at https://github.com/example/healthcare-ml.
    
    Ethics Statement:
    This study was approved by the IRB (approval #12345). All patient data was
    anonymized and handled according to HIPAA guidelines.
    """

@pytest.fixture
def agents():
    return {
        "R1": OriginalityContributionAgent(model="gpt-3.5-turbo"),
        "R2": ImpactSignificanceAgent(model="gpt-3.5-turbo"),
        "R3": EthicsComplianceAgent(model="gpt-3.5-turbo"),
        "R4": DataCodeAvailabilityAgent(model="gpt-3.5-turbo"),
        "R5": StatisticalRigorAgent(model="gpt-3.5-turbo"),
        "R6": TechnicalAccuracyAgent(model="gpt-3.5-turbo"),
        "R7": ConsistencyAgent(model="gpt-3.5-turbo")
    }

def test_agent_initialization(agents):
    """Test that all agents initialize correctly with expected attributes"""
    expected_names = {
        "R1": "R1_Originality_Contribution_Agent",
        "R2": "R2_Impact_Significance_Agent",
        "R3": "R3_Ethics_Compliance_Agent",
        "R4": "R4_Data_Code_Availability_Agent",
        "R5": "R5_Statistical_Rigor_Agent",
        "R6": "R6_Technical_Accuracy_Agent",
        "R7": "R7_Consistency_Agent"
    }
    for name, agent in agents.items():
        assert agent.model == "gpt-3.5-turbo"
        assert agent.name == expected_names[name]
        assert agent.category == "Scientific Rigor"

def test_originality_contribution_analysis(agents, sample_manuscript):
    """Test R1 agent's analysis functionality"""
    result = agents["R1"].analyze_originality_contribution(sample_manuscript, "healthcare")
    assert isinstance(result, dict)
    assert "originality_contribution_score" in result
    assert isinstance(result["originality_contribution_score"], (int, float))
    assert 1 <= result["originality_contribution_score"] <= 10
    assert "critical_remarks" in result
    assert "improvement_suggestions" in result
    assert "detailed_feedback" in result
    assert "summary" in result

def test_impact_significance_analysis(agents, sample_manuscript):
    """Test R2 agent's analysis functionality"""
    result = agents["R2"].analyze_impact_significance(sample_manuscript, {"field": "healthcare"})
    assert isinstance(result, dict)
    assert "impact_significance_score" in result
    assert 1 <= result["impact_significance_score"] <= 10
    assert "critical_remarks" in result
    assert "improvement_suggestions" in result

def test_ethics_compliance_analysis(agents, sample_manuscript):
    """Test R3 agent's analysis functionality"""
    result = agents["R3"].analyze_ethics_compliance(sample_manuscript, "healthcare")
    assert isinstance(result, dict)
    assert "ethics_compliance_score" in result
    assert 1 <= result["ethics_compliance_score"] <= 10
    assert "critical_remarks" in result
    assert "improvement_suggestions" in result

def test_error_handling(agents):
    """Test error handling for invalid inputs"""
    # Test with empty input
    result = agents["R1"].analyze_originality_contribution("", "healthcare")
    assert result.get("error") is True
    assert "Error in analysis" in result.get("summary", "")
    
    # Test with None input
    result = agents["R2"].analyze_impact_significance(None, {"field": "healthcare"})
    assert result.get("error") is True
    assert "Error in analysis" in result.get("summary", "")

def test_output_format_consistency(agents, sample_manuscript):
    """Test that all agents return consistently formatted output"""
    for name, agent in agents.items():
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
        else:  # R7
            result = agent.analyze_consistency(sample_manuscript, "healthcare")
            
        assert isinstance(result, dict)
        assert any(key.endswith('_score') for key in result.keys())
        assert "critical_remarks" in result
        assert "improvement_suggestions" in result
        assert "detailed_feedback" in result
        assert "summary" in result 