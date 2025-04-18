#!/usr/bin/env python3
"""
Facebook Page Information Example
This script demonstrates how to retrieve Facebook page information without using an ad account
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.meta_client import MetaBusinessClient


def format_fan_count(count):
    """Format large numbers for better readability"""
    if count >= 1000000:
        return f"{count/1000000:.1f}M"
    elif count >= 1000:
        return f"{count/1000:.1f}K"
    else:
        return str(count)


def print_page_summary(page):
    """Print a summary of page information"""
    print(f"\n📄 Page: {page.get('name')} (ID: {page.get('id')})")
    print(f"  Category: {page.get('category')}")
    
    if page.get('username'):
        print(f"  Username: @{page.get('username')}")
        
    if page.get('fan_count'):
        print(f"  Fans: {format_fan_count(page.get('fan_count'))}")
        
    if page.get('verification_status'):
        verification = "✓ Verified" if page.get('verification_status') else "Not Verified"
        print(f"  Status: {verification}")
        
    if page.get('link'):
        print(f"  URL: {page.get('link')}")


def display_page_details(page_details):
    """Display detailed page information"""
    print("\n" + "=" * 50)
    print(f"📊 DETAILED PAGE INFORMATION: {page_details.get('name')}")
    print("=" * 50)
    
    # Basic information
    print(f"\n🔍 BASIC INFO:")
    print(f"  ID: {page_details.get('id')}")
    print(f"  Name: {page_details.get('name')}")
    if page_details.get('username'):
        print(f"  Username: @{page_details.get('username')}")
    if page_details.get('about'):
        print(f"  About: {page_details.get('about')}")
    if page_details.get('category'):
        print(f"  Category: {page_details.get('category')}")
    
    # Audience metrics
    print(f"\n👥 AUDIENCE:")
    if page_details.get('fan_count'):
        print(f"  Fans: {format_fan_count(page_details.get('fan_count'))}")
    if page_details.get('followers_count'):
        print(f"  Followers: {format_fan_count(page_details.get('followers_count'))}")
    if page_details.get('talking_about_count'):
        print(f"  People Talking About: {format_fan_count(page_details.get('talking_about_count'))}")
    
    # Contact information
    print(f"\n📞 CONTACT INFO:")
    if page_details.get('website'):
        print(f"  Website: {page_details.get('website')}")
    if page_details.get('phone'):
        print(f"  Phone: {page_details.get('phone')}")
    if page_details.get('emails'):
        print(f"  Email: {', '.join(page_details.get('emails'))}")
    
    # Location if available
    if page_details.get('location'):
        location = page_details.get('location')
        print(f"\n📍 LOCATION:")
        if location.get('street'):
            print(f"  Street: {location.get('street')}")
        city_parts = []
        if location.get('city'):
            city_parts.append(location.get('city'))
        if location.get('state'):
            city_parts.append(location.get('state'))
        if city_parts:
            print(f"  City/State: {', '.join(city_parts)}")
        if location.get('country'):
            print(f"  Country: {location.get('country')}")
        if location.get('zip'):
            print(f"  Zip: {location.get('zip')}")
    
    print("\n" + "=" * 50)


def display_recent_posts(posts, limit=5):
    """Display information about recent posts"""
    if not posts:
        print("\n📝 No recent posts found.")
        return
        
    print(f"\n📝 RECENT POSTS (Last {min(len(posts), limit)}):")
    
    for i, post in enumerate(posts[:limit], 1):
        print(f"\n  {i}. POST {post.get('id')}")
        
        # Post content
        if post.get('message'):
            message = post.get('message')
            # Truncate long messages
            if len(message) > 100:
                message = message[:97] + "..."
            print(f"     {message}")
        
        # Post details
        if post.get('created_time'):
            created_time = datetime.strptime(post.get('created_time'), '%Y-%m-%dT%H:%M:%S%z')
            print(f"     Posted: {created_time.strftime('%Y-%m-%d %H:%M')}")
            
        # Engagement stats
        engagement = []
        
        if post.get('likes') and post.get('likes').get('summary') and post.get('likes').get('summary').get('total_count'):
            likes = post.get('likes').get('summary').get('total_count')
            engagement.append(f"👍 {likes}")
            
        if post.get('comments') and post.get('comments').get('summary') and post.get('comments').get('summary').get('total_count'):
            comments = post.get('comments').get('summary').get('total_count')
            engagement.append(f"💬 {comments}")
            
        if post.get('shares') and post.get('shares').get('count'):
            shares = post.get('shares').get('count')
            engagement.append(f"🔄 {shares}")
            
        if engagement:
            print(f"     Engagement: {' | '.join(engagement)}")
            
        if post.get('permalink_url'):
            print(f"     Link: {post.get('permalink_url')}")


def main():
    """Main function to demonstrate accessing Facebook page information"""
    print("🚀 Accessing Facebook Page Information...\n")
    
    try:
        # Initialize the Meta Business Client
        client = MetaBusinessClient()
        
        # Get pages owned by the business
        print("📚 Retrieving Pages owned by your Business:")
        pages = client.get_business_pages()
        
        if not pages:
            print("❌ No Facebook Pages found for this business account.")
            print("Make sure your business account has connected Facebook Pages.")
            return
            
        # Display summary of all pages
        print(f"\n✅ Found {len(pages)} Facebook Page(s):")
        for page in pages:
            print_page_summary(page)
        
        # If there are multiple pages, allow user to select one
        selected_page = None
        if len(pages) == 1:
            selected_page = pages[0]
        else:
            try:
                print("\nMultiple pages found. Enter the number of the page you want to view details for:")
                for i, page in enumerate(pages, 1):
                    print(f"{i}. {page.get('name')}")
                    
                choice = int(input("\nEnter page number (or press Enter for page 1): ") or "1")
                if 1 <= choice <= len(pages):
                    selected_page = pages[choice-1]
                else:
                    print("Invalid choice. Using the first page.")
                    selected_page = pages[0]
            except ValueError:
                print("Invalid input. Using the first page.")
                selected_page = pages[0]
                
        # Get detailed information about the selected page
        page_id = selected_page.get('id')
        print(f"\n🔍 Getting detailed information for page: {selected_page.get('name')}")
        
        # Get page details
        page_details = client.get_page_details(page_id)
        if page_details:
            display_page_details(page_details)
        
        # Get recent posts
        print("\n📝 Retrieving recent posts...")
        posts = client.get_page_posts(page_id, limit=5)
        display_recent_posts(posts)
        
        # Offer to get insights if available
        print("\n📊 Would you like to view page insights (requires additional permissions)?")
        get_insights = input("Enter 'y' to view insights or any other key to skip: ")
        
        if get_insights.lower() == 'y':
            print("\nRetrieving page insights (last 28 days)...")
            insights = client.get_page_insights(page_id)
            
            if insights:
                print("\n📈 PAGE INSIGHTS (Last 28 Days):")
                for insight in insights:
                    metric = insight.get('name')
                    values = insight.get('values', [])
                    
                    if values and len(values) > 0:
                        # Get the most recent value
                        recent_value = values[-1].get('value')
                        if recent_value is not None:
                            print(f"  {metric}: {recent_value}")
            else:
                print("❌ No insights data available. This may be due to permission restrictions.")
                print("   The page insights require the 'read_insights' permission.")
                
        print("\n🎉 Facebook Page information retrieval complete!")
            
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\n⚠️ Please make sure you've set up your .env file with valid API credentials.")
        print("1. Copy the template: cp config/.env.template config/.env")
        print("2. Edit the file: config/.env")
        print("3. Add your APP_ID, APP_SECRET, ACCESS_TOKEN, and BUSINESS_ID")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\n⚠️ If this is a permission error, check that your access token")
        print("   has the necessary permissions: pages_read_engagement, pages_show_list")


if __name__ == "__main__":
    main()