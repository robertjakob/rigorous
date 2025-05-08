import os
import re

def update_score_scale(file_path):
    """Update the score scale in a file from 1-10 to 1-5."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace score scale comments
    content = re.sub(
        r'# Single comprehensive score \(1-10\)',
        '# Single comprehensive score (1-5)\n            # IMPORTANT: The score MUST be between 1 and 5, where:\n            # 1 = Poor: Major issues that significantly impact quality\n            # 2 = Below Average: Several notable issues that need attention\n            # 3 = Average: Some issues but generally acceptable\n            # 4 = Good: Minor issues that don\'t significantly impact quality\n            # 5 = Excellent: Very few or no issues, high quality',
        content
    )
    
    # Replace score range in JSON format
    content = re.sub(
        r'"score": <1-10>',
        '"score": <1-5>',
        content
    )
    
    with open(file_path, 'w') as f:
        f.write(content)

def main():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the directories to search
    agent_dirs = [
        os.path.join(script_dir, 'src', 'reviewer_agents', 'section'),
        os.path.join(script_dir, 'src', 'reviewer_agents', 'rigor'),
        os.path.join(script_dir, 'src', 'reviewer_agents', 'writing')
    ]
    
    # Update each agent file
    for agent_dir in agent_dirs:
        for filename in os.listdir(agent_dir):
            if filename.endswith('_agent.py'):
                file_path = os.path.join(agent_dir, filename)
                print(f"Updating {filename}...")
                update_score_scale(file_path)
    
    print("All agent files have been updated to use the 1-5 scale.")

if __name__ == "__main__":
    main() 