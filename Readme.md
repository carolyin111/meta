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

## 如何使用此專案

本專案提供了完整的工具來與 Meta Business API 進行交互，並分析廣告數據。以下是使用此專案的完整步驟：

### 1. 設置您的憑證

首先，需要設置您的 Meta API 憑證：

```bash
# 將模板文件複製並填入您的憑證
cp config/.env.template config/.env
# 編輯 .env 文件，填入您的憑證信息
```

### 2. 安裝依賴項

確保已激活虛擬環境，然後安裝所需的依賴項：

```bash
# 在專案根目錄中
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 運行示例腳本

我們提供了兩個示例腳本來展示如何使用此專案：

```bash
# 基本使用示例
./scripts/example_usage.py

# 生成廣告洞察報告
./scripts/generate_insights_report.py --days 30 --level ad_account
```

### 4. 生成特定級別的報告

您可以生成特定廣告活動、廣告組或廣告的報告：

```bash
# 廣告活動級別報告
./scripts/generate_insights_report.py --level campaign --id 您的廣告活動ID --output campaign_report.csv

# 廣告組級別報告
./scripts/generate_insights_report.py --level adset --id 您的廣告組ID --output adset_report.csv

# 廣告級別報告
./scripts/generate_insights_report.py --level ad --id 您的廣告ID --output ad_report.csv
```

### 5. 自定義您的代碼

專案結構是模塊化的，您可以根據需要擴展它：

- `src/meta_client.py` - 添加更多方法來與 Meta API 交互
- `src/insights_helper.py` - 擴展數據分析功能
- `scripts/` - 創建更多特定任務的腳本

### 6. 數據分析與報告

生成的 CSV 報告可以使用 Excel、Google Sheets 或其他數據分析工具進行進一步分析。報告包含所有關鍵的廣告表現指標，如：

- 曝光量和點擊量
- 花費和轉化數
- CTR、CPC 和轉化率
- 參與度排名和質量排名

## 注意事項

- 請確保你的 Meta 開發者賬號已經設置並獲取了必要的 API 訪問權限。
- 保持你的 API 密鑰和訪問令牌的安全，不要將它們提交到版本控制中。
- 創建 .env 文件來存儲敏感數據，並將 .env 添加到 .gitignore。

## 更多資源

- [Meta Business SDK GitHub](https://github.com/facebook/facebook-python-business-sdk)
- [Meta for Developers](https://developers.facebook.com/)
- [Meta Business SDK Documentation](https://developers.facebook.com/docs/marketing-api/sdks)