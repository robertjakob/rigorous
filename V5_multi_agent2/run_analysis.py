import os
import json
from PyPDF2 import PdfReader
from src.reviewer_agents.controller_agent import ControllerAgent
from src.core.config import DEFAULT_MODEL

def process_pdf(pdf_path):
    """Process PDF and extract text."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def main():
    # Process the manuscript
    manuscript_path = "manuscripts/DigitalScale___Paper.pdf"
    manuscript_text = process_pdf(manuscript_path)
    
    # Initialize controller agent
    controller = ControllerAgent(model=DEFAULT_MODEL)
    
    # Run the analysis
    results = controller.run_analysis(manuscript_text)
    
    # Save results
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save individual agent results
    for agent_name, result in results.items():
        output_file = os.path.join(output_dir, f"{agent_name}_results.json")
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
    
    # Save combined results
    combined_output = os.path.join(output_dir, "combined_results.json")
    with open(combined_output, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Analysis complete. Results saved to {output_dir}/")

if __name__ == "__main__":
    main() 