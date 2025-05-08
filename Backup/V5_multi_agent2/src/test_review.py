import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.reviewer_agents.rigor.R1_originality_contribution_agent import OriginalityContributionAgent
from src.reviewer_agents.rigor.R2_impact_significance_agent import ImpactSignificanceAgent
from src.reviewer_agents.writing.W1_language_style_agent import LanguageStyleAgent
import json

def main():
    # Sample manuscript for testing
    sample_manuscript = """
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
    """
    
    # Initialize agents with GPT-3.5-turbo
    originality_agent = OriginalityContributionAgent(model="gpt-3.5-turbo")
    impact_agent = ImpactSignificanceAgent(model="gpt-3.5-turbo")
    language_agent = LanguageStyleAgent(model="gpt-3.5-turbo")
    
    # Create results directory if it doesn't exist
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    
    # Get reviews from each agent
    print("\nGetting originality review...")
    originality_review = originality_agent.analyze_originality_contribution(sample_manuscript, "healthcare")
    
    print("\nGetting impact review...")
    impact_review = impact_agent.analyze_impact_significance(sample_manuscript, {"field": "healthcare"})
    
    print("\nGetting language review...")
    language_review = language_agent.analyze_language_style(sample_manuscript, "healthcare")
    
    # Save individual reviews
    reviews = {
        "originality_review": originality_review,
        "impact_review": impact_review,
        "language_review": language_review
    }
    
    # Save to file
    output_file = os.path.join(results_dir, "test_reviews.json")
    with open(output_file, 'w') as f:
        json.dump(reviews, f, indent=2)
    
    print(f"\nReviews saved to: {output_file}")
    
    # Print summary of reviews
    print("\n=== Review Summary ===")
    print(f"Originality Score: {originality_review.get('originality_contribution_score', 'N/A')}")
    print(f"Impact Score: {impact_review.get('impact_significance_score', 'N/A')}")
    print(f"Language Score: {language_review.get('language_style_score', 'N/A')}")

if __name__ == "__main__":
    main() 