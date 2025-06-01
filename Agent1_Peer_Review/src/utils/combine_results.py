#!/usr/bin/env python3
"""
Utility functions for combining results from different agents.

Input files:
- section_results.json: Results from section agents (S1-S10)
- rigor_results.json: Results from rigor agents (R1-R7)
- writing_results.json: Results from writing agents (W1-W7)
"""

import json
import os
import glob
from typing import Dict, Any


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load and parse a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return {}


def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """Save data to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        print(f"Results successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")


def combine_results_by_category(results_dir: str, output_dir: str) -> None:
    """Combine individual agent results into three category-specific JSON files."""
    # Initialize category-specific result dictionaries
    section_results = {}
    rigor_results = {}
    writing_results = {}
    
    # Get all JSON files in the results directory
    json_files = glob.glob(os.path.join(results_dir, '*_results.json'))
    
    # Process each JSON file
    for file_path in json_files:
        # Extract agent name from filename (e.g., 'S1_results.json' -> 'S1')
        agent_name = os.path.basename(file_path).split('_')[0]
        
        # Skip files that are not agent results
        if agent_name in ['critical_remarks', 'score', 'detailed_feedback', 'summary', 'improvement_suggestions', 'combined']:
            continue
        
        # Load the agent's results
        agent_results = load_json_file(file_path)
        
        # Skip if the file is empty or contains an error
        if not agent_results or (isinstance(agent_results, dict) and 'error' in agent_results):
            print(f"Skipping {file_path} due to error or empty file")
            continue
        
        # Categorize and add the agent's results
        if agent_name.startswith('S'):
            section_results[agent_name] = agent_results
        elif agent_name.startswith('R'):
            rigor_results[agent_name] = agent_results
        elif agent_name.startswith('W'):
            writing_results[agent_name] = agent_results
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the categorized results
    save_json_file(section_results, os.path.join(output_dir, 'section_results.json'))
    save_json_file(rigor_results, os.path.join(output_dir, 'rigor_results.json'))
    save_json_file(writing_results, os.path.join(output_dir, 'writing_results.json'))
    
    return {"section_results": section_results, "rigor_results": rigor_results, "writing_results": writing_results}


def main():
    """Main function to run the script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Combine individual agent results into category-specific JSON files')
    parser.add_argument('--results-dir', '-r', type=str,
                        default='results',
                        help='Directory containing individual agent results')
    parser.add_argument('--output-dir', '-o', type=str,
                        default='results',
                        help='Directory to save the combined results')
    
    args = parser.parse_args()
    
    combine_results_by_category(args.results_dir, args.output_dir)


if __name__ == "__main__":
    main() 