#!/usr/bin/env python3
"""
Combine Results

This script combines all individual agent results into a single JSON file.
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


def combine_results(results_dir: str, output_file: str) -> None:
    """Combine all individual agent results into a single JSON file."""
    # Initialize the combined results dictionary
    combined_results = {}
    
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
        
        # Add the agent's results to the combined results
        combined_results[agent_name] = agent_results
    
    # Save the combined results
    save_json_file(combined_results, output_file)


def main():
    """Main function to run the script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Combine individual agent results into a single JSON file')
    parser.add_argument('--results-dir', '-r', type=str,
                        default='/Users/robertjakob/rigorous-1/V5_multi_agent2/results',
                        help='Directory containing individual agent results')
    parser.add_argument('--output', '-o', type=str,
                        default='/Users/robertjakob/rigorous-1/V5_multi_agent2/results/combined_results.json',
                        help='Path to save the combined results')
    
    args = parser.parse_args()
    
    combine_results(args.results_dir, args.output)


if __name__ == "__main__":
    main() 