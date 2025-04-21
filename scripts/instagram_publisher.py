#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Publishing Script
---------------------------
This script provides functionality to publish content to Instagram
including image posts, videos, carousel posts and scheduled posts.
"""

import os
import sys
import time
import datetime
import argparse
from typing import Optional, List, Dict, Any

# Path setup for Facebook Business SDK
sys.path.append('/opt/homebrew/lib/python2.7/site-packages')
sys.path.append('/opt/homebrew/lib/python2.7/site-packages/facebook_business-3.0.0-py2.7.egg-info')
# 添加src目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.user import User
from facebook_business.adobjects.iguser import IGUser
from facebook_business.exceptions import FacebookRequestError

# 引入 TokenManager 和環境變數
from src.token_manager import TokenManager
from dotenv import load_dotenv


class InstagramPublisher:
    """Instagram content publishing handler"""
    
    def __init__(self, debug=False):
        """Initialize the Instagram publisher with authentication"""
        # 載入環境變數
        load_dotenv()
        load_dotenv('config/.env')
        
        self.app_id = os.getenv('APP_ID')
        self.app_secret = os.getenv('APP_SECRET')
        self.page_id = os.getenv('PAGE_ID')
        self.debug = debug
        
        # 初始化 TokenManager
        self.token_manager = TokenManager(app_id=self.app_id, app_secret=self.app_secret)
        self.ig_account_id = None
        self.ig_account = None
        
        # 設置 Facebook API
        self._setup_api()
    
    def _setup_api(self):
        """Set up Facebook API and get necessary tokens and IDs"""
        if self.debug:
            print("初始化 API...")
        
        # 獲取頁面token並初始化API
        page_token = self.token_manager.get_valid_page_token(self.page_id)
        FacebookAdsApi.init(self.app_id, self.app_secret, page_token)
        
        if self.debug:
            self.token_manager.print_token_info()
        
        # 獲取 Instagram 帳戶
        self._get_instagram_account()
    
    def _get_instagram_account(self):
        """Get Instagram business account ID from the Facebook Page"""
        if self.debug:
            print("獲取與頁面關聯的 Instagram 帳戶...")
        
        try:
            page = Page(self.page_id)
            page_data = page.api_get(fields=['instagram_business_account'])
            
            if 'instagram_business_account' in page_data:
                self.ig_account_id = page_data['instagram_business_account']['id']
                self.ig_account = IGUser(self.ig_account_id)
                if self.debug:
                    print(f"找到關聯的 Instagram 帳戶 ID: {self.ig_account_id}")
                
                # 獲取基本信息
                if self.debug:
                    self._print_account_info()
            else:
                raise ValueError("此頁面沒有關聯的 Instagram 商業帳戶")
                
        except Exception as e:
            raise Exception(f"獲取 Instagram 帳戶時出錯: {e}")
    
    def _print_account_info(self):
        """Print Instagram account information (for debug)"""
        account_info = self.ig_account.api_get(
            fields=['id', 'username', 'biography', 'followers_count']
        )
        print("---------Instagram 帳戶信息---------")
        print(f"ID: {account_info.get('id')}")
        print(f"用戶名: {account_info.get('username')}")
        print(f"簡介: {account_info.get('biography')}")
        print(f"粉絲數: {account_info.get('followers_count')}")
    
    def get_recent_posts(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent Instagram posts
        
        Args:
            limit: Maximum number of posts to retrieve
            
        Returns:
            List of post data dictionaries
        """
        if not self.ig_account:
            raise ValueError("Instagram 帳戶未初始化")
        
        media = self.ig_account.get_media(
            fields=['id', 'caption', 'media_type', 'permalink', 'timestamp', 'like_count'],
            params={'limit': limit}
        )
        
        return media
    
    def print_recent_posts(self, limit: int = 5):
        """Print recent Instagram posts (for debugging)"""
        media = self.get_recent_posts(limit)
        
        print("---------最近的 Instagram 貼文---------")
        if not media:
            print("沒有找到任何貼文")
            return
            
        for item in media:
            print(f"媒體 ID: {item.get('id')}")
            print(f"類型: {item.get('media_type')}")
            print(f"標題: {item.get('caption')}")
            print(f"發布時間: {item.get('timestamp')}")
            print(f"鏈接: {item.get('permalink')}")
            print(f"讚數: {item.get('like_count', 0)}")
            print("-" * 40)
    
    def post_image(self, image_url: str, caption: str, is_carousel_item: bool = False) -> Dict[str, Any]:
        """Create a container for an image post
        
        Args:
            image_url: URL of the image to post
            caption: Caption text for the post
            is_carousel_item: Whether this is part of a carousel post
            
        Returns:
            Response containing creation_id
        """
        if not self.ig_account:
            raise ValueError("Instagram 帳戶未初始化")
        
        params = {
            'image_url': image_url,
            'caption': caption,
        }
        
        if is_carousel_item:
            params['is_carousel_item'] = True
        
        try:
            response = self.ig_account.create_media(params=params)
            if self.debug:
                print(f"媒體容器已創建，creation_id: {response.get('id')}")
            return response
        except FacebookRequestError as e:
            raise Exception(f"創建媒體容器時出錯: {e}")
    
    def post_video(self, video_url: str, caption: str, cover_url: Optional[str] = None, 
                  upload_type: str = 'FEED') -> Dict[str, Any]:
        """Create a container for a video post
        
        Args:
            video_url: URL of the video to post
            caption: Caption text for the post
            cover_url: URL of the cover image (optional)
            upload_type: Type of upload (FEED, REELS, STORIES)
            
        Returns:
            Response containing creation_id
        """
        if not self.ig_account:
            raise ValueError("Instagram 帳戶未初始化")
        
        params = {
            'video_url': video_url,
            'caption': caption,
            'upload_type': upload_type
        }
        
        # For REELS, don't specify media_type as it's deprecated according to the error
        if upload_type != 'REELS':
            params['media_type'] = 'VIDEO'
            
        if cover_url:
            params['cover_url'] = cover_url
        
        if self.debug:
            print(f"準備上傳影片，參數: {params}")
            
        try:
            response = self.ig_account.create_media(params=params)
            if self.debug:
                print(f"影片媒體容器已創建，creation_id: {response.get('id')}")
            return response
        except FacebookRequestError as e:
            # Handle Google Drive URLs
            if "drive.google.com" in video_url and "Invalid parameter" in str(e):
                raise Exception(f"Google Drive 連結無法直接使用。請提供直接可下載的影片URL。Google Drive 需要額外的身份驗證，API 無法直接訪問。")
            raise Exception(f"創建影片媒體容器時出錯: {e}")
    
    def post_carousel(self, image_urls: List[str], caption: str) -> Dict[str, Any]:
        """Create a container for a carousel post with multiple images
        
        Args:
            image_urls: List of image URLs
            caption: Caption text for the post
            
        Returns:
            Response containing creation_id
        """
        if not self.ig_account:
            raise ValueError("Instagram 帳戶未初始化")
        
        # First, create individual carousel items
        children_ids = []
        for url in image_urls:
            try:
                response = self.post_image(url, "", is_carousel_item=True)
                children_ids.append(response['id'])
                if self.debug:
                    print(f"輪播項目已創建: {response['id']}")
            except Exception as e:
                raise Exception(f"創建輪播項目時出錯: {e}")
        
        # Then create the carousel container
        params = {
            'caption': caption,
            'children': children_ids,
            'media_type': 'CAROUSEL'
        }
        
        try:
            response = self.ig_account.create_media(params=params)
            if self.debug:
                print(f"輪播媒體容器已創建，creation_id: {response.get('id')}")
            return response
        except FacebookRequestError as e:
            raise Exception(f"創建輪播媒體容器時出錯: {e}")
    
    def schedule_post(self, media_type: str, content_url: str, caption: str, 
                     scheduled_time: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        """Schedule a post for future publishing
        
        Args:
            media_type: Type of media ('IMAGE', 'VIDEO', 'CAROUSEL')
            content_url: URL of the media or list of URLs for carousel
            caption: Caption text for the post
            scheduled_time: Unix timestamp for scheduled publishing time
            **kwargs: Additional parameters specific to the media type
            
        Returns:
            Response containing creation_id
        """
        if not self.ig_account:
            raise ValueError("Instagram 帳戶未初始化")
        
        # If no scheduled time is provided, default to 24 hours from now
        if not scheduled_time:
            scheduled_time = int(time.time()) + 86400  # 24 hours
        
        # Prepare base parameters for scheduling
        base_params = {
            'caption': caption,
            'publish_type': 'SCHEDULED',
            'scheduled_publish_time': scheduled_time
        }
        
        try:
            if media_type == 'IMAGE':
                params = {**base_params, 'image_url': content_url}
                response = self.ig_account.create_media(params=params)
            elif media_type == 'VIDEO':
                params = {
                    **base_params, 
                    'video_url': content_url
                }
                
                # For REELS, don't specify media_type as it's deprecated
                if kwargs.get('upload_type') != 'REELS':
                    params['media_type'] = 'VIDEO'
                    
                if 'cover_url' in kwargs:
                    params['cover_url'] = kwargs['cover_url']
                if 'upload_type' in kwargs:
                    params['upload_type'] = kwargs['upload_type']
                    
                response = self.ig_account.create_media(params=params)
            elif media_type == 'CAROUSEL':
                # For carousel, content_url should be a list of URLs
                if not isinstance(content_url, list):
                    raise ValueError("輪播貼文需要提供URL列表")
                    
                # Create carousel items
                children_ids = []
                for url in content_url:
                    item_response = self.ig_account.create_media(
                        params={'image_url': url, 'is_carousel_item': True}
                    )
                    children_ids.append(item_response['id'])
                
                # Create carousel container with scheduling
                carousel_params = {
                    **base_params,
                    'children': children_ids,
                    'media_type': 'CAROUSEL'
                }
                response = self.ig_account.create_media(params=carousel_params)
            else:
                raise ValueError(f"不支持的媒體類型: {media_type}")
            
            if self.debug:
                print(f"排程貼文媒體容器已創建，creation_id: {response.get('id')}")
                print(f"排程發布時間: {datetime.datetime.fromtimestamp(scheduled_time).strftime('%Y-%m-%d %H:%M:%S')}")
                
            return response
            
        except FacebookRequestError as e:
            raise Exception(f"排程貼文時出錯: {e}")
    
    def publish_media(self, creation_id: str) -> Dict[str, Any]:
        """Publish a media container using its creation ID
        
        Args:
            creation_id: The creation ID returned from a create_media call
            
        Returns:
            Response containing published media ID
        """
        if not self.ig_account:
            raise ValueError("Instagram 帳戶未初始化")
        
        try:
            response = self.ig_account.create_media_publish(
                params={'creation_id': creation_id}
            )
            if self.debug:
                print(f"媒體已發布，ID: {response.get('id')}")
            return response
        except FacebookRequestError as e:
            raise Exception(f"發布媒體時出錯: {e}")
    
    def create_and_publish(self, media_type: str, content: str, caption: str, **kwargs) -> Dict[str, Any]:
        """Create and immediately publish content in one step
        
        Args:
            media_type: Type of media ('IMAGE', 'VIDEO', 'CAROUSEL')
            content: URL of the media or list of URLs for carousel
            caption: Caption text for the post
            **kwargs: Additional parameters for specific media types
            
        Returns:
            Response from publish operation
        """
        creation_response = None
        
        try:
            # Create the appropriate media container
            if media_type == 'IMAGE':
                creation_response = self.post_image(content, caption)
            elif media_type == 'VIDEO':
                cover_url = kwargs.get('cover_url')
                upload_type = kwargs.get('upload_type', 'FEED')
                creation_response = self.post_video(content, caption, cover_url, upload_type)
            elif media_type == 'CAROUSEL':
                # For carousel, content should be a list
                if not isinstance(content, list):
                    raise ValueError("輪播貼文需要提供URL列表")
                creation_response = self.post_carousel(content, caption)
            else:
                raise ValueError(f"不支持的媒體類型: {media_type}")
            
            # Publish the media
            creation_id = creation_response['id']
            publish_response = self.publish_media(creation_id)
            return publish_response
            
        except Exception as e:
            if creation_response and 'id' in creation_response:
                print(f"創建了媒體容器 {creation_response['id']}，但發布失敗: {e}")
            raise Exception(f"創建並發布媒體時出錯: {e}")


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Instagram Publishing Tool')
    
    # Main command
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # View recent posts
    view_parser = subparsers.add_parser('view', help='View recent posts')
    view_parser.add_argument('--limit', type=int, default=5, help='Number of posts to view')
    
    # Post image
    image_parser = subparsers.add_parser('image', help='Post a single image')
    image_parser.add_argument('--url', required=True, help='URL of the image to post')
    image_parser.add_argument('--caption', required=True, help='Caption for the post')
    
    # Post video
    video_parser = subparsers.add_parser('video', help='Post a video')
    video_parser.add_argument('--url', required=True, help='URL of the video to post')
    video_parser.add_argument('--caption', required=True, help='Caption for the post')
    video_parser.add_argument('--cover', help='URL of the cover image (optional)')
    video_parser.add_argument('--type', choices=['FEED', 'REELS', 'STORIES'], default='FEED', 
                            help='Type of video post (default: FEED)')
    
    # Post carousel
    carousel_parser = subparsers.add_parser('carousel', help='Post a carousel of images')
    carousel_parser.add_argument('--urls', required=True, nargs='+', help='URLs of images for the carousel')
    carousel_parser.add_argument('--caption', required=True, help='Caption for the post')
    
    # Schedule post
    schedule_parser = subparsers.add_parser('schedule', help='Schedule a post for future publishing')
    schedule_parser.add_argument('--type', required=True, choices=['IMAGE', 'VIDEO', 'CAROUSEL'], 
                               help='Type of media to schedule')
    schedule_parser.add_argument('--content', required=True, nargs='+', 
                               help='URL(s) of the content (single URL for IMAGE/VIDEO, multiple for CAROUSEL)')
    schedule_parser.add_argument('--caption', required=True, help='Caption for the post')
    schedule_parser.add_argument('--time', type=int, help='Unix timestamp for publishing (default: 24h from now)')
    schedule_parser.add_argument('--cover', help='Cover URL for video (only for VIDEO type)')
    schedule_parser.add_argument('--upload-type', choices=['FEED', 'REELS', 'STORIES'], 
                               default='FEED', help='Upload type for video (only for VIDEO type)')
    
    # Tokens command
    tokens_parser = subparsers.add_parser('tokens', help='Manage API tokens')
    tokens_parser.add_argument('--refresh', action='store_true', help='Force refresh all tokens')
    
    # Global options
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    return parser.parse_args()


def main():
    """Main entry point for the script"""
    args = parse_args()
    
    try:
        # Tokens management command
        if args.command == 'tokens':
            # Initialize token manager directly
            token_manager = TokenManager()
            
            if args.refresh:
                print("強制刷新所有令牌...")
                page_id = os.getenv('PAGE_ID')
                user_token = token_manager.get_valid_user_token(refresh=True)
                page_token = token_manager.get_valid_page_token(page_id, refresh=True)
                app_token = token_manager.get_valid_app_token(refresh=True)
                print("所有令牌已刷新")
            
            token_manager.print_token_info()
            return 0
            
        # Initialize the Instagram publisher for other commands
        publisher = InstagramPublisher(debug=args.debug)
        
        # Process commands
        if args.command == 'view':
            publisher.print_recent_posts(args.limit)
            
        elif args.command == 'image':
            response = publisher.create_and_publish('IMAGE', args.url, args.caption)
            print(f"已發布圖片貼文，ID: {response.get('id')}")
            
        elif args.command == 'video':
            response = publisher.create_and_publish('VIDEO', args.url, args.caption, 
                                                  cover_url=args.cover, upload_type=args.type)
            print(f"已發布影片貼文，ID: {response.get('id')}")
            
        elif args.command == 'carousel':
            response = publisher.create_and_publish('CAROUSEL', args.urls, args.caption)
            print(f"已發布輪播貼文，ID: {response.get('id')}")
            
        elif args.command == 'schedule':
            content = args.content[0] if args.type != 'CAROUSEL' else args.content
            
            kwargs = {}
            if args.type == 'VIDEO':
                if args.cover:
                    kwargs['cover_url'] = args.cover
                kwargs['upload_type'] = args.upload_type
            
            creation_response = publisher.schedule_post(
                args.type, content, args.caption, args.time, **kwargs
            )
            
            scheduled_time = args.time or (int(time.time()) + 86400)
            print(f"已排程貼文，creation_id: {creation_response.get('id')}")
            print(f"排程發布時間: {datetime.datetime.fromtimestamp(scheduled_time).strftime('%Y-%m-%d %H:%M:%S')}")
            
        else:
            print("請指定命令: view, image, video, carousel, schedule, 或 tokens")
            return 1
            
    except Exception as e:
        print(f"錯誤: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())