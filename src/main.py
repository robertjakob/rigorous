import argparse
import json
import os
from typing import List
from requirements_checker import RequirementsChecker

def read_requirements(requirements_path: str) -> List[str]:
    """
    Read requirements from a text file.
    
    Args:
        requirements_path (str): Path to the requirements file
        
    Returns:
        List[str]: List of requirements
    """
    with open(requirements_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def get_pdf_files(directory: str) -> List[str]:
    """
    Get all PDF files from a directory.
    
    Args:
        directory (str): Path to the directory
        
    Returns:
        List[str]: List of PDF file paths
    """
    pdf_files = []
    for file in os.listdir(directory):
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(directory, file))
    return pdf_files

def analyze_manuscript(checker: RequirementsChecker, pdf_path: str, requirements: List[str], output_dir: str) -> None:
    """
    Analyze a single manuscript and save results to a file.
    
    Args:
        checker (RequirementsChecker): The requirements checker instance
        pdf_path (str): Path to the PDF file
        requirements (List[str]): List of requirements to check
        output_dir (str): Directory to save the results
    """
    try:
        # Get the base filename without extension
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        # Analyze manuscript
        results = checker.analyze_manuscript(pdf_path, requirements)
        
        # Format results
        formatted_results = checker.format_results(results)
        
        # Save results to file
        output_file = os.path.join(output_dir, f"{base_name}_analysis.txt")
        with open(output_file, 'w') as f:
            f.write(formatted_results)
            
        print(f"Analysis completed for {base_name}")
        print(f"Results saved to: {output_file}\n")
        
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}\n")

def main():
    parser = argparse.ArgumentParser(description='Manuscript Requirements Checker')
    parser.add_argument('--manuscripts-dir', default='manuscripts', 
                      help='Directory containing PDF manuscripts (default: manuscripts)')
    parser.add_argument('--requirements', required=True, help='Path to the requirements text file')
    parser.add_argument('--output-dir', default='analysis_results',
                      help='Directory to save analysis results (default: analysis_results)')
    parser.add_argument('--api-key', help='OpenAI API key (optional if set in environment)')
    
    args = parser.parse_args()
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Read requirements
        requirements = read_requirements(args.requirements)
        
        # Get PDF files
        pdf_files = get_pdf_files(args.manuscripts_dir)
        
        if not pdf_files:
            print(f"No PDF files found in {args.manuscripts_dir}")
            return 1
            
        print(f"Found {len(pdf_files)} PDF files to analyze")
        
        # Initialize checker
        checker = RequirementsChecker(api_key=args.api_key)
        
        # Process each PDF
        for pdf_path in pdf_files:
            analyze_manuscript(checker, pdf_path, requirements, args.output_dir)
            
        print("Analysis complete!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == '__main__':
    exit(main()) 