
import os
import sys

sys.path.append(os.getcwd())
from config import Config

def test_api_key_loading():
    print("Testing API Key Loading...")
    
    key = Config.GEMINI_API_KEY
    default_key = ''
    
    masked_key = key[:4] + "..." + key[-4:] if key and len(key) > 8 else str(key)
    print(f"Loaded Key: {masked_key}")
    
    if key == default_key:
        print("FAILURE: Loaded key matches the hardcoded default. .env was NOT loaded.")
    elif not key or key == '':
        print("FAILURE: Key is missing or generic placeholder.")
    else:
        print("SUCCESS: A non-default API Key was loaded!")

if __name__ == "__main__":
    test_api_key_loading()
