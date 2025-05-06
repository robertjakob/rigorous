from rq import get_current_job
import os

def run_analysis_task(temp_file_path):
    """
    Simple task to calculate file size in MB.
    
    Args:
        temp_file_path (str): Path to the temporary PDF file
    """
    job = get_current_job()
    
    try:
        if not os.path.exists(temp_file_path):
            raise FileNotFoundError(f"File not found: {temp_file_path}")
        
        # Get file size in bytes
        file_size_bytes = os.path.getsize(temp_file_path)
        
        # Convert to MB
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        # Clean up the temporary file
        try:
            os.remove(temp_file_path)
        except Exception as e:
            print(f"Warning: Failed to remove temporary file {temp_file_path}: {str(e)}")
        
        return {
            'status': 'success',
            'file_size_mb': round(file_size_mb, 2)
        }
        
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