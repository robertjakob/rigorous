import os
import json
import time
from src.reviewer_agents.quality import QualityControlAgent

def wait_for_files(file_paths: list, timeout: int = 300, check_interval: int = 5) -> bool:
    """
    Wait for files to be created and not be empty.
    Returns True if all files exist and are not empty, False if timeout is reached.
    """
    # Check if files exist and are not empty
    for file_path in file_paths:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return False
    return True

def main():
    # Define paths according to the implementation plan
    base_dir = os.path.dirname(os.path.abspath(__file__))
    context_path = os.path.join(base_dir, 'context', 'context.json')
    
    # Define result file paths
    manuscript_dir = os.path.join(base_dir, 'manuscripts')
    results_dir = os.path.join(base_dir, 'results')
    
    # Define result file paths
    rigor_results_path = os.path.join(results_dir, 'rigor_results.json')
    section_results_path = os.path.join(results_dir, 'section_results.json')
    writing_results_path = os.path.join(results_dir, 'writing_results.json')
    
    # Check if files exist
    print("Checking for required files...")
    if not wait_for_files([rigor_results_path, section_results_path, writing_results_path]):
        raise FileNotFoundError("Required result files not found")
    print("All required files found")
    
    # Find the most recent manuscript
    manuscript_files = [f for f in os.listdir(manuscript_dir) if f.endswith('.pdf')]
    if not manuscript_files:
        raise FileNotFoundError("No PDF manuscripts found in the manuscripts directory")
    manuscript_path = os.path.join(manuscript_dir, manuscript_files[0])
    
    # Initialize the quality control agent
    agent = QualityControlAgent()
    
    # Prepare inputs
    inputs = {
        'manuscript_path': manuscript_path,
        'context_path': context_path,
        'rigor_results_path': rigor_results_path,
        'section_results_path': section_results_path,
        'writing_results_path': writing_results_path
    }
    
    # Run the quality control analysis
    results = agent.process(inputs)
    
    # Save the results
    output_path = os.path.join(results_dir, 'quality_control_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Quality control analysis completed. Results saved to: {output_path}")

if __name__ == '__main__':
    main() 