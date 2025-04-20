from editor_agent import EditorAgent
import json
import os

def main():
    # Initialize the editor agent with explicit configuration for the cheaper model
    model_config = {
        "default": "gpt-3.5-turbo",  # Cheaper model for testing
        "production": "gpt-4-turbo-preview",  # More expensive model (not used in testing)
        "current": "default"  # Always use the cheaper model for testing
    }
    
    editor = EditorAgent(model_config)
    print(f"\nUsing model: {editor.get_current_model()} (Testing Mode)")
    
    # Sample paper content (short version for testing)
    sample_paper = """
    Title: A Novel Approach to Machine Learning in Healthcare
    
    Abstract:
    This paper presents a new machine learning framework for healthcare applications,
    focusing on improved patient outcome prediction. We demonstrate significant
    improvements over existing methods in terms of accuracy and interpretability.
    
    Introduction:
    Machine learning in healthcare has seen rapid development in recent years.
    However, current approaches often lack interpretability and fail to consider
    the unique challenges of medical data. Our work addresses these limitations
    through a novel architecture that combines deep learning with domain-specific
    constraints.
    
    Related Work:
    Previous approaches (Smith et al., 2020; Jones et al., 2021) have focused
    primarily on prediction accuracy, often sacrificing interpretability. Recent
    work by Brown et al. (2022) attempted to address this trade-off but faced
    limitations in handling missing data.
    
    Methods:
    We propose a new neural network architecture that incorporates medical domain
    knowledge through constrained optimization. Our approach uses a combination of
    attention mechanisms and traditional statistical methods to ensure both
    accuracy and interpretability.
    
    Results:
    Experimental results on three large-scale medical datasets show that our
    method achieves a 15% improvement in prediction accuracy while maintaining
    full interpretability. We also demonstrate superior handling of missing data
    compared to existing approaches.
    
    Discussion:
    Our results suggest that the proposed framework successfully addresses the
    limitations of current approaches. The improved accuracy and interpretability
    make it particularly suitable for clinical applications.
    """
    
    # Generate review plan
    print("\nGenerating review plan...")
    result = editor.generate_review_plan(sample_paper)
    
    # Debug: Print review plan structure
    print("\nReview plan structure:")
    print(json.dumps(result, indent=2))
    
    # Collect feedback from all specialized reviewers
    print("\nCollecting specialized reviewer feedback...")
    specialized_feedback = {}
    for agent in editor.core_reviewers:
        agent_feedback = editor.get_agent_feedback(agent['id'], sample_paper)
        specialized_feedback[agent['id']] = agent_feedback
        print(f"Collected feedback from {agent['role']}")
    
    # Add specialized feedback to results
    result['specialized_reviewer_feedback'] = specialized_feedback
    
    # Create results directory if it doesn't exist
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Save complete results to JSON file
    results_file = os.path.join(results_dir, 'review_results.json')
    with open(results_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\nComplete results saved to: {results_file}")
    
    # Print key parts of the result in a structured way
    print("\n=== Paper Analysis ===")
    print(json.dumps(result["review_plan"]["paper_analysis"], indent=2))
    
    print("\n=== Key Scientists Identified ===")
    for scientist in result["review_plan"]["key_scientists"]:
        print(f"\nScientist: {scientist['name']}")
        print(f"Research Focus: {scientist['research_focus']}")
        print(f"Review Style: {scientist['review_style']}")
    
    print("\n=== Executive Summary ===")
    print(json.dumps(result["final_report"]["executive_summary"], indent=2))
    
    print("\n=== Thematic Analysis ===")
    print(json.dumps(result["final_report"]["thematic_analysis"], indent=2))
    
    print("\n=== Final Assessment ===")
    print(json.dumps(result["final_report"]["final_assessment"], indent=2))

if __name__ == "__main__":
    main() 