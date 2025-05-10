#!/usr/bin/env python3
"""
Script to run the Executive Summary Agent and generate a high-level summary of the review results.
"""

import os
import json
from src.reviewer_agents.executive_summary_agent import ExecutiveSummaryAgent

def main():
    # Initialize the Executive Summary Agent
    agent = ExecutiveSummaryAgent()
    
    # Define input paths
    inputs = {
        'manuscript_path': 'manuscripts/Systematic Review.pdf',
        'context_path': 'context/context.json',
        'quality_control_results_path': 'results/quality_control_results.json'
    }
    
    # Define output path
    output_path = 'results/executive_summary.json'
    
    try:
        # Process the inputs and generate the executive summary
        results = agent.process(inputs)
        
        # Save the results
        agent.save_results(results, output_path)
        
        print("\nExecutive Summary Generation Complete!")
        print(f"Results saved to: {output_path}")
        
        # Print the scores
        print("\nOverall Scores:")
        print(f"Section Score: {results['scores']['section_score']:.1f}/5")
        print(f"Rigor Score: {results['scores']['rigor_score']:.1f}/5")
        print(f"Writing Score: {results['scores']['writing_score']:.1f}/5")
        print(f"Final Score: {results['scores']['final_score']:.1f}/5")
        
    except Exception as e:
        print(f"Error generating executive summary: {str(e)}")
        raise

if __name__ == "__main__":
    main() 