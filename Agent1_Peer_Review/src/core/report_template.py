from typing import Dict, Any, List
import json
from datetime import datetime

class ReportTemplate:
    """Template for generating standardized review reports."""
    
    def __init__(self):
        """Initialize the report template."""
        self.template = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "agent_name": "",
                "category": "",
                "model_used": "",
                "version": "1.0"
            },
            "analysis": {
                "overall_score": 0,
                "critical_remarks": [],
                "improvement_suggestions": [],
                "detailed_feedback": {},
                "summary": ""
            }
        }
    
    def generate_report(self, agent_name: str, category: str, model: str, 
                       analysis_results: Dict[str, Any], output_path: str) -> None:
        """
        Generate a standardized review report.
        
        Args:
            agent_name (str): Name of the agent
            category (str): Category of the agent
            model (str): Model used for analysis
            analysis_results (Dict[str, Any]): Results of the analysis
            output_path (str): Path to save the report
        """
        report = self.template.copy()
        report["metadata"].update({
            "agent_name": agent_name,
            "category": category,
            "model_used": model
        })
        report["analysis"].update(analysis_results)
        
        with open(output_path, 'w') as f:
            f.write(f"Review Report - {agent_name}\n")
            f.write("=" * (len(agent_name) + 13) + "\n\n")
            
            f.write("Metadata\n")
            f.write("-" * 8 + "\n")
            f.write(json.dumps(report["metadata"], indent=2))
            f.write("\n\n")
            
            f.write("Analysis Results\n")
            f.write("-" * 16 + "\n")
            f.write(json.dumps(report["analysis"], indent=2))
            f.write("\n")

    @staticmethod
    def create_template(agent_name: str, section_name: str) -> Dict[str, Any]:
        """Create a standardized report template.
        
        Args:
            agent_name (str): Name of the reviewer agent
            section_name (str): Name of the section being reviewed
            
        Returns:
            Dict[str, Any]: Standardized report template
        """
        return {
            "agent_name": agent_name,
            "section_name": section_name,
            "timestamp": datetime.now().isoformat(),
            "score": None,  # 1-5 score
            "remarks": [],  # List of issues, questions, or observations
            "concrete_suggestions": [],  # Actionable steps for each remark
            "automated_suggestions": [],  # AI-generated improvements
            "section_specific_analysis": {}  # Additional section-specific analysis
        }
    
    @staticmethod
    def save_report(report: Dict[str, Any], output_dir: str) -> str:
        """Save the report to a text file.
        
        Args:
            report (Dict[str, Any]): The report to save
            output_dir (str): Directory to save the report in
            
        Returns:
            str: Path to the saved report file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{report['agent_name'].lower().replace(' ', '_')}_{timestamp}.txt"
        filepath = f"{output_dir}/{filename}"
        
        with open(filepath, 'w') as f:
            f.write(f"Review Report - {report['agent_name']}\n")
            f.write(f"Section: {report['section_name']}\n")
            f.write(f"Timestamp: {report['timestamp']}\n\n")
            
            f.write(f"Score: {report['score']}/5\n\n")
            
            f.write("Remarks:\n")
            for remark in report['remarks']:
                f.write(f"- {remark}\n")
            f.write("\n")
            
            f.write("Concrete Suggestions:\n")
            for suggestion in report['concrete_suggestions']:
                f.write(f"- {suggestion}\n")
            f.write("\n")
            
            f.write("Automated Suggestions:\n")
            for suggestion in report['automated_suggestions']:
                f.write(f"- {suggestion}\n")
            f.write("\n")
            
            if report['section_specific_analysis']:
                f.write("Section-Specific Analysis:\n")
                f.write(json.dumps(report['section_specific_analysis'], indent=2))
        
        return filepath 