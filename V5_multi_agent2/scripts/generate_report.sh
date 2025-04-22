#!/bin/bash

# Script to generate a report from the combined_results.json file

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory (parent of scripts directory)
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Set paths
INPUT_FILE="$PROJECT_ROOT/results/combined_results.json"
OUTPUT_FILE="$PROJECT_ROOT/results/manuscript_report.md"
CONVERTER_SCRIPT="$PROJECT_ROOT/src/utils/json_to_report.py"

# Check if the input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file not found at $INPUT_FILE"
    exit 1
fi

# Run the converter script
echo "Generating report from $INPUT_FILE..."
python "$CONVERTER_SCRIPT" --input "$INPUT_FILE" --output "$OUTPUT_FILE"

# Check if the report was generated successfully
if [ -f "$OUTPUT_FILE" ]; then
    echo "Report generated successfully at $OUTPUT_FILE"
    
    # Open the report if on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$OUTPUT_FILE"
    fi
else
    echo "Error: Failed to generate report"
    exit 1
fi 