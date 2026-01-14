import os
import sys
from dotenv import load_dotenv
from google import genai

# Add project root to path
sys.path.append(os.getcwd())

load_dotenv()

def list_gemini_models():
    api_key = os.getenv("API_KEY_GEMINI")
    if not api_key:
        print("Error: API_KEY_GEMINI not found in .env file.")
        return

    try:
        client = genai.Client(api_key=api_key)
        
        print("Fetching available models from Google GenAI...")
        # Note: The exact method might vary by SDK version, trying common pattern for the new library
        pager = client.models.list()
        
        print(f"\n{'Name':<50} {'Display Name':<30}")
        print("-" * 80)
        
        count = 0
        for model in pager:
            # Filter for Gemini models usually relevant to generation
            name = model.name
            if 'gemini' in name.lower():
                display_name = getattr(model, 'display_name', '')
                print(f"{name:<50} {display_name:<30}")
                count += 1
                
        print(f"\nTotal Gemini models found: {count}")

    except Exception as e:
        print(f"Error listing models: {e}")
        # In case the SDK structure is different than expected
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    list_gemini_models()
