#!/usr/bin/env python3
"""
List Business Pages API
A simple API script to list all Facebook Pages associated with your business account
"""

import sys
import os
import json
from pathlib import Path
from tabulate import tabulate

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.meta_client import MetaBusinessClient


def main():
    """Find and display all pages associated with the business account"""
    print("正在查詢您的商業帳戶所擁有的 Facebook 專頁...\n")
    
    try:
        # Initialize the Meta Business Client
        client = MetaBusinessClient()
        
        # Get pages owned by the business
        pages = client.get_business_pages()
        
        if not pages:
            print("❌ 找不到與此商業帳戶關聯的 Facebook 專頁。")
            print("請確保您的商業帳戶已連接 Facebook 專頁並且有適當的權限。")
            return
        
        # Format the data for display
        table_data = []
        for page in pages:
            # Format fan count for display
            fan_count = page.get('fan_count', 0)
            if fan_count >= 1000000:
                fan_display = f"{fan_count/1000000:.1f}M"
            elif fan_count >= 1000:
                fan_display = f"{fan_count/1000:.1f}K"
            else:
                fan_display = str(fan_count)
                
            verification = "✓" if page.get('verification_status') else "✗"
            
            # Create a row for the table
            row = [
                page.get('id', 'N/A'),
                page.get('name', 'N/A'),
                f"@{page.get('username', '')}" if page.get('username') else "N/A",
                page.get('category', 'N/A'),
                fan_display,
                verification
            ]
            table_data.append(row)
        
        # Display the results in a table format
        headers = ["專頁 ID", "專頁名稱", "使用者名稱", "類別", "粉絲數", "已驗證"]
        print(f"✅ 找到 {len(pages)} 個 Facebook 專頁:")
        print(tabulate(table_data, headers, tablefmt="pretty"))
        
        # Option to save as JSON
        save_option = input("\n是否要將結果保存為 JSON 文件? (y/n): ")
        if save_option.lower() == 'y':
            output_path = os.path.join(project_root, "business_pages.json")
            
            # Convert the page objects to dictionaries
            pages_data = []
            for page in pages:
                page_dict = {}
                for key, value in dict(page).items():
                    page_dict[key] = value
                pages_data.append(page_dict)
                
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(pages_data, f, ensure_ascii=False, indent=2)
            print(f"結果已保存至: {output_path}")
            
    except ValueError as e:
        print(f"❌ 錯誤: {e}")
        print("\n⚠️ 請確保您已在 .env 文件中設置了有效的 API 憑證。")
        print("1. 複製模板: cp config/.env.template config/.env")
        print("2. 編輯文件: config/.env")
        print("3. 添加您的 APP_ID, APP_SECRET, ACCESS_TOKEN 和 BUSINESS_ID")
    except Exception as e:
        print(f"❌ 意外錯誤: {e}")
        print("\n⚠️ 如果這是權限錯誤，請檢查您的訪問令牌是否具有必要的權限:")
        print("   所需權限: pages_read_engagement, pages_show_list")


if __name__ == "__main__":
    main()