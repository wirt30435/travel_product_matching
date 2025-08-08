# GCP 部署設定指南

## 🚀 部署前準備

### 1. 安裝 Google Cloud CLI
```bash
# Windows
下載並安裝: https://cloud.google.com/sdk/docs/install

# macOS
brew install google-cloud-sdk

# Linux
curl https://sdk.cloud.google.com | bash
```

### 2. 登入並設定專案
```bash
# 登入 GCP
gcloud auth login

# 設定專案 ID（請替換為你的專案 ID）
gcloud config set project YOUR_PROJECT_ID

# 確認設定
gcloud config list
```

### 3. 修改安全設定
在 `app.yaml` 中修改以下設定：

```yaml
env_variables:
  APP_PASSWORD: "your_secure_password_here"  # 改成你的密碼
  SECRET_KEY: "your_secret_key_here"         # 改成隨機字串
```

**建議密碼要求：**
- 至少 8 位字符
- 包含大小寫字母、數字和特殊符號
- 不要使用常見密碼

## 🛠️ 部署步驟

### 自動部署（推薦）
```bash
# Windows
deploy-gcp.bat

# Linux/macOS
./deploy-gcp.sh
```

### 手動部署
```bash
# 1. 啟用必要服務
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable firestore.googleapis.com

# 2. 建立 App Engine 應用
gcloud app create

# 3. 準備檔案
cp main_gcp.py main.py
cp requirements-gcp.txt requirements.txt

# 4. 部署
gcloud app deploy app.yaml

# 5. 清理
rm main.py requirements.txt
```

## 🔧 設定詳解

### App Engine 配置 (app.yaml)

#### 基本設定
- **runtime**: Python 3.11
- **service**: default (主要服務)
- **automatic_scaling**: 自動擴展（0-10 實例）

#### 環境變數
```yaml
env_variables:
  STREAMLIT_SERVER_PORT: 8080        # App Engine 固定端口
  STREAMLIT_SERVER_ADDRESS: 0.0.0.0  # 綁定所有介面
  STREAMLIT_BROWSER_GATHER_USAGE_STATS: false  # 關閉統計
  STREAMLIT_SERVER_HEADLESS: true    # 無頭模式
  APP_PASSWORD: "your_password"       # 存取密碼
  SECRET_KEY: "your_secret_key"       # Session 密鑰
```

#### 資源限制
```yaml
resources:
  cpu: 1          # 1 個 CPU
  memory_gb: 2    # 2GB 記憶體
  disk_size_gb: 10 # 10GB 磁碟
```

### 安全設定 (security_headers.yaml)
- **X-Content-Type-Options**: 防止 MIME 類型混淆
- **X-Frame-Options**: 防止點擊劫持
- **Strict-Transport-Security**: 強制 HTTPS
- **Content-Security-Policy**: 內容安全政策

## 📊 成本估算

### 免費額度（每月）
- **App Engine**: 28 小時實例時間
- **Cloud Storage**: 5GB
- **Cloud Firestore**: 1GB 儲存 + 50K 讀取/20K 寫入
- **網路流量**: 1GB

### 超出免費額度後的收費
- **App Engine F1**: $0.05/小時
- **Cloud Storage**: $0.020/GB
- **Cloud Firestore**: $0.18/GB + $0.06/100K 讀取

### 預估月費用
**輕量使用**（5-10 人，每人每週 2-3 次）:
- App Engine: $0-20
- Storage: $1-5
- Firestore: $0-10
- **總計**: $1-35/月

## 🔐 安全最佳實踐

### 1. 密碼管理
```bash
# 生成強密碼
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 生成 Secret Key
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. 存取控制
- 只給認識的人密碼
- 定期更換密碼（建議每 3 個月）
- 監控使用統計

### 3. 資料保護
- 所有資料傳輸都使用 HTTPS
- 臨時檔案會自動清理
- 不會永久儲存使用者上傳的檔案

## 🔍 監控與除錯

### 查看日誌
```bash
# 查看應用程式日誌
gcloud app logs tail -s default

# 查看特定時間的日誌
gcloud app logs read --since=1h
```

### 效能監控
```bash
# 查看應用程式狀態
gcloud app instances list

# 查看版本資訊
gcloud app versions list
```

### 常見問題除錯

#### 1. 部署失敗
```bash
# 檢查 API 是否啟用
gcloud services list --enabled

# 檢查計費是否啟用
gcloud billing accounts list
```

#### 2. 應用程式無法啟動
```bash
# 檢查日誌錯誤
gcloud app logs tail -s default

# 檢查環境變數
gcloud app versions describe VERSION_ID
```

#### 3. 權限問題
```bash
# 檢查 IAM 權限
gcloud projects get-iam-policy PROJECT_ID

# 新增必要權限
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="user:EMAIL" \
    --role="roles/appengine.deployer"
```

## 📱 使用指南

### 1. 存取應用程式
1. 開啟部署後提供的網址
2. 輸入設定的密碼
3. 開始使用系統

### 2. 分享給朋友
1. 提供應用程式網址
2. 告知存取密碼
3. 簡單說明使用方式

### 3. 維護與更新
```bash
# 更新應用程式
gcloud app deploy app.yaml

# 停止服務（節省費用）
gcloud app versions stop VERSION_ID

# 重新啟動
gcloud app deploy app.yaml
```

## 🆘 緊急處理

### 立即停止服務
```bash
# 停止所有流量
gcloud app services set-traffic default --splits VERSION_ID=0

# 完全停止版本
gcloud app versions stop VERSION_ID
```

### 回復備份
```bash
# 部署先前版本
gcloud app versions list
gcloud app services set-traffic default --splits PREVIOUS_VERSION=100
```

---

**📞 需要協助？**
如有任何問題，請聯繫系統管理員或查看 Google Cloud 官方文檔。
