import os
from pathlib import Path
from dotenv import load_dotenv

# Get the base directory of the project
BASE_DIR = Path(__file__).parent.parent

# Load environment variables
env_path = os.path.join(BASE_DIR, 'config', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    print("Warning: .env file not found. Create one based on .env.template")

# Meta API credentials
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
BUSINESS_ID = os.getenv('BUSINESS_ID')
AD_ACCOUNT_ID = os.getenv('AD_ACCOUNT_ID')

def validate_config():
    """Validates that all required environment variables are set."""
    required_vars = ['APP_ID', 'APP_SECRET', 'ACCESS_TOKEN', 'BUSINESS_ID', 'AD_ACCOUNT_ID']
    missing_vars = [var for var in required_vars if not globals().get(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with the required values.")
        return False
    return True