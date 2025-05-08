# Scientific Rigor Agents

These agents ensure research meets high standards of originality, ethics, and accuracy by evaluating various aspects of scientific rigor.

## Agent Labels and Descriptions

### R1 - Originality and Contribution Agent
- **Purpose**: Assesses research novelty and unique contributions to the field.
- **Key Evaluations**:
  - Novelty of research approach
  - Unique contributions
  - Verification of novelty claims
  - Comparison with existing literature
  - Knowledge advancement

### R2 - Impact and Significance Agent
- **Purpose**: Evaluates research influence and broader implications.
- **Key Evaluations**:
  - Field influence potential
  - Research advancement potential
  - Practical applications
  - Policy implications
  - Future research directions

### R3 - Ethics and Compliance Agent
- **Purpose**: Reviews ethical considerations and research standards compliance.
- **Key Evaluations**:
  - Conflicts of interest
  - Data privacy and protection
  - Informed consent procedures
  - Research integrity
  - Ethical guidelines adherence

### R4 - Data and Code Availability Agent
- **Purpose**: Checks data and code sharing practices and documentation.
- **Key Evaluations**:
  - Data availability
  - Code availability
  - Documentation quality
  - Reproducibility
  - Sharing practices

### R5 - Statistical Rigor Agent
- **Purpose**: Ensures appropriateness and correctness of statistical methods.
- **Key Evaluations**:
  - Method appropriateness
  - Analysis correctness
  - Assumptions validation
  - Power analysis
  - Reporting completeness

### R6 - Technical Accuracy Agent
- **Purpose**: Reviews mathematical derivations and technical content.
- **Key Evaluations**:
  - Mathematical correctness
  - Algorithm accuracy
  - Technical clarity
  - Derivation completeness
  - Implementation feasibility

### R7 - Consistency Agent
- **Purpose**: Checks logical coherence across manuscript sections.
- **Key Evaluations**:
  - Methods-Results alignment
  - Results-Conclusions alignment
  - Claims consistency
  - Variable/terminology consistency
  - Cross-section coherence

## Implementation Details

Each agent:
- Inherits from `BaseReviewerAgent`
- Uses the `ReportTemplate` for standardized reports
- Provides detailed analysis with subscores
- Generates specific improvement suggestions
- Includes error handling and reporting
- Returns structured JSON output

## Usage

The agents can be used individually or as part of a comprehensive review process. Each agent focuses on specific aspects of scientific rigor while maintaining consistency in reporting format and evaluation standards. 