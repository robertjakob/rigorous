import os
from dotenv import load_dotenv
from openai import OpenAI

def test_env_file():
    """Test that the .env file is being loaded correctly from the root directory."""
    print("Testing .env file loading...")
    
    # Try to load .env from the current directory
    load_dotenv()
    
    # Check if API key is loaded
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"API Key loaded from current directory: Yes")
        print(f"API Key starts with: {api_key[:7]}...")
    else:
        print("API Key loaded from current directory: No")
        
    # Try to load from parent directory
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    env_path = os.path.join(parent_dir, ".env")
    print(f"\nLooking for .env file at: {env_path}")
    print(f".env file exists: {os.path.exists(env_path)}")
    
    if os.path.exists(env_path):
        load_dotenv(env_path)
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print(f"API Key loaded from parent directory: Yes")
            print(f"API Key starts with: {api_key[:7]}...")
        else:
            print("API Key loaded from parent directory: No")
    
    # Try to make a simple API call
    if api_key:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello!"}],
                max_tokens=5
            )
            print("\nAPI call successful!")
            print(f"Response: {response.choices[0].message.content}")
        except Exception as e:
            print(f"\nError making API call: {str(e)}")
    else:
        print("\nNo API key found, skipping API call test")

if __name__ == "__main__":
    test_env_file() 