import os
import sys
sys.path.append('/opt/homebrew/lib/python2.7/site-packages') # Replace this with the place you installed facebookads using pip
sys.path.append('/opt/homebrew/lib/python2.7/site-packages/facebook_business-3.0.0-py2.7.egg-info') # same as above

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adaccountuser import AdAccountUser

my_app_id = os.getenv('APP_ID')
my_app_secret = os.getenv('APP_SECRET')
my_access_token = os.getenv('ACCESS_TOKEN')
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)



#  ===== Business =======
# 懶惰得人的平台
myBusiness = Business(os.getenv('BUSINESS_ID'))
businessUser = myBusiness.get_business_users()
print('---------businessUser---------')
print(businessUser)

# adInfo = myBusiness.get_ad_account_infos()
# print('---------ad info---------')
# print(adInfo)


#  ===== AdAccount =======
my_account = AdAccount('act_' + os.getenv('AD_ACCOUNT_ID'))
campaigns = my_account.get_campaigns()
print(campaigns)

# users = my_account.get_users()
# print('--------get_users----------')
# for user in users:
#     print(user[AdAccountUser.Field.id])
