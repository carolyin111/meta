from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.page import Page
from facebook_business.exceptions import FacebookRequestError

from config.config import APP_ID, APP_SECRET, ACCESS_TOKEN, BUSINESS_ID, AD_ACCOUNT_ID, validate_config


class MetaBusinessClient:
    """Client for interacting with the Meta Business API."""
    
    def __init__(self):
        """Initialize the Meta Business API client."""
        if not validate_config():
            raise ValueError("Missing required environment variables")
        
        # Initialize the Facebook API
        self.api = FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)
        self.business = Business(BUSINESS_ID)
        self.ad_account = AdAccount(f'act_{AD_ACCOUNT_ID}')
        
    def get_ad_account_details(self):
        """Get details about the connected Ad Account."""
        try:
            fields = ['name', 'account_id', 'account_status', 'amount_spent', 'balance', 'currency']
            return self.ad_account.api_get(fields=fields)
        except FacebookRequestError as e:
            print(f"Error fetching ad account details: {e}")
            return None
    
    def get_campaigns(self, limit=100):
        """Get active campaigns for the ad account."""
        try:
            fields = ['name', 'objective', 'status', 'created_time', 'start_time', 'stop_time', 'daily_budget']
            params = {'limit': limit}
            return self.ad_account.get_campaigns(fields=fields, params=params)
        except FacebookRequestError as e:
            print(f"Error fetching campaigns: {e}")
            return []
    
    def get_adsets(self, campaign_id=None, limit=100):
        """Get ad sets for the ad account or a specific campaign."""
        try:
            fields = ['name', 'campaign_id', 'daily_budget', 'bid_amount', 'billing_event', 'optimization_goal', 'status']
            params = {'limit': limit}
            
            if campaign_id:
                params['campaign_id'] = campaign_id
                
            return self.ad_account.get_ad_sets(fields=fields, params=params)
        except FacebookRequestError as e:
            print(f"Error fetching ad sets: {e}")
            return []
    
    def get_ads(self, adset_id=None, limit=100):
        """Get ads for the ad account or a specific ad set."""
        try:
            fields = ['name', 'adset_id', 'creative', 'status', 'effective_status', 'created_time']
            params = {'limit': limit}
            
            if adset_id:
                params['adset_id'] = adset_id
                
            return self.ad_account.get_ads(fields=fields, params=params)
        except FacebookRequestError as e:
            print(f"Error fetching ads: {e}")
            return []
            
    def get_insights(self, object_id, level='ad_account', time_range=None, fields=None):
        """
        Get insights data for the specified object.
        
        Args:
            object_id: ID of the object to get insights for
            level: One of 'ad_account', 'campaign', 'adset', 'ad'
            time_range: Dictionary with 'since' and 'until' dates in YYYY-MM-DD format
            fields: List of insight metrics to retrieve
            
        Returns:
            List of insight objects
        """
        if fields is None:
            fields = [
                'impressions', 'clicks', 'spend', 'ctr', 'cpc', 
                'reach', 'frequency', 'actions', 'conversions'
            ]
            
        if time_range is None:
            time_range = {'since': '7d', 'until': 'today'}
            
        params = {
            'level': level,
            'time_range': time_range,
            'filtering': [],
            'breakdowns': [],
        }
        
        try:
            if level == 'ad_account':
                return self.ad_account.get_insights(fields=fields, params=params)
            elif level == 'campaign':
                campaign = self.ad_account.get_campaigns(filters=[{'field': 'campaign.id', 'operator': 'EQUAL', 'value': object_id}])
                return campaign[0].get_insights(fields=fields, params=params) if campaign else []
            elif level == 'adset':
                adset = self.ad_account.get_ad_sets(filters=[{'field': 'adset.id', 'operator': 'EQUAL', 'value': object_id}])
                return adset[0].get_insights(fields=fields, params=params) if adset else []
            elif level == 'ad':
                ad = self.ad_account.get_ads(filters=[{'field': 'ad.id', 'operator': 'EQUAL', 'value': object_id}])
                return ad[0].get_insights(fields=fields, params=params) if ad else []
            else:
                print(f"Invalid level: {level}")
                return []
        except FacebookRequestError as e:
            print(f"Error fetching insights: {e}")
            return []

    # New methods for working with Pages
    
    def get_business_pages(self, limit=100):
        """Get pages owned by the business."""
        try:
            fields = ['id', 'name', 'username', 'link', 'category', 'fan_count', 'verification_status']
            params = {'limit': limit}
            return self.business.get_owned_pages(fields=fields, params=params)
        except FacebookRequestError as e:
            print(f"Error fetching business pages: {e}")
            return []
    
    def get_page_details(self, page_id):
        """Get detailed information about a specific page."""
        try:
            page = Page(page_id)
            fields = [
                'id', 'name', 'username', 'link', 'about', 'category', 
                'category_list', 'fan_count', 'followers_count', 'talking_about_count', 
                'rating_count', 'overall_star_rating', 'verification_status', 
                'website', 'phone', 'emails', 'location', 'cover', 'picture'
            ]
            return page.api_get(fields=fields)
        except FacebookRequestError as e:
            print(f"Error fetching page details: {e}")
            return None
    
    def get_page_posts(self, page_id, limit=25):
        """Get recent posts from a page."""
        try:
            page = Page(page_id)
            fields = [
                'id', 'message', 'created_time', 'permalink_url', 
                'full_picture', 'type', 'status_type', 'likes.summary(true)', 
                'comments.summary(true)', 'shares'
            ]
            params = {'limit': limit}
            return page.get_posts(fields=fields, params=params)
        except FacebookRequestError as e:
            print(f"Error fetching page posts: {e}")
            return []
    
    def get_page_insights(self, page_id, period='day', days=28, metrics=None):
        """
        Get page insights data.
        
        Args:
            page_id: ID of the page
            period: One of 'day', 'week', 'month'
            days: Number of days to look back
            metrics: List of metrics to retrieve
            
        Returns:
            List of insights objects
        """
        if metrics is None:
            metrics = [
                'page_impressions',
                'page_impressions_unique',
                'page_engaged_users',
                'page_post_engagements',
                'page_fans',
                'page_fan_adds',
                'page_views_total'
            ]
            
        try:
            page = Page(page_id)
            params = {
                'period': period,
                'date_preset': f'last_{days}_days'
            }
            
            return page.get_insights(params=params, metric=metrics)
        except FacebookRequestError as e:
            print(f"Error fetching page insights: {e}")
            return []