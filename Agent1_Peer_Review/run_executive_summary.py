#!/usr/bin/env python3
"""
Script to run the Executive Summary Agent and generate a high-level summary of the review results.
"""

import os
import json
from src.reviewer_agents.executive_summary_agent import ExecutiveSummaryAgent

def get_local_manuscript():
    with open('manuscript.json', "r") as f:
        manuscript = json.load(f)
        
    publication_outlet = manuscript['publicationOutlets'] or ''
    review_focus = manuscript['reviewFocus'] or ''
    
    manuscript['context'] = {
        "target_publication_outlets": {
            "label": "Target Publication Outlets (optional but recommended)",
            "description": "This helps us tailor the review to your target venue's requirements.",
            "placeholder": "e.g., Nature Medicine, Science, or specific conferences like NeurIPS 2024",
            "user_input": publication_outlet
        },
        "review_focus_areas": {
            "label": "Review Focus Areas (optional but recommended)",
            "description": "Specify any particular aspects you'd like the AI peer reviewers to focus on.",
            "placeholder": "e.g., statistical analysis, methodology, experimental design, motivation, or specific aspects you want reviewers to focus on",
            "user_input": review_focus
        }
    }
        
    return manuscript

def run_executive_summary(inputs):
    # Initialize the Executive Summary Agent
    agent = ExecutiveSummaryAgent()   
    
    # Define output path
    output_path = 'results/executive_summary.json'
    
    try:
        # Process the inputs and generate the executive summary
        results = agent.process(inputs)
        
        # Save the results
        agent.save_results(results, output_path)
        
        print("\nExecutive Summary Generation Complete!", f"Results saved to: {output_path}")
        
        # Print the scores
        print("\nOverall Scores:")
        print(f"Section Score: {results['scores']['section_score']:.1f}/5")
        print(f"Rigor Score: {results['scores']['rigor_score']:.1f}/5")
        print(f"Writing Score: {results['scores']['writing_score']:.1f}/5")
        print(f"Final Score: {results['scores']['final_score']:.1f}/5")
        
        return results
        
    except Exception as e:
        print(f"Error generating executive summary: {str(e)}")
        raise

if __name__ == "__main__": 
    
    manuscript = get_local_manuscript()
    
    with open('./results/quality_control_results.json', "r") as f:
        quality_control_results_json = json.load(f)
        
    manuscript['quality_control_results'] = quality_control_results_json  
    
    run_executive_summary(manuscript) 