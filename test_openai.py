import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables")
    print("Please create a .env file with your OpenAI API key")
    exit(1)

# Initialize OpenAI client
openai.api_key = api_key

# Test OpenAI API
print("Testing OpenAI API connection...")
try:
    response = openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, this is a test message."}
        ]
    )
    print("OpenAI API test successful!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"Error testing OpenAI API: {str(e)}")
    print("Please check your API key and internet connection.") 