import argparse
import json
import os
from typing import Dict, List
from peer_review_checker import PeerReviewChecker

def read_review_criteria(criteria_path: str) -> Dict[str, str]:
    """
    Read review criteria from a JSON file.
    
    Args:
        criteria_path (str): Path to the criteria file
        
    Returns:
        Dict[str, str]: Dictionary of criteria and their descriptions
    """
    with open(criteria_path, 'r') as f:
        return json.load(f)

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

def review_manuscript(checker: PeerReviewChecker, pdf_path: str, criteria: Dict[str, str], output_dir: str) -> None:
    """
    Review a single manuscript and save results to a file.
    
    Args:
        checker (PeerReviewChecker): The peer review checker instance
        pdf_path (str): Path to the PDF file
        criteria (Dict[str, str]): Review criteria
        output_dir (str): Directory to save the results
    """
    try:
        # Get the base filename without extension
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        # Review manuscript
        results = checker.review_manuscript(pdf_path, criteria)
        
        # Format results
        formatted_results = checker.format_results(results)
        
        # Save results to file
        output_file = os.path.join(output_dir, f"{base_name}_review.txt")
        with open(output_file, 'w') as f:
            f.write(formatted_results)
            
        print(f"Review completed for {base_name}")
        print(f"Results saved to: {output_file}\n")
        
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}\n")

def main():
    parser = argparse.ArgumentParser(description='Academic Manuscript Peer Review Tool')
    parser.add_argument('--manuscripts-dir', default='manuscripts', 
                      help='Directory containing PDF manuscripts (default: manuscripts)')
    parser.add_argument('--criteria', required=True, help='Path to the review criteria JSON file')
    parser.add_argument('--output-dir', default='analysis_results',
                      help='Directory to save review results (default: analysis_results)')
    parser.add_argument('--api-key', help='OpenAI API key (optional if set in environment)')
    
    args = parser.parse_args()
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Read review criteria
        criteria = read_review_criteria(args.criteria)
        
        # Get PDF files
        pdf_files = get_pdf_files(args.manuscripts_dir)
        
        if not pdf_files:
            print(f"No PDF files found in {args.manuscripts_dir}")
            return 1
            
        print(f"Found {len(pdf_files)} PDF files to review")
        
        # Initialize checker
        checker = PeerReviewChecker(api_key=args.api_key)
        
        # Process each PDF
        for pdf_path in pdf_files:
            review_manuscript(checker, pdf_path, criteria, args.output_dir)
            
        print("Review process complete!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == '__main__':
    exit(main()) 