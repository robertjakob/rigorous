import pytest
import json
from src.reviewer_agents.writing.W1_language_style_agent import LanguageStyleAgent
from src.reviewer_agents.writing.W2_narrative_structure_agent import NarrativeStructureAgent
from src.reviewer_agents.writing.W3_clarity_conciseness_agent import ClarityConciseAgent
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
    """

@pytest.fixture
def agents():
    return {
        "W1": LanguageStyleAgent(model="gpt-3.5-turbo"),
        "W2": NarrativeStructureAgent(model="gpt-3.5-turbo"),
        "W3": ClarityConciseAgent(model="gpt-3.5-turbo"),
        "W4": TerminologyConsistencyAgent(model="gpt-3.5-turbo")
    }

def test_agent_initialization(agents):
    """Test that all agents initialize correctly with expected attributes"""
    for name, agent in agents.items():
        assert agent.model == "gpt-3.5-turbo"
        assert agent.name == f"{name}_Agent"
        assert agent.category == "Writing Quality"

def test_language_style_analysis(agents, sample_manuscript):
    """Test W1 agent's analysis functionality"""
    result = agents["W1"].analyze_language_style(sample_manuscript)
    assert isinstance(result, dict)
    assert "language_style_score" in result
    assert isinstance(result["language_style_score"], (int, float))
    assert 1 <= result["language_style_score"] <= 5
    assert "critical_remarks" in result
    assert "improvement_suggestions" in result
    assert "detailed_feedback" in result
    assert "summary" in result

def test_narrative_structure_analysis(agents, sample_manuscript):
    """Test W2 agent's analysis functionality"""
    result = agents["W2"].analyze_narrative_structure(sample_manuscript)
    assert isinstance(result, dict)
    assert "narrative_structure_score" in result
    assert 1 <= result["narrative_structure_score"] <= 5
    assert "critical_remarks" in result
    assert "improvement_suggestions" in result

def test_clarity_conciseness_analysis(agents, sample_manuscript):
    """Test W3 agent's analysis functionality"""
    result = agents["W3"].analyze_clarity_conciseness(sample_manuscript)
    assert isinstance(result, dict)
    assert "clarity_conciseness_score" in result
    assert 1 <= result["clarity_conciseness_score"] <= 5
    assert "critical_remarks" in result
    assert "improvement_suggestions" in result

def test_terminology_consistency_analysis(agents, sample_manuscript):
    """Test W4 agent's analysis functionality"""
    result = agents["W4"].analyze_terminology_consistency(sample_manuscript)
    assert isinstance(result, dict)
    assert "terminology_consistency_score" in result
    assert 1 <= result["terminology_consistency_score"] <= 5
    assert "critical_remarks" in result
    assert "improvement_suggestions" in result

def test_error_handling(agents):
    """Test error handling for invalid inputs"""
    with pytest.raises(ValueError):
        agents["W1"].analyze_language_style("")
    
    with pytest.raises(ValueError):
        agents["W2"].analyze_narrative_structure(None)

def test_output_format_consistency(agents, sample_manuscript):
    """Test that all agents return consistently formatted output"""
    for name, agent in agents.items():
        if name == "W1":
            result = agent.analyze_language_style(sample_manuscript)
        elif name == "W2":
            result = agent.analyze_narrative_structure(sample_manuscript)
        elif name == "W3":
            result = agent.analyze_clarity_conciseness(sample_manuscript)
        else:  # W4
            result = agent.analyze_terminology_consistency(sample_manuscript)
            
        assert isinstance(result, dict)
        assert any(key.endswith('_score') for key in result.keys())
        assert "critical_remarks" in result
        assert "improvement_suggestions" in result
        assert "detailed_feedback" in result
        assert "summary" in result

def test_cross_agent_consistency(agents, sample_manuscript):
    """Test that scores and feedback are consistent across agents"""
    results = {}
    for name, agent in agents.items():
        if name == "W1":
            results[name] = agent.analyze_language_style(sample_manuscript)
        elif name == "W2":
            results[name] = agent.analyze_narrative_structure(sample_manuscript)
        elif name == "W3":
            results[name] = agent.analyze_clarity_conciseness(sample_manuscript)
        else:  # W4
            results[name] = agent.analyze_terminology_consistency(sample_manuscript)
    
    # Check that no agent gives wildly different scores
    scores = [list(result.values())[0] for result in results.values()]
    max_score_diff = max(scores) - min(scores)
    assert max_score_diff <= 3  # No more than 3 points difference between highest and lowest scores 