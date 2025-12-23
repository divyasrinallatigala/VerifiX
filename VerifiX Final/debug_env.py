
import os
import sys
from dotenv import load_dotenv, find_dotenv

print(f"CWD: {os.getcwd()}")
print(f"Script: {__file__}")

# check potential locs
locs = [
    ".env",
    "verifyx/.env",
    os.path.join(os.path.dirname(__file__), ".env"),
    os.path.join(os.path.dirname(__file__), "verifyx", ".env")
]

found = False
for loc in locs:
    exists = os.path.exists(loc)
    print(f"Checking {loc}: {'EXISTS' if exists else 'MISSING'}")
    if exists:
        print(f"  Content preview (first 20 chars):")
        try:
            with open(loc, 'r') as f:
                content = f.read().strip()
                print(f"  '{content[:20]}...'")
                if "GEMINI_API_KEY" in content:
                    print("  Found 'GEMINI_API_KEY' in file.")
                else:
                    print("  'GEMINI_API_KEY' NOT found in file.")
        except Exception as e:
            print(f"  Error reading: {e}")

print("-" * 20)
print("Attempting to load...")

# Clear env first just in case
if 'GEMINI_API_KEY' in os.environ:
    del os.environ['GEMINI_API_KEY']

# Try standard load
load_dotenv()
val = os.getenv('GEMINI_API_KEY')
print(f"After load_dotenv(): {val}")

if not val:
    # Try verifyx
    v_path = os.path.join(os.getcwd(), 'verifyx', '.env')
    if os.path.exists(v_path):
        print(f"Loading direct from {v_path}")
        load_dotenv(v_path)
        val = os.getenv('GEMINI_API_KEY')
        print(f"After loading verifyx/.env: {val}")

