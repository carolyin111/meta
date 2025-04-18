#!/usr/bin/env python3
"""
Generate insights reports from Meta Business data.
This script demonstrates how to generate detailed performance reports from your ad account.
"""

import sys
import os
from pathlib import Path
import argparse
from datetime import datetime

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.meta_client import MetaBusinessClient
from src.insights_helper import (
    format_date_range,
    insights_to_dataframe,
    calculate_performance_metrics,
    export_insights_to_csv,
    format_insights_summary
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate Meta Ads insights report')
    parser.add_argument(
        '--days', 
        type=int, 
        default=30,
        help='Number of days to include in the report (default: 30)'
    )
    parser.add_argument(
        '--level', 
        type=str, 
        choices=['ad_account', 'campaign', 'adset', 'ad'], 
        default='ad_account',
        help='The level at which to generate the report (default: ad_account)'
    )
    parser.add_argument(
        '--id', 
        type=str, 
        help='ID of the specific object (required for campaign, adset, or ad level)'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        default='insights_report.csv',
        help='Output CSV filename (default: insights_report.csv)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.level != 'ad_account' and not args.id:
        parser.error(f"--id is required when --level is {args.level}")
    
    return args


def main():
    """Main function to generate insights reports."""
    args = parse_args()
    
    print(f"Generating {args.level} insights report for the past {args.days} days...")
    
    try:
        # Initialize the client
        client = MetaBusinessClient()
        
        # Prepare date range
        time_range = format_date_range(days_ago=args.days)
        print(f"Date range: {time_range['since']} to {time_range['until']}")
        
        # Define insights fields
        fields = [
            'impressions',
            'clicks',
            'spend',
            'ctr',
            'cpc',
            'reach',
            'frequency',
            'actions',
            'conversions',
            'cost_per_action_type',
            'conversion_rate_ranking',
            'quality_ranking',
            'engagement_rate_ranking'
        ]
        
        # Get insights data
        insights = client.get_insights(
            object_id=args.id,
            level=args.level,
            time_range=time_range,
            fields=fields
        )
        
        if not insights:
            print("No insights data available for the specified parameters.")
            return
            
        # Convert to DataFrame and calculate additional metrics
        insights_df = insights_to_dataframe(insights)
        insights_df = calculate_performance_metrics(insights_df)
        
        # Display summary
        print("\n" + format_insights_summary(insights_df))
        
        # Export to CSV
        export_insights_to_csv(insights_df, args.output)
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Please make sure you've set up your .env file with valid API credentials.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()