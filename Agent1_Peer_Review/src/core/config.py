from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4.1-nano")

# Agent configurations
AGENT_CONFIGS = {
    "scientific_rigor": [
        {
            "name": "R1_Methodology_Agent",
            "category": "Scientific Rigor",
            "expertise": ["Research Design", "Methodology", "Experimental Setup"],
            "focus_areas": [
                "Methodology robustness",
                "Experimental design",
                "Control conditions",
                "Sample size justification",
                "Data collection procedures"
            ]
        },
        {
            "name": "R2_Impact_Significance_Agent",
            "category": "Scientific Rigor",
            "expertise": ["Research Impact", "Scientific Significance", "Field Contribution"],
            "focus_areas": [
                "Scientific impact",
                "Field contribution",
                "Practical implications",
                "Future research directions"
            ]
        },
        {
            "name": "R3_Ethics_Compliance_Agent",
            "category": "Scientific Rigor",
            "expertise": ["Research Ethics", "Compliance", "Data Protection"],
            "focus_areas": [
                "Ethical considerations",
                "Conflict of interest",
                "Data privacy",
                "Informed consent",
                "Research integrity"
            ]
        },
        {
            "name": "R4_Data_Code_Availability_Agent",
            "category": "Scientific Rigor",
            "expertise": ["Data Management", "Code Availability", "Reproducibility"],
            "focus_areas": [
                "Data availability",
                "Code sharing",
                "Documentation",
                "Reproducibility",
                "Access restrictions"
            ]
        },
        {
            "name": "R5_Statistical_Rigor_Agent",
            "category": "Scientific Rigor",
            "expertise": ["Statistical Analysis", "Data Validation", "Statistical Methods"],
            "focus_areas": [
                "Statistical methods",
                "Data validation",
                "Statistical significance",
                "Error analysis",
                "Statistical reporting"
            ]
        },
        {
            "name": "R6_Technical_Accuracy_Agent",
            "category": "Scientific Rigor",
            "expertise": ["Technical Content", "Mathematical Rigor", "Algorithm Analysis"],
            "focus_areas": [
                "Technical accuracy",
                "Mathematical correctness",
                "Algorithm validation",
                "Technical clarity",
                "Implementation details"
            ]
        },
        {
            "name": "R7_Consistency_Agent",
            "category": "Scientific Rigor",
            "expertise": ["Logical Coherence", "Cross-section Analysis", "Consistency Checking"],
            "focus_areas": [
                "Logical coherence",
                "Cross-section consistency",
                "Terminology consistency",
                "Results alignment",
                "Conclusion support"
            ]
        }
    ],
    "writing_presentation": [
        {
            "name": "W1_Language_Style_Agent",
            "category": "Writing and Presentation",
            "expertise": ["Grammar", "Spelling", "Punctuation"],
            "focus_areas": [
                "Grammar correctness",
                "Spelling accuracy",
                "Punctuation usage",
                "Sentence structure",
                "Academic writing conventions"
            ]
        },
        {
            "name": "W2_Narrative_Structure_Agent",
            "category": "Writing and Presentation",
            "expertise": ["Narrative Flow", "Structural Organization", "Logical Progression"],
            "focus_areas": [
                "Narrative coherence",
                "Logical progression",
                "Section transitions",
                "Paragraph organization",
                "Reader engagement"
            ]
        },
        {
            "name": "W3_Clarity_Conciseness_Agent",
            "category": "Writing and Presentation",
            "expertise": ["Language Simplicity", "Jargon Reduction", "Conciseness"],
            "focus_areas": [
                "Language simplicity",
                "Jargon usage",
                "Wordiness",
                "Readability",
                "Information density"
            ]
        },
        {
            "name": "W4_Terminology_Consistency_Agent",
            "category": "Writing and Presentation",
            "expertise": ["Terminology Consistency", "Notation Standards", "Acronym Usage"],
            "focus_areas": [
                "Term usage consistency",
                "Notation consistency",
                "Acronym usage",
                "Variable naming",
                "Definition consistency"
            ]
        }
    ]
}

# Review criteria
REVIEW_CRITERIA = {
    "scientific_rigor": {
        "methodology": {
            "weight": 0.15,
            "criteria": [
                "Research design appropriateness",
                "Methodology robustness",
                "Experimental setup completeness",
                "Control conditions adequacy",
                "Sample size justification"
            ]
        },
        "impact": {
            "weight": 0.15,
            "criteria": [
                "Scientific significance",
                "Field contribution",
                "Practical implications",
                "Future research potential"
            ]
        },
        "ethics": {
            "weight": 0.15,
            "criteria": [
                "Ethical considerations",
                "Conflict of interest disclosure",
                "Data privacy protection",
                "Informed consent procedures",
                "Research integrity"
            ]
        },
        "data_code": {
            "weight": 0.15,
            "criteria": [
                "Data availability",
                "Code sharing",
                "Documentation completeness",
                "Reproducibility",
                "Access restrictions justification"
            ]
        },
        "statistics": {
            "weight": 0.15,
            "criteria": [
                "Statistical methods appropriateness",
                "Data validation",
                "Statistical significance",
                "Error analysis",
                "Statistical reporting"
            ]
        },
        "technical": {
            "weight": 0.15,
            "criteria": [
                "Technical accuracy",
                "Mathematical correctness",
                "Algorithm validation",
                "Technical clarity",
                "Implementation details"
            ]
        },
        "consistency": {
            "weight": 0.10,
            "criteria": [
                "Logical coherence",
                "Cross-section consistency",
                "Terminology consistency",
                "Results alignment",
                "Conclusion support"
            ]
        }
    },
    "writing_presentation": {
        "language_style": {
            "weight": 0.25,
            "criteria": [
                "Grammar correctness",
                "Spelling accuracy",
                "Punctuation usage",
                "Sentence structure",
                "Academic writing conventions"
            ]
        },
        "narrative_structure": {
            "weight": 0.25,
            "criteria": [
                "Narrative coherence",
                "Logical progression",
                "Section transitions",
                "Paragraph organization",
                "Reader engagement"
            ]
        },
        "clarity_conciseness": {
            "weight": 0.25,
            "criteria": [
                "Language simplicity",
                "Jargon usage",
                "Wordiness",
                "Readability",
                "Information density"
            ]
        },
        "terminology_consistency": {
            "weight": 0.25,
            "criteria": [
                "Term usage consistency",
                "Notation consistency",
                "Acronym usage",
                "Variable naming",
                "Definition consistency"
            ]
        }
    }
}

# Controller Agent Configuration
CONTROLLER_CONFIG = {
    "review_steps": [
        "initial_analysis",
        "agent_review_comparison",
        "remark_ranking",
        "report_generation"
    ],
    "output_formats": ["json", "text"],
    "score_range": (1, 5)
}

# PDF Processing Configuration
PDF_PROCESSOR_CONFIG = {
    "supported_formats": ["pdf"],
    "max_pages": 100,
    "image_quality": "high",
    "ocr_enabled": True
}

# File Paths
PATHS = {
    "manuscripts": "manuscripts/",
    "results": "results/",
    "tests": "tests/",
    "logs": "logs/"
}

# Create directories if they don't exist
for path in PATHS.values():
    os.makedirs(path, exist_ok=True) 