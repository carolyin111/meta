# Meta API 自動化工具

這個專案提供了一套工具，用於自動化 Facebook 頁面和 Instagram 內容的管理，包括發布貼文、排程內容、獲取分析數據等功能。

## 目錄

- [環境設置](#環境設置)
- [Facebook 頁面管理](#facebook-頁面管理)
- [Instagram 內容發布](#instagram-內容發布)
- [令牌管理](#令牌管理)
- [故障排除](#故障排除)

## 環境設置

### 先決條件

- Python 3.7 或更高版本
- Meta Facebook Business SDK
- Meta 開發者帳戶和應用程序
- Facebook 頁面管理權限
- Instagram 商業或創作者帳戶（與 Facebook 頁面關聯）

### 安裝

1. 克隆此代碼庫：
   ```bash
   git clone https://github.com/yourusername/meta-automation.git
   cd meta-automation
   ```

2. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```

3. 設置環境變數，創建 `config/.env` 文件：
   ```
   APP_ID=your_app_id
   APP_SECRET=your_app_secret
   ACCESS_TOKEN=your_user_access_token
   PAGE_ID=your_page_id
   ```

## Facebook 頁面管理

### 獲取頁面信息和發布貼文

`scripts/page.py` 腳本用於管理 Facebook 頁面，包括獲取頁面信息、發布貼文和排程貼文。

```bash
# 運行頁面管理腳本
python scripts/page.py
```

這個腳本會：
1. 獲取頁面基本信息
2. 顯示最近的貼文
3. 發布一條新貼文
4. 創建一條排程貼文（24小時後發布）
5. 獲取與頁面關聯的 Instagram 帳戶信息

### 列出所有關聯的業務頁面

```bash
# 列出與您的帳戶關聯的所有業務頁面
python scripts/list_business_pages.py
```

## Instagram 內容發布

`scripts/instagram_publisher.py` 提供了一個強大的工具，用於在 Instagram 上發布和排程各種類型的內容。

### 查看最近的 Instagram 貼文

```bash
# 查看最近的 5 篇貼文
python scripts/instagram_publisher.py view

# 查看最近的 10 篇貼文
python scripts/instagram_publisher.py view --limit 10
```

### 發布圖片

```bash
# 發布單張圖片
python scripts/instagram_publisher.py image --url "https://example.com/image.jpg" --caption "我的測試圖片 #test"
```

### 發布影片

```bash
# 發布普通影片
python scripts/instagram_publisher.py video --url "https://example.com/video.mp4" --caption "我的測試影片"

# 發布 Reels
python scripts/instagram_publisher.py video --url "https://example.com/video.mp4" --caption "我的 Reels" --type REELS

# 發布 Stories
python scripts/instagram_publisher.py video --url "https://example.com/video.mp4" --caption "我的 Stories" --type STORIES --cover "https://example.com/cover.jpg"
```

### 發布輪播 (Carousel)

```bash
# 發布多張圖片的輪播
python scripts/instagram_publisher.py carousel --urls "https://example.com/image1.jpg" "https://example.com/image2.jpg" "https://example.com/image3.jpg" --caption "我的輪播貼文 #carousel"
```

### 排程貼文

```bash
# 排程圖片貼文 (24小時後發布)
python scripts/instagram_publisher.py schedule --type IMAGE --content "https://example.com/image.jpg" --caption "排程的圖片貼文"

# 排程影片貼文 (指定時間發布)
python scripts/instagram_publisher.py schedule --type VIDEO --content "https://example.com/video.mp4" --caption "排程的影片貼文" --time 1745019000 --upload-type REELS

# 排程輪播貼文
python scripts/instagram_publisher.py schedule --type CAROUSEL --content "https://example.com/image1.jpg" "https://example.com/image2.jpg" --caption "排程的輪播貼文"
```

### 啟用調試模式

添加 `--debug` 參數可以啟用調試模式，顯示更多的執行信息：

```bash
python scripts/instagram_publisher.py video --url "https://example.com/video.mp4" --caption "測試" --debug
```

## 令牌管理

本專案內建了智能令牌管理系統，可以自動處理 Meta API 的認證令牌，包括獲取、刷新和存儲令牌。

### 查看令牌信息

```bash
# 顯示所有存儲的令牌信息
python scripts/instagram_publisher.py tokens
```

### 刷新令牌

```bash
# 強制刷新所有令牌
python scripts/instagram_publisher.py tokens --refresh
```

令牌管理系統會：
- 自動將短期用戶令牌轉換為長期令牌（60天有效期）
- 存儲令牌到 `config/tokens.json` 文件中
- 在需要時自動刷新令牌
- 顯示令牌的剩餘有效期

## 文件結構

- `config/` - 配置文件和令牌存儲
  - `config.py` - 配置管理
  - `tokens.json` - 令牌存儲
- `scripts/` - 執行腳本
  - `page.py` - Facebook 頁面管理
  - `instagram_publisher.py` - Instagram 內容發布
  - `list_business_pages.py` - 列出業務頁面
  - `business.py` - 業務帳號操作
- `src/` - 核心功能模塊
  - `token_manager.py` - 令牌管理
  
## 故障排除

### 權限錯誤

如果遇到 "Insufficient permissions" 或 "Invalid permissions" 錯誤，請確保您的應用有以下權限：
- `pages_read_engagement`
- `pages_manage_posts`
- `pages_show_list`
- `instagram_basic`
- `instagram_content_publish`

### 令牌過期

如果遇到 "Error validating access token" 錯誤，請使用令牌刷新工具：
```bash
python scripts/instagram_publisher.py tokens --refresh
```

### 媒體上傳問題

- 確保 URL 是直接可訪問的，不需要登錄（不能使用 Google Drive 或需要驗證的鏈接）
- 圖片格式支持：JPG, PNG
- 影片格式支持：MP4
- 檢查影片分辨率和長度是否符合 Instagram 要求