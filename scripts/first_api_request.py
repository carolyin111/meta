#!/usr/bin/env python3
"""
First Meta API Request Example
This script demonstrates how to make your first API request to the Meta Business API
"""

import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.meta_client import MetaBusinessClient


def main():
    """Make a first basic request to the Meta API"""
    print("🚀 Making your first Meta API request...\n")
    
    try:
        # Initialize the Meta Business Client
        client = MetaBusinessClient()
        
        # Get basic information about the ad account
        print("📊 Retrieving Ad Account Details:")
        account_details = client.get_ad_account_details()
        
        if account_details:
            print(f"\n✅ Success! Connected to your Meta Ad Account")
            print("-" * 50)
            print(f"Account Name: {account_details.get('name')}")
            print(f"Account ID: {account_details.get('account_id')}")
            print(f"Account Status: {account_details.get('account_status')}")
            print(f"Currency: {account_details.get('currency')}")
            print("-" * 50)
            
            # Let's also get a list of the most recent campaigns
            print("\n📈 Retrieving your most recent campaigns:")
            campaigns = client.get_campaigns(limit=5)
            
            if campaigns:
                for i, campaign in enumerate(campaigns, 1):
                    print(f"{i}. {campaign.get('name')} (Status: {campaign.get('status')})")
            else:
                print("No campaigns found in this account.")
                
            print("\n🎉 Congratulations! Your first Meta API request was successful.")
            print("You can now start building more complex functionality using the SDK.")
        else:
            print("❌ Failed to retrieve account details. Check your API credentials.")
            
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\n⚠️ Please make sure you've set up your .env file with valid API credentials.")
        print("1. Copy the template: cp config/.env.template config/.env")
        print("2. Edit the file: config/.env")
        print("3. Add your APP_ID, APP_SECRET, ACCESS_TOKEN, BUSINESS_ID, and AD_ACCOUNT_ID")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\n⚠️ If this is an authentication error, check your API credentials.")
        print("If it's another type of error, check the Meta API documentation or your code.")


if __name__ == "__main__":
    main()