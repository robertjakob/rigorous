#!/usr/bin/env python3
"""
Example script demonstrating how to use the V4 Multi-Agent Peer Review System.
"""

import os
import sys
import json
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from main import main

def run_example():
    """Run an example peer review."""
    # Example manuscript and output paths
    manuscript_path = "../manuscripts/example_manuscript.pdf"
    criteria_path = "../review_criteria.txt"
    output_path = "../output/example_review.json"
    
    # Run the peer review
    try:
        main([
            "--manuscript", manuscript_path,
            "--criteria", criteria_path,
            "--output", output_path
        ])
        
        # Read and display the results
        with open(output_path, 'r') as f:
            results = json.load(f)
            
        print("\nReview Results Summary:")
        print("------------------------")
        print(f"Overall Recommendation: {results['final_recommendation']['decision']}")
        print("\nKey Strengths:")
        for strength in results['comprehensive_assessment']['key_strengths']:
            print(f"- {strength}")
            
        print("\nPriority Actions:")
        for action in results['action_plan']['priority_actions']:
            print(f"- {action}")
            
    except Exception as e:
        print(f"Error running example: {str(e)}")

if __name__ == "__main__":
    run_example() 