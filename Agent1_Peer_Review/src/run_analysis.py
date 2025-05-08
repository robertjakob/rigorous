#!/usr/bin/env python3
"""
Run Analysis

This script runs the manuscript analysis using all agents and saves the results
in three category-specific JSON files:
- section_results.json: Results from section agents (S1-S10)
- rigor_results.json: Results from rigor agents (R1-R7)
- writing_results.json: Results from writing agents (W1-W8)
"""

import argparse
import json
import os
from typing import Dict, Any

from reviewer_agents.controller_agent import ControllerAgent
from utils.combine_results import combine_results_by_category


def load_manuscript(file_path: str) -> str:
    """Load the manuscript text from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading manuscript: {e}")
        return ""


def save_results(results: Dict[str, Any], output_dir: str) -> None:
    """Save the analysis results to category-specific JSON files."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save individual agent results first
        for agent_name, agent_results in results.items():
            agent_file = os.path.join(output_dir, f"{agent_name}_results.json")
            with open(agent_file, 'w', encoding='utf-8') as file:
                json.dump(agent_results, file, indent=2)
        
        # Combine results by category
        combine_results_by_category(output_dir, output_dir)
        
        print(f"Results successfully saved to {output_dir}")
    except Exception as e:
        print(f"Error saving results: {e}")


def main():
    """Main function to run the analysis."""
    parser = argparse.ArgumentParser(description='Run manuscript analysis')
    parser.add_argument('--input', '-i', type=str, 
                        default='manuscripts/manuscript.txt',
                        help='Path to the input manuscript file')
    parser.add_argument('--results-dir', '-r', type=str,
                        default='results',
                        help='Directory to save the analysis results')
    parser.add_argument('--model', '-m', type=str,
                        default='gpt-4.1-nano',
                        help='Model to use for analysis')
    
    args = parser.parse_args()
    
    # Load the manuscript
    manuscript_text = load_manuscript(args.input)
    if not manuscript_text:
        print("Failed to load manuscript. Exiting.")
        return
    
    # Initialize the controller agent
    controller = ControllerAgent(model=args.model)
    
    # Run the analysis
    print("Running analysis...")
    results = controller.run_analysis(manuscript_text)
    
    # Save the results
    save_results(results, args.results_dir)
    
    print(f"Analysis complete. Results saved to {args.results_dir}")


if __name__ == "__main__":
    main() 