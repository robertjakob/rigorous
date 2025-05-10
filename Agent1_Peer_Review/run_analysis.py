import os
import json
import glob
from src.utils.pdf_parser import PDFParser
from src.reviewer_agents.controller_agent import ControllerAgent
from src.core.config import DEFAULT_MODEL
from src.utils.combine_results import combine_results_by_category

def process_pdf(pdf_path):
    """Process PDF and extract text, figures, and tables."""
    parser = PDFParser(pdf_path)
    
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

def find_pdf_in_directory(directory):
    """Find the first PDF file in the specified directory."""
    pdf_files = glob.glob(os.path.join(directory, "*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {directory}")
    return pdf_files[0]  # Return the first PDF file found

def main():
    # Find PDF in manuscripts directory
    manuscripts_dir = "manuscripts"
    try:
        manuscript_path = find_pdf_in_directory(manuscripts_dir)
        print(f"Found PDF: {os.path.basename(manuscript_path)}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    
    # Process the manuscript
    manuscript_data = process_pdf(manuscript_path)
    
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
    combine_results_by_category(output_dir, output_dir)
    
    print(f"Analysis complete. Results saved to {output_dir}/")
    print("Created category-specific files:")
    print("- section_results.json (S1-S10)")
    print("- rigor_results.json (R1-R7)")
    print("- writing_results.json (W1-W7)")

if __name__ == "__main__":
    main() 