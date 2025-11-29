import os
from dotenv import load_dotenv

# Load env vars
load_dotenv("backend/.env")

from services.ai import analyze_recipe

# Mock metadata
mock_metadata = {
    "title": "Test Recipe",
    "description": "This is a test recipe. Step 1: Boil water. Step 2: Add pasta."
}

try:
    print("Testing OpenAI API...")
    result = analyze_recipe(mock_metadata)
    print("Success!")
    print(result)
except Exception as e:
    print(f"Error: {e}")
