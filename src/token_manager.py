import os
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User

class TokenManager:
    """管理 Meta API 訪問令牌的類"""
    
    def __init__(self, app_id=None, app_secret=None, token_file=None):
        """初始化令牌管理器
        
        Args:
            app_id: Facebook 應用 ID
            app_secret: Facebook 應用密鑰
            token_file: 存儲令牌的文件路徑
        """
        self.app_id = app_id or os.getenv('APP_ID')
        self.app_secret = app_secret or os.getenv('APP_SECRET')
        
        if not self.app_id or not self.app_secret:
            raise ValueError("缺少 APP_ID 或 APP_SECRET，請檢查環境變量")
        
        # 設置令牌存儲文件
        if token_file:
            self.token_file = token_file
        else:
            base_dir = Path(__file__).parent.parent
            self.token_file = os.path.join(base_dir, 'config', 'tokens.json')
        
        # 加載現有令牌
        self.tokens = self._load_tokens()
    
    def _load_tokens(self):
        """從文件加載令牌"""
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def _save_tokens(self):
        """保存令牌到文件"""
        # 確保目錄存在
        os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
        
        with open(self.token_file, 'w') as f:
            json.dump(self.tokens, f, indent=2)
    
    def extend_user_token(self, short_lived_token):
        """將短期用戶令牌轉換為長期令牌"""
        url = "https://graph.facebook.com/v22.0/oauth/access_token"
        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'fb_exchange_token': short_lived_token
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'access_token' in data:
            # 存儲新獲取的長期令牌
            self.tokens['user_token'] = {
                'token': data['access_token'],
                'created_at': int(time.time()),
                'expires_in': data.get('expires_in', 5184000)  # 默認60天
            }
            self._save_tokens()
            return data['access_token']
        else:
            raise Exception(f"無法延長令牌: {data.get('error', {}).get('message')}")
    
    def get_page_token(self, user_token, page_id):
        """使用用戶令牌獲取頁面令牌"""
        # 初始化 API
        FacebookAdsApi.init(self.app_id, self.app_secret, user_token)
        
        me = User(fbid='me')
        pages = me.get_accounts(fields=['access_token', 'name', 'id'])
        
        for page in pages:
            if page['id'] == page_id:
                # 存儲新獲取的頁面令牌
                self.tokens[f'page_{page_id}'] = {
                    'token': page['access_token'],
                    'name': page['name'],
                    'created_at': int(time.time())
                }
                self._save_tokens()
                return page['access_token']
        
        raise Exception(f"找不到ID為 {page_id} 的頁面")
    
    def get_app_token(self):
        """獲取應用訪問令牌"""
        url = "https://graph.facebook.com/oauth/access_token"
        params = {
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'grant_type': 'client_credentials'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'access_token' in data:
            # 存儲新獲取的應用令牌
            self.tokens['app_token'] = {
                'token': data['access_token'],
                'created_at': int(time.time())
            }
            self._save_tokens()
            return data['access_token']
        else:
            raise Exception(f"無法獲取應用令牌: {data.get('error', {}).get('message')}")
    
    def get_valid_user_token(self, refresh=False):
        """獲取有效的用戶令牌，必要時刷新"""
        user_token_info = self.tokens.get('user_token', {})
        
        # 如果沒有用戶令牌或需要刷新，則從環境變量獲取並延長
        if not user_token_info or refresh:
            env_token = os.getenv('ACCESS_TOKEN')
            if not env_token:
                raise ValueError("缺少 ACCESS_TOKEN 環境變量")
            
            return self.extend_user_token(env_token)
        
        # 檢查令牌是否過期
        if 'created_at' in user_token_info and 'expires_in' in user_token_info:
            created = user_token_info['created_at']
            expires_in = user_token_info['expires_in']
            now = int(time.time())
            
            # 如果令牌已過期或將在1天內過期，則刷新
            if (created + expires_in - now) < 86400:  # 1天 = 86400秒
                env_token = os.getenv('ACCESS_TOKEN')
                if not env_token:
                    raise ValueError("缺少 ACCESS_TOKEN 環境變量，無法刷新令牌")
                
                return self.extend_user_token(env_token)
        
        return user_token_info['token']
    
    def get_valid_page_token(self, page_id, refresh=False):
        """獲取有效的頁面令牌"""
        page_token_key = f'page_{page_id}'
        page_token_info = self.tokens.get(page_token_key, {})
        
        # 如果沒有頁面令牌或需要刷新，則通過用戶令牌獲取
        if not page_token_info or refresh:
            user_token = self.get_valid_user_token()
            return self.get_page_token(user_token, page_id)
        
        return page_token_info['token']
    
    def get_valid_app_token(self, refresh=False):
        """獲取有效的應用令牌"""
        app_token_info = self.tokens.get('app_token', {})
        
        # 如果沒有應用令牌或需要刷新，則獲取新的
        if not app_token_info or refresh:
            return self.get_app_token()
        
        return app_token_info['token']
    
    def print_token_info(self):
        """打印所有存儲的令牌信息"""
        print("\n===== 存儲的令牌信息 =====")
        
        for key, info in self.tokens.items():
            print(f"\n{key}:")
            if 'token' in info:
                token_preview = f"{info['token'][:10]}...{info['token'][-10:]}"
                print(f"  令牌: {token_preview}")
            
            if 'created_at' in info:
                created_time = datetime.fromtimestamp(info['created_at']).strftime('%Y-%m-%d %H:%M:%S')
                print(f"  創建時間: {created_time}")
            
            if 'expires_in' in info:
                expires_in = info['expires_in']
                created_at = info['created_at']
                now = int(time.time())
                remaining = created_at + expires_in - now
                
                if remaining > 0:
                    days = remaining // 86400
                    hours = (remaining % 86400) // 3600
                    print(f"  剩餘時間: {days}天 {hours}小時")
                else:
                    print("  已過期")
            
            if 'name' in info:
                print(f"  名稱: {info['name']}")
        
        print("\n==============================")