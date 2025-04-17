# Meta Business SDK 專案

這個專案使用 Meta (Facebook) Business SDK 進行 Meta 平台的商業應用開發。

## 環境設置

本專案使用 Python 虛擬環境（venv）管理依賴包，並已經安裝了 Meta Business SDK。

### 環境要求

- Python 3.x
- MacOS (或其他支持的作業系統)

## 如何啟動專案

### 第一步：啟動虛擬環境

每次開始工作時，你需要先激活虛擬環境。在終端機中執行以下命令：

```bash
cd /Users/carolyin/sideproject/meta
source venv/bin/activate
```

成功啟動後，你會在命令行的開頭看到 `(venv)` 的提示，表示你已經在虛擬環境中。

### 第二步：使用 Meta Business SDK

在激活虛擬環境後，你可以直接運行你的 Python 腳本，Python 解釋器會自動使用虛擬環境中安裝的 Meta Business SDK。

示例：

```python
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

# 初始化 API 連接
my_app_id = 'your-app-id'
my_app_secret = 'your-app-secret'
my_access_token = 'your-access-token'
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

# 使用 SDK
my_account = AdAccount('act_<your-account-id>')
campaigns = my_account.get_campaigns()
print(campaigns)
```

### 第三步：退出虛擬環境

當你完成工作後，可以通過以下命令退出虛擬環境：

```bash
deactivate
```

## 安裝新的依賴包

如果你需要安裝其他的依賴包，請確保你已經激活了虛擬環境，然後使用 pip：

```bash
pip install package-name
```

## 更新 Meta Business SDK

要更新 SDK 到最新版本，請在激活虛擬環境後運行：

```bash
pip install --upgrade facebook_business
```

## 注意事項

- 請確保你的 Meta 開發者賬號已經設置並獲取了必要的 API 訪問權限。
- 保持你的 API 密鑰和訪問令牌的安全，不要將它們提交到版本控制中。
- 創建 .env 文件來存儲敏感數據，並將 .env 添加到 .gitignore。

## 更多資源

- [Meta Business SDK GitHub](https://github.com/facebook/facebook-python-business-sdk)
- [Meta for Developers](https://developers.facebook.com/)
- [Meta Business SDK Documentation](https://developers.facebook.com/docs/marketing-api/sdks)