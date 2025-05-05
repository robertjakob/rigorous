import os
from dotenv import load_dotenv
from openai import OpenAI

def test_api_key():
    # Force reload of environment variables
    load_dotenv(override=True)
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key loaded: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"API Key starts with: {api_key[:7]}...")
        print(f"API Key length: {len(api_key)}")
    
    # Print current working directory and .env file location
    print(f"\nCurrent working directory: {os.getcwd()}")
    env_path = os.path.join(os.getcwd(), '.env')
    print(f"Looking for .env file at: {env_path}")
    print(f".env file exists: {os.path.exists(env_path)}")
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Make a simple API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}],
            max_tokens=5
        )
        print("\nAPI call successful!")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    test_api_key() 