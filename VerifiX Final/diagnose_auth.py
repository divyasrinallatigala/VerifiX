import google.generativeai as genai
import os
from config import Config

def diagnose():
    print("--- Diagnostic Start ---")
    
    # Check Key
    key = Config.GEMINI_API_KEY
    if not key:
        print("ERROR: Key is empty")
        return
        
    print(f"Key Prefix: {key[:4]}")
    print(f"Key Length: {len(key)}")
    
    # Configure
    try:
        genai.configure(api_key=key)
        print("Configuration successful (client side)")
    except Exception as e:
        print(f"Configuration failed: {e}")
        return

    # Call API
    print("Attempting to list models...")
    try:
        models = genai.list_models()
        print("Available models:")
        has_flash = False
        for m in models:
            if 'gemini-2.0-flash' in m.name:
                has_flash = True
                print(f" - {m.name} (MATCH FOUND)")
        
        if has_flash:
            print("\nAttempting small generation test with gemini-2.0-flash...")
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content("Hello, say 'API connected'")
            print(f"Response: {response.text}")
        else:
            print("ERROR: gemini-2.0-flash not found in list")
            
    except Exception as e:
        print(f"API Call Failed: {e}")

if __name__ == "__main__":
    diagnose()
