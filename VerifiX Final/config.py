"""
config.py - Configuration settings for the Invoice Audit Agent
"""
import os
from dotenv import load_dotenv

# Load from .env in current directory OR verifyx subdirectory
# We use absolute paths based on this file's location to be safe
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_ENV = os.path.join(BASE_DIR, '.env')
VERIFYX_ENV = os.path.join(BASE_DIR, 'verifyx', '.env')

# Load root .env firs
if os.path.exists(ROOT_ENV):
    load_dotenv(ROOT_ENV)

# Then load verifyx .env (overrides root if present, assuming user edits this one)
if os.path.exists(VERIFYX_ENV):
    load_dotenv(VERIFYX_ENV, override=True)

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Model Configuration
    GEMINI_MODEL = 'gemini-2.0-flash'
    
    # Server Configuration
    HOST = '0.0.0.0'
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = True
    
    # Audit Rules Configuration
    PO_AMOUNT_TOLERANCE = 0.10  # 10% tolerance
    TAX_CALCULATION_TOLERANCE = 1000  # ₹1000 tolerance
    GST_RATE = 0.18  # 18% GST
    MIN_GST_LENGTH = 15
    
    # Archive Configuration
    MAX_ARCHIVE_SIZE = 1000