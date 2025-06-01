import run_analysis
import run_quality_control
import run_executive_summary
import json
import os
from datetime import datetime
import pdf_generator
import time





def get_local_manuscript():
    with open('manuscript.json', "r") as f:
        manuscript = json.load(f)
        
    publication_outlet = manuscript['publicationOutlets'] or ''
    review_focus = manuscript['reviewFocus'] or ''
    
    manuscript['context'] = {
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
        
    return manuscript

if __name__ == "__main__":
    
    start_time = time.time()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Get manuscript
    manuscript = get_local_manuscript()
    
    print('manuscript', manuscript)
        
    # Run analysis
    analysis_results = run_analysis.run_analysis(manuscript)    
    manuscript = manuscript.copy() | analysis_results    
    
    # Run quality control
    quality_control_results = run_quality_control.run_quality_control(manuscript)        
    manuscript['quality_control_results'] = quality_control_results
            
    executive_summary_results = run_executive_summary.run_executive_summary(manuscript)  
    manuscript['executive_summary_results'] = executive_summary_results
    
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    manuscript['output_path'] = os.path.join(base_dir, 'reports', f'{current_datetime}_review_report.pdf')   
    
    # Generate PDF
    pdf_generator.generate_pdf(manuscript)
    
    elapsed_time = time.time() - start_time
    elapsed_minutes = elapsed_time / 60
    print(f"Code block executed in {elapsed_minutes:.2f} minutes.")    