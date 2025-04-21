import datetime
import os
import sys
import time
sys.path.append('/opt/homebrew/lib/python2.7/site-packages') # Replace this with the place you installed facebookads using pip
sys.path.append('/opt/homebrew/lib/python2.7/site-packages/facebook_business-3.0.0-py2.7.egg-info') # same as above

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.user import User
from facebook_business.adobjects.iguserforigonlyapi import IGUserForIGOnlyAPI

# 添加src目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.token_manager import TokenManager

# 載入環境變數
from dotenv import load_dotenv
# 嘗試從當前目錄和config目錄載入.env文件
load_dotenv()
load_dotenv('config/.env')

# 檢查環境變數
my_app_id = os.getenv('APP_ID')
my_app_secret = os.getenv('APP_SECRET')
my_page_id = os.getenv('PAGE_ID')

# 初始化令牌管理器
token_manager = TokenManager(app_id=my_app_id, app_secret=my_app_secret)

try:
    print("初始化 API 並獲取令牌...")
    
    # 獲取有效的頁面令牌(會自動刷新)
    page_token = token_manager.get_valid_page_token(my_page_id)
    
    # 使用頁面token初始化API
    FacebookAdsApi.init(my_app_id, my_app_secret, page_token)
    
    # 顯示令牌信息
    token_manager.print_token_info()
    
    # 使用獲取到的頁面ID和token
    my_page = Page(my_page_id)

    # 獲取頁面資訊
    page_info = my_page.api_get(fields=['id', 'name', 'category'])
    print('---------page info---------')
    print(page_info)

    # 獲取頁面貼文
    posts = my_page.get_posts(fields=['id', 'message', 'created_time'], params={'limit': 5})
    print('---------page posts---------')
    for post in posts:
        print(f"Post ID: {post['id']}")
        print(f"Message: {post.get('message', 'No message')}")
        print(f"Created: {post.get('created_time')}")
        print('--------------------------')

    # 嘗試發布一個新的貼文
    print('\n嘗試發布新貼文...')
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post_result = my_page.create_feed(
        params={
            'message': f"這是一個測試貼文，發布於 {current_time}"
        }
    )
    print(f"貼文已發布，ID: {post_result['id']}")

    # 嘗試發布一個排程貼文
    print('\n嘗試發布排程貼文...')
    # 設定排程時間為當前時間後24小時
    scheduled_time = int(time.time()) + 86400  # 24小時 = 86400秒
    schedule_result = my_page.create_feed(
        params={
            'message': f"這是一個排程測試貼文，計劃於 24 小時後發布",
            'scheduled_publish_time': scheduled_time,
            'published': False
        }
    )
    print(f"排程貼文已設置，ID: {schedule_result['id']}")
    print(f"排程發布時間: {datetime.datetime.fromtimestamp(scheduled_time).strftime('%Y-%m-%d %H:%M:%S')}")

except Exception as e:
    print(f"操作頁面時出錯: {e}")

# 嘗試獲取Instagram賬戶信息
try:
    # 獲取與頁面關聯的Instagram賬戶
    page_with_ig = my_page.api_get(fields=['instagram_business_account'])
    if 'instagram_business_account' in page_with_ig:
        ig_account_id = page_with_ig['instagram_business_account']['id']
        print(f"\n找到關聯的Instagram賬戶ID: {ig_account_id}")
        
        # 使用IGUser類來操作Instagram賬戶
        from facebook_business.adobjects.iguser import IGUser
        ig_account = IGUser(ig_account_id)
        
        # 獲取Instagram賬戶信息
        ig_info = ig_account.api_get(fields=['id', 'username', 'biography', 'followers_count'])
        print('---------Instagram賬戶信息---------')
        print(f"ID: {ig_info.get('id')}")
        print(f"用戶名: {ig_info.get('username')}")
        print(f"簡介: {ig_info.get('biography')}")
        print(f"粉絲數: {ig_info.get('followers_count')}")
        
        # 獲取最近的媒體內容
        ig_media = ig_account.get_media(fields=['id', 'caption', 'media_type', 'permalink'], params={'limit': 3})
        print('---------最近的Instagram貼文---------')
        for media in ig_media:
            print(f"媒體ID: {media.get('id')}")
            print(f"類型: {media.get('media_type')}")
            print(f"標題: {media.get('caption')}")
            print(f"鏈接: {media.get('permalink')}")
            print('--------------------------')
    else:
        print("此頁面沒有關聯的Instagram商業賬戶")
except Exception as e:
    print(f"獲取Instagram信息時出錯: {e}")