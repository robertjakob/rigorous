PDF creation implementation

We got the following JSON inputs which we now want to turn in a comprehensive and professionally looking pdf report (please make sure to comprehend their content before continuing)

input 1:
/Users/robertjakob/rigorous-6/Agent1_Peer_Review/results/executive_summary.json

Includes manuscript Title, Executive Summary, Combined Scores

input 2
- /Users/robertjakob/rigorous-6/Agent1_Peer_Review/results/quality_control_results.json

Includes detailed AI peer review feedback


What the PDF report could as folowed and include the following information


Page 1 - Cover Page
- Company Name: The Rigorous Company (maybe in header?)
- Title: Rigorous AI Peer Review Report 
- Subtitle: For the manuscript titled... (can be extracted from input 1)
- Date and time of Review (when this report was created)
- Overall Scores from executive_summary.json:
  - Section Score: 3.3/5
  - Rigor Score: 3.1/5
  - Writing Score: 3.3/5
  - Final Score: 3.2/5
- Thank you note and request for feedback:

Thank you for using the Rigorous AI Peer Reviewer!
We're dedicated to providing actionable, high-quality feedback that accelerates your revision process and boosts your chances of publication. To help us improve the system, please consider completing our short feedback survey. Your input directly contributes to making this tool more useful, accurate, and impactful for the research community. All responses are confidential and sincerely appreciated.

Feedback Link: https://docs.google.com/forms/d/1EhQvw-HdGRqfL01jZaayoaiTWLSydZTI4V0lJSvNpds/edit

- Important Note: "Like real peer reviews, this AI-generated feedback may occasionally include hallucinations, overconfident statements, vague suggestions, or simply a flase statement. Still, we hope you find it insightful and helpful in improving your manuscript for publication."

- A graphical illustration of the high level scores (can be extracted from input 1). We could use a star system Score: ⭐️⭐️⭐️⭐️ (4/5)


Page 2 - Executive Summary (1 page)
- The three-paragraph executive summary from executive_summary.json
- 3 Radar charts showing scores of subcategories (Section Scores: S1-S10, Rigorous Scores: R1-R7, Writing Scores: W1-W7, which can be extracted from input 2). Ideally these can be fitted next to each other.

- Detailed Section Analyses organized as follows:

Section-Specific Assessment (S1–S10):
- S1 – Title and Keywords
- S2 – Abstract
- S3 – Introduction
- S4 – Literature Review
- S5 – Methodology
- S6 – Results
- S7 – Discussion
- S8 – Conclusion
- S9 – References
- S10 – Supplementary Materials

Rigorous Assessment (R1–R7):
- R1 – Originality and Contribution
- R2 – Impact and Significance
- R3 – Ethics and Compliance
- R4 – Data and Code Availability
- R5 – Statistical Rigor
- R6 – Technical Accuracy
- R7 – Consistency

Writing Assessment (W1–W7):
- W1 – Language and Style
- W2 – Narrative and Structure
- W3 – Clarity and Conciseness
- W4 – Terminology Consistency
- W5 – Inclusive Language
- W6 – Citation Formatting
- W7 – Target Audience Alignment

For each section, include:
- Score
- Summary
- Specific suggestions with:
  - Original text
  - Improved version
  - Explanation
- Consider displaying inputs as tables

More suggestions:

- try to use fittings icons/emoji
  - Critical issues (⚠️)
  - Suggestions (💡)
  - Improvements (✅)
- Use professional design elements to make reading easier and give the report a more professional look:
  - Consistent color coding for different score ranges:
    - High scores: Green (#4CAF50)
    - Medium scores: Yellow (#FFC107)
    - Low scores: Red (#F44336)
  - Clear hierarchy of information
  - Tables for structured data
  - Page numbers and headers/footers

Implementation Details:

1. PDF Generation:
   - Use reportlab library for PDF creation
   - Page size: Letter (8.5" x 11")
   - Margins: 1 inch on all sides
   - Font: Arial or similar sans-serif font
   - Base font size: 11pt
   - Headers: 14pt bold
   - Subheaders: 12pt bold

2. Layout Specifications:
   - Cover Page:
     - Company logo in header (/Users/robertjakob/rigorous-6/Agent1_Peer_Review/logo.svg)
     - Website in header: https://www.rigorous.company/
     - Star rating system: 5 stars max, half-star increments
     - Footer: Page number, date
   
   - Executive Summary Page:
     - Radar charts: 3 charts side by side, each 2.5" wide
     - Each chart should have clear labels and a 0-5 scale
     - Executive summary text: 11pt, justified alignment
   
   - Detailed Analysis Pages:
     - Each section starts on a new page
     - Section header: 14pt bold
     - Score display: Large, color-coded number
     - Tables: 10pt font, alternating row colors
     - Icons: 12pt size, consistent spacing

3. Error Handling:
   - Gracefully handle missing sections in JSON
   - Provide default values for missing scores
   - Skip empty sections without breaking layout
   - Log any data inconsistencies

4. Output:
   - Filename format: "Rigorous_Review_[manuscript_title]_[date].pdf"
   - Include metadata (title, author, creation date)
   - Enable PDF search functionality
   - Ensure PDF is accessible (proper tagging)
