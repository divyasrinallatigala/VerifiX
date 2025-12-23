
import os
import sys
from project_types import ExtractedData

# Ensure we can import modules
sys.path.append(os.getcwd())

# Mock environment to have NO key or default key
# We want to verify it RAISES an error
os.environ['GEMINI_API_KEY'] = 'AQ.Ab8RN6L6Hzm7lAoihlI27KiDCZEAwSmqCeXxRKhjrx_WPbX8Yg'

# Reload config to pick up the env var
import config
import importlib
importlib.reload(config)

from extraction_service import ExtractionService

def test_extraction_error():
    print("Testing Extraction Service Error Handling...")
    
    try:
        service = ExtractionService()
        # This should raise ValueError because key is default
        service.extract_from_image("ZHVtbXk=", "image/jpeg")
        print("FAILURE: expected ValueError but got result (or mock data).")
    except ValueError as e:
        print(f"SUCCESS: Caught expected ValueError: {e}")
    except Exception as e:
        print(f"FAILURE: Caught unexpected exception: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_extraction_error()
