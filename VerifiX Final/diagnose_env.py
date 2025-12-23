
import os
import sys

# Force output to be unbuffered
sys.stdout.reconfigure(line_buffering=True)

print(f"Diagnostics Start")
print(f"CWD: {os.getcwd()}")

api_key_env = os.environ.get('AQ.Ab8RN6L6Hzm7lAoihlI27KiDCZEAwSmqCeXxRKhjrx_WPbX8Yg')
print(f"Environment GEMINI_API_KEY before load_dotenv: {api_key_env}")

try:
    from dotenv import load_dotenv, find_dotenv
    print("python-dotenv is installed and imported.")
except ImportError:
    print("CRITICAL: python-dotenv NOT FOUND.")

# Check for .env files
possible_paths = [
    os.path.join(os.getcwd(), ".env"),
    os.path.join(os.getcwd(), "verifyx", ".env"),
    "C:\\Users\\N.DIVYA SRI\\OneDrive\\Desktop\\OneDrive\\Desktop\\Verifix new\\.env",
]

for path in possible_paths:
    print(f"\nChecking path: {path}")
    if os.path.exists(path):
        print("  [EXISTS]")
        try:
            size = os.path.getsize(path)
            print(f"  Size: {size} bytes")
            if size < 5:
                print("  [WARNING] File seems identical to empty or too small.")
            
            with open(path, 'rb') as f:
                raw = f.read()
                print(f"  Raw bytes header: {raw[:20]}")
                
            try:
                content = raw.decode('utf-8').strip()
                print(f"  Content (UTF-8): '{content}'")
                if "GEMINI_API_KEY" in content:
                    print("  [OK] Contains GEMINI_API_KEY")
                else:
                    print("  [MISSING] Does not contain GEMINI_API_KEY")
            except Exception as e:
                print(f"  [encoding error] {e}")
                
        except Exception as e:
            print(f"  Error reading file: {e}")
            
        print("  Attempting load_dotenv on this file...")
        try:
            # Clear first
            if 'GEMINI_API_KEY' in os.environ:
                del os.environ['GEMINI_API_KEY']
            load_dotenv(path, override=True)
            val = os.environ.get('GEMINI_API_KEY')
            print(f"  Resulting GEMINI_API_KEY: {val}")
        except Exception as e:
            print(f"  Error loading: {e}")
    else:
        print("  [NOT FOUND]")

print("\n--- Config Test ---")
try:
    # Clear again
    if 'GEMINI_API_KEY' in os.environ:
        del os.environ['GEMINI_API_KEY']
        
    import config
    import importlib
    importlib.reload(config)
    print(f"Config.GEMINI_API_KEY: {config.Config.GEMINI_API_KEY}")
except Exception as e:
    print(f"Config import failed: {e}")
