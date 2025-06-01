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

def run_quality_control(inputs):   
    
    # Initialize the quality control agent
    agent = QualityControlAgent()
    
    # Run the quality control analysis
    results = agent.process(inputs)
    
    # Save the results
    output_path = os.path.join('./results/', 'quality_control_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Quality control analysis completed. Results saved to: {output_path}")   
    
    return results


def create_context_json(manuscript):
    
    publication_outlet = manuscript['publicationOutlets'] or ''
    review_focus = manuscript['reviewFocus'] or ''
    
    return {
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

if __name__ == '__main__':
    
    print("Checking for required files...")
    for f in map(lambda x: os.path.join('./results', x), ['rigor_results.json', 'section_results.json', 'writing_results.json']):
        if not os.path.exists(f):
            raise FileNotFoundError(f"Required result file not found: {f}")          
    
    with open('manuscript.json', "r") as f:
        manuscript = json.load(f)
        
    context_json = create_context_json(manuscript)
        
    with open('./results/rigor_results.json', "r") as f:
        rigor_results_json = json.load(f)
        
    with open('./results/section_results.json', "r") as f:
        section_results_json = json.load(f)
        
    with open('./results/writing_results.json', "r") as f:
        writing_results_json = json.load(f)      
    
    inputs = {
        'manuscript_src': './manuscripts/manuscript.pdf',        
        'context': context_json,
        'rigor_results': rigor_results_json,
        'section_results': section_results_json,
        'writing_results': writing_results_json
    } 
    
    run_quality_control(inputs)