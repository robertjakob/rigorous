# Flask-RQ2 File Analysis Service

This Flask application provides an API for analyzing files from Backblaze URLs. It uses Flask-RQ2 for background task processing and Resend for email notifications.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in the parent directory's `.env` file:
```
RESEND_API_KEY=your_resend_api_key_here
```

3. Start Redis server (if not already running):
```bash
redis-server
```

4. Start the Flask application:
```bash
python app.py
```

5. Start the RQ worker (in a separate terminal):
```bash
# On Mac:
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES rq worker

# On other platforms:
rq worker
```

## API Endpoints

### POST /analyze
Queues a file analysis task.

Request body:
```json
{
    "backblaze_url": "https://your-backblaze-url.com/path/to/file.pdf",
    "email": "recipient@example.com"
}
```

### GET /status/<job_id>
Check the status of a queued job.

## Mac-specific RQ Worker Note

On macOS, you need to run the RQ worker with `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` due to Apple's security measures. Here's why:

1. **Fork Safety**: macOS implements a security feature that prevents certain operations in forked processes. This is part of Apple's security hardening.

2. **Python's multiprocessing**: RQ uses Python's multiprocessing, which on Unix-like systems (including macOS) uses `fork()` to create new processes.

3. **Objective-C Runtime**: The issue occurs because macOS's Objective-C runtime has safety checks that prevent certain operations in forked processes. This is to prevent potential security vulnerabilities.

4. **The Solution**: Setting `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` tells the Objective-C runtime to disable these safety checks. While this is generally safe for development, you should be aware of the security implications in production environments.

Alternative solutions for production:
- Use a different process creation method (like 'spawn' instead of 'fork')
- Run the worker in a Docker container
- Use a different operating system for the worker

## Testing

Test the API with curl:

```bash
# Queue a task
curl -X POST http://localhost:5001/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "backblaze_url": "https://your-backblaze-url.com/path/to/file.pdf",
    "email": "your-email@example.com"
  }'

# Check task status
curl http://localhost:5001/status/<job_id>
```

## Architecture

- **Flask**: Web framework for handling HTTP requests
- **Flask-RQ2**: Task queue integration for background processing
- **Redis**: Message broker for the task queue
- **Resend**: Email service for notifications
- **RQ Worker**: Processes background tasks 