from flask import Flask, request, jsonify
from flask_rq2 import RQ
import os
import tempfile
import requests
from urllib.parse import urlparse
from tasks import run_analysis_task

app = Flask(__name__)

# Configure Redis connection
app.config['RQ_REDIS_URL'] = 'redis://localhost:6379/0'
app.config['RQ_QUEUES'] = ['default']

# Initialize RQ
rq = RQ(app)

# Register the task with RQ
job = rq.job(run_analysis_task)

def download_from_backblaze(url):
    """
    Download a file from Backblaze URL to a temporary location.
    
    Args:
        url (str): The Backblaze URL of the file
        
    Returns:
        str: Path to the downloaded temporary file
    """
    try:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_path = temp_file.name
        temp_file.close()
        
        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Save the file
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return temp_path
    except Exception as e:
        raise Exception(f"Failed to download file from Backblaze: {str(e)}")

@app.route('/analyze', methods=['POST'])
def analyze_paper():
    data = request.get_json()
    if not data or 'backblaze_url' not in data:
        return jsonify({'error': 'No backblaze_url provided'}), 400
    if not data or 'email' not in data:
        return jsonify({'error': 'No email provided'}), 400
    
    backblaze_url = data['backblaze_url']
    email = data['email']
    
    try:
        # Download the file from Backblaze
        response = requests.get(backblaze_url)
        response.raise_for_status()
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name
        
        # Queue the analysis task
        job = rq.get_queue().enqueue(run_analysis_task, temp_file_path, email)
        
        return jsonify({
            'status': 'success',
            'message': 'Analysis task queued',
            'job_id': job.id
        })
        
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to download file: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/<job_id>', methods=['GET'])
def get_job_status(job_id):
    job = rq.get_queue().fetch_job(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    if job.is_finished:
        result = job.result
        print(f"Job {job_id} completed successfully!")
        print(f"Result: {result}")
        
        return jsonify({
            'status': 'completed',
            'message': 'Job completed successfully',
            'result': result
        })
    elif job.is_failed:
        error = str(job.exc_info)
        print(f"Job {job_id} failed!")
        print(f"Error: {error}")
        return jsonify({
            'status': 'failed',
            'error': error
        }), 500
    else:
        return jsonify({
            'status': 'processing',
            'message': 'Job is still running'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)