import datetime
import os
import sys
import time
sys.path.append('/opt/homebrew/lib/python2.7/site-packages') # Replace this with the place you installed facebookads using pip
sys.path.append('/opt/homebrew/lib/python2.7/site-packages/facebook_business-3.0.0-py2.7.egg-info') # same as above

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.iguserforigonlyapi import IGUserForIGOnlyAPI

my_app_id = os.getenv('APP_ID')
my_app_secret = os.getenv('APP_SECRET')

#  ===== Page =======
my_page_id = os.getenv('PAGE_ID')
page_access_token = os.getenv('PAGE_ACCESS_TOKEN')


# 初始化 API 時使用頁面的 access token
FacebookAdsApi.init(my_app_id, my_app_secret, page_access_token)

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


# (TODO)發佈貼文
# fan_count = my_page.
# iguserforigonlyapi.p
# 
# 獲取 Instagram 用戶
ig_user_id = os.getenv('IG_USER_ID')
ig_user = IGUserForIGOnlyAPI(ig_user_id)

response = ig_user.create_media(
    params={
        'image_url': 'https://example.com/image.jpg',
        'caption': '這是一個排程貼文測試',
        'publish_type': 'SCHEDULED',
        'scheduled_publish_time': 1745019000
    }
)