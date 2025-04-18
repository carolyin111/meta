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

# 載入環境變數
from dotenv import load_dotenv
# 嘗試從當前目錄和config目錄載入.env文件
load_dotenv()
load_dotenv('config/.env')

# 檢查環境變數
my_app_id = os.getenv('APP_ID')
my_app_secret = os.getenv('APP_SECRET')
user_access_token = os.getenv('ACCESS_TOKEN')  # 用戶的access token
my_page_id = os.getenv('PAGE_ID')
page_access_token = os.getenv('PAGE_ACCESS_TOKEN')

# 檢查環境變數是否成功載入
if not my_app_id or not my_app_secret or not user_access_token:
    print("錯誤: 關鍵環境變數未正確載入")
    print(f"APP_ID: {my_app_id}")
    print(f"APP_SECRET: {'已設置' if my_app_secret else '未設置'}")
    print(f"ACCESS_TOKEN: {'已設置' if user_access_token else '未設置'}")
    sys.exit(1)

# 首先用用戶token初始化API，以獲取頁面token
print("初始化 API 並嘗試獲取新的頁面 token...")
FacebookAdsApi.init(my_app_id, my_app_secret, user_access_token)

# 嘗試獲取頁面的 access token
try:
    print("獲取頁面 access_token...")
    me = User(fbid='me')
    pages = me.get_accounts(fields=['access_token', 'name', 'id'])
    
    # 顯示所有可用的頁面
    print("\n可用的頁面:")
    for page in pages:
        print(f"ID: {page['id']}, 名稱: {page['name']}")
        if page['id'] == my_page_id:
            page_access_token = page['access_token']
            print(f"找到指定頁面! 獲取新的 access_token")
    
    if not page_access_token and my_page_id:
        print(f"找不到ID為 {my_page_id} 的頁面，請確認頁面ID是否正確")
        if pages:
            first_page = pages[0]
            print(f"使用第一個可用頁面: {first_page['name']} (ID: {first_page['id']})")
            my_page_id = first_page['id']
            page_access_token = first_page['access_token']
    
    # 使用新獲取的頁面token重新初始化API
    if page_access_token:
        print(f"使用新的頁面token重新初始化API...")
        FacebookAdsApi.init(my_app_id, my_app_secret, page_access_token)
    else:
        print("無法獲取任何頁面的 access_token")
        sys.exit(1)
        
except Exception as e:
    print(f"獲取頁面token時出錯: {e}")
    sys.exit(1)

# 使用獲取到的頁面ID和token
my_page = Page(my_page_id)

try:
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