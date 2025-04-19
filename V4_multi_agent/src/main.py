#!/usr/bin/env python3
"""
Main script for the peer review tool.
"""

import os
import json
import argparse
from pdf_parser import PDFParser
from editor_agent import EditorAgent
from specialized_agent import SpecializedReviewAgent
from coordinator_agent import CoordinatorAgent
from review_criteria_parser import ReviewCriteriaParser

def main():
    """Main function to run the peer review tool."""
    parser = argparse.ArgumentParser(description='Multi-agent peer review system for scientific manuscripts')
    parser.add_argument('--manuscript', type=str, required=True, help='Path to the manuscript PDF')
    parser.add_argument('--criteria', type=str, required=True, help='Path to the review criteria file')
    parser.add_argument('--output', type=str, required=True, help='Path to save the review results')
    
    args = parser.parse_args()
    
    try:
        print(f"Starting multi-agent peer review for: {args.manuscript}")
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Parse manuscript
        pdf_parser = PDFParser()
        manuscript_text = pdf_parser.extract_text(args.manuscript)
        
        # Parse review criteria
        criteria_parser = ReviewCriteriaParser()
        if not criteria_parser.validate_criteria(args.criteria):
            raise Exception("Invalid review criteria file format")
        
        # Initialize editor agent
        print("Initializing editor agent...")
        editor = EditorAgent()
        
        # Generate review plan
        print("Analyzing paper requirements...")
        review_plan = editor.generate_review_plan(manuscript_text)
        if "error" in review_plan:
            raise Exception(f"Failed to generate review plan: {review_plan['error']}")
        
        # Save review plan
        review_plan_path = os.path.join(output_dir, "review_plan.json")
        with open(review_plan_path, 'w') as f:
            json.dump(review_plan, f, indent=2)
        print(f"Review plan saved to: {review_plan_path}")
        
        # Create specialized review agents
        print("Creating specialized review team...")
        specialized_agents = {}
        
        # First, initialize core reviewers
        print("\nInitializing core reviewers:")
        for agent_config in review_plan["review_team"]["agents"]:
            agent_id = agent_config["id"]
            agent_role = agent_config["role"]
            
            # Check if this is a core reviewer
            is_core = agent_id in ["language_reviewer", "methodology_reviewer", "ethics_reviewer"]
            
            if is_core:
                print(f"  - {agent_role} (Core Reviewer)")
            else:
                print(f"  - {agent_role} (Domain-Specific Reviewer)")
                
            # Get agent-specific criteria
            agent_criteria = criteria_parser.get_agent_criteria(args.criteria, agent_role)
            
            # Update agent config with specific criteria
            agent_config["review_criteria"] = agent_criteria["criteria"]
            agent_config["criteria_description"] = agent_criteria["description"]
            
            specialized_agents[agent_id] = SpecializedReviewAgent(agent_config)
        
        # Perform specialized reviews
        print("\nPerforming specialized reviews...")
        specialized_reviews = {}
        
        # First, run core reviews
        print("\nRunning core reviews:")
        for agent_id, agent in specialized_agents.items():
            is_core = agent_id in ["language_reviewer", "methodology_reviewer", "ethics_reviewer"]
            
            if is_core:
                print(f"  - Reviewing with {agent.role} (Core Reviewer)...")
            else:
                print(f"  - Reviewing with {agent.role} (Domain-Specific Reviewer)...")
                
            review = agent.perform_review(manuscript_text)
            if "error" in review:
                print(f"    Warning: {agent.role} encountered an error: {review['error']}")
            specialized_reviews[agent_id] = review
            
            # Save individual agent review
            agent_review_path = os.path.join(output_dir, f"{agent_id}_review.json")
            with open(agent_review_path, 'w') as f:
                json.dump(review, f, indent=2)
            print(f"    Review saved to: {agent_review_path}")
        
        # Save all specialized reviews
        specialized_reviews_path = os.path.join(output_dir, "specialized_reviews.json")
        with open(specialized_reviews_path, 'w') as f:
            json.dump(specialized_reviews, f, indent=2)
        print(f"\nAll specialized reviews saved to: {specialized_reviews_path}")
        
        # Initialize coordinator
        print("\nInitializing coordinator agent...")
        coordinator = CoordinatorAgent()
        
        # Synthesize reviews
        print("Synthesizing reviews...")
        synthesis = coordinator.synthesize_reviews(specialized_reviews, manuscript_text)
        if "error" in synthesis:
            raise Exception(f"Failed to synthesize reviews: {synthesis['error']}")
        
        # Save synthesis
        synthesis_path = os.path.join(output_dir, "synthesis.json")
        with open(synthesis_path, 'w') as f:
            json.dump(synthesis, f, indent=2)
        print(f"Synthesis saved to: {synthesis_path}")
        
        # Generate final report
        print("Generating final report...")
        final_report = coordinator.generate_final_report(specialized_reviews, synthesis)
        if "error" in final_report:
            raise Exception(f"Failed to generate final report: {final_report['error']}")
        
        # Save final report
        with open(args.output, 'w') as f:
            json.dump(final_report, f, indent=2)
            
        print(f"\nReview completed successfully. Results saved to: {args.output}")
        
    except Exception as e:
        print(f"Error during peer review: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main() 