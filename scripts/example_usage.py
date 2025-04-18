#!/usr/bin/env python3
"""
Example usage of the Meta Business Client.
This script demonstrates how to retrieve basic information from your Facebook Ads account.
"""

import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.meta_client import MetaBusinessClient


def main():
    """Main function to demonstrate Meta Business SDK usage."""
    print("Initializing Meta Business Client...")
    try:
        client = MetaBusinessClient()
        
        # Get account details
        print("\n--- Account Details ---")
        account_details = client.get_ad_account_details()
        if account_details:
            print(f"Account Name: {account_details.get('name')}")
            print(f"Account ID: {account_details.get('account_id')}")
            print(f"Account Status: {account_details.get('account_status')}")
            print(f"Amount Spent: {account_details.get('amount_spent')}")
            print(f"Balance: {account_details.get('balance')} {account_details.get('currency')}")
        
        # Get campaigns
        print("\n--- Recent Campaigns ---")
        campaigns = client.get_campaigns(limit=5)
        for i, campaign in enumerate(campaigns, 1):
            print(f"{i}. {campaign.get('name')} (Status: {campaign.get('status')})")
        
        # Get insights for the ad account
        print("\n--- Account Insights (Last 7 Days) ---")
        insights = client.get_insights(None, level='ad_account')
        if insights and len(insights) > 0:
            insight = insights[0]
            print(f"Impressions: {insight.get('impressions')}")
            print(f"Clicks: {insight.get('clicks')}")
            print(f"Spend: {insight.get('spend')}")
            print(f"CTR: {insight.get('ctr')}%")
            print(f"CPC: {insight.get('cpc')}")
        else:
            print("No insights data available")
            
    except ValueError as e:
        print(f"Error: {e}")
        print("Please make sure you've set up your .env file with valid API credentials.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()