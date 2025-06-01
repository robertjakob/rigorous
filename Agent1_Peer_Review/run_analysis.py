import os
import json
import glob
from src.utils.pdf_parser import PDFParser
from src.reviewer_agents.controller_agent import ControllerAgent
from src.core.config import DEFAULT_MODEL
from src.utils.combine_results import combine_results_by_category
from dotenv import load_dotenv
import pathlib

# Load environment variables
env_path = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


def process_pdf(pdf_url):
    """Process PDF and extract text, figures, and tables."""   

    # Pass to PDFParser  
    parser = PDFParser(pdf_url)
    
    # Extract all components
    text = parser.extract_text()
    metadata = parser.get_metadata()
    images = parser.extract_images()
    tables = parser.extract_tables()
    
    return {
        'text': text,
        'metadata': metadata,
        'images': images,
        'tables': tables
    }

def run_analysis(manuscript):    # Find PDF in manuscripts directory   
    
    # Process the manuscript
    manuscript_data = process_pdf(manuscript['manuscript_src'])   
    
    # Initialize controller agent
    controller = ControllerAgent(model=DEFAULT_MODEL)
    
    # Run the analysis
    results = controller.run_analysis(text=manuscript_data['text'])
    
    # Save results
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save manuscript data for reference
    manuscript_data_file = os.path.join(output_dir, "manuscript_data.json")
    with open(manuscript_data_file, "w") as f:
        # Convert image data to base64 for JSON serialization
        manuscript_json = manuscript_data.copy()
        for img in manuscript_json['images']:
            img['image_data'] = None  # Remove binary image data for JSON
        json.dump(manuscript_json, f, indent=2)
    
    # Save individual agent results
    for agent_name, result in results.items():
        output_file = os.path.join(output_dir, f"{agent_name}_results.json")
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
    
    # Save combined results
    combined_output = os.path.join(output_dir, "combined_results.json")
    with open(combined_output, "w") as f:
        json.dump(results, f, indent=2)
    
    # Combine results into category-specific files
    combined_results = combine_results_by_category(output_dir, output_dir)

    return combined_results

if __name__ == "__main__":   
    
    with open('manuscript.json', "r") as f:
        manuscript = json.load(f)
        
    # Run the analysis
    run_analysis(manuscript)