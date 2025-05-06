from rq import get_current_job
import os
import time
import resend
from dotenv import load_dotenv
import pathlib

# Load environment variables from parent directory
env_path = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Initialize Resend
resend.api_key = os.getenv('RESEND_API_KEY')

def send_completion_email(email, result):
    """
    Send an email notification when a job is completed.
    
    Args:
        email (str): Recipient email address
        result (dict): The job result
    """
    print(f"Sending completion email to {email}")
    try:
        params = {
            "from": "ai.peer.reviewer@rigorous.kosullivan.ie",
            "to": email,
            "subject": f"Analysis Task Completed",
            "html": f"""
                <h2>Your Analysis Task is Complete!</h2>
                <p>File Size: {result.get('file_size_mb', 'N/A')} MB</p>
            """
        }
        print(f"Params: {params}")
        email_response = resend.Emails.send(params)
        print(f"Email response: {email_response}")
        print(f"Completion email sent to {email}")
    except Exception as e:
        print(f"Failed to send completion email: {str(e)}")

def run_analysis_task(temp_file_path, email):
    """
    Simple task to calculate file size in MB.
    
    Args:
        temp_file_path (str): Path to the temporary PDF file
    """
    job = get_current_job()
    
    try:
        if not os.path.exists(temp_file_path):
            raise FileNotFoundError(f"File not found: {temp_file_path}")
        
        time.sleep(120)  # Pretend processing takes time
        
        # Get file size in bytes
        file_size_bytes = os.path.getsize(temp_file_path)
        
        # Convert to MB
        file_size_mb = file_size_bytes / (1024 * 1024)

        print(f"File size: {file_size_mb} MB")
        
        # Clean up the temporary file
        try:
            os.remove(temp_file_path)
        except Exception as e:
            print(f"Warning: Failed to remove temporary file {temp_file_path}: {str(e)}")

            # Send email notification if email was provided

        result = {
            'status': 'success',
            'file_size_mb': round(file_size_mb, 2)
        }
        
        send_completion_email(email, result)
        
        return result
        
    except Exception as e:
        # Clean up the temporary file even if there's an error
        try:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        except Exception as cleanup_error:
            print(f"Warning: Failed to remove temporary file {temp_file_path}: {str(cleanup_error)}")
        
        return {
            'status': 'error',
            'message': str(e)
        }