# 🔐 環境變數配置指南

本文件說明如何安全地設定系統所需的環境變數。

## 📋 必要環境變數

### APP_PASSWORD
- **用途**: 系統存取密碼保護
- **格式**: 字串
- **建議**: 使用強密碼（至少12個字元，包含大小寫字母、數字和特殊符號）

## 🛠️ 設定方法

### 本機開發環境

#### 方法一：使用 .env 檔案 (推薦)
1. 在專案根目錄建立 `.env` 檔案：
```bash
APP_PASSWORD=your_secure_password_here
```

2. 安裝 python-dotenv：
```bash
pip install python-dotenv
```

3. 在程式中載入（已整合到專案中）

#### 方法二：系統環境變數

**Windows:**
```powershell
# 臨時設定（當前 session）
$env:APP_PASSWORD="your_secure_password_here"

# 永久設定
[Environment]::SetEnvironmentVariable("APP_PASSWORD", "your_secure_password_here", "User")
```

**Linux/macOS:**
```bash
# 臨時設定（當前 session）
export APP_PASSWORD="your_secure_password_here"

# 永久設定（加入到 ~/.bashrc 或 ~/.zshrc）
echo 'export APP_PASSWORD="your_secure_password_here"' >> ~/.bashrc
source ~/.bashrc
```

### Docker 部署

```bash
# 使用環境變數檔案
docker run --env-file .env -p 8080:8080 travel-product-matching

# 直接指定環境變數
docker run -e APP_PASSWORD="your_secure_password_here" -p 8080:8080 travel-product-matching
```

### Google Cloud Run 部署

```bash
# 使用 gcloud CLI
gcloud run deploy travel-product-matching \
  --source . \
  --region=asia-east1 \
  --set-env-vars=APP_PASSWORD="your_secure_password_here" \
  --allow-unauthenticated

# 使用 Cloud Console
# 1. 前往 Cloud Run 服務
# 2. 選擇您的服務
# 3. 點擊「編輯和部署新版本」
# 4. 在「變數和密鑰」分頁中新增環境變數
# 5. 名稱：APP_PASSWORD，值：your_secure_password_here
```

## 🔒 安全性最佳實務

### 密碼強度建議
- **長度**: 至少 12 個字元
- **複雜度**: 包含大小寫字母、數字、特殊符號
- **避免**: 字典單詞、個人資訊、常見密碼

### 範例強密碼
```bash
# 好的密碼範例
APP_PASSWORD="Tr@v3l_M@tch1ng_2025!"
APP_PASSWORD="$yst3m_Pr0t3ct10n#2025"
APP_PASSWORD="Eztr@v3l_S3cur3_K3y!"
```

### 安全性檢查清單
- [ ] 不在程式碼中硬編碼密碼
- [ ] 不在 README 或文件中暴露實際密碼
- [ ] 使用 `.env` 檔案且加入 `.gitignore`
- [ ] 定期更換密碼
- [ ] 使用不同環境不同密碼（開發/測試/生產）

## 🚫 常見錯誤

### ❌ 不要這樣做
```python
# 硬編碼密碼
password = "eztravel_activity"

# 在 README 中暴露實際密碼
**存取密碼**: eztravel_activity
```

### ✅ 正確的做法
```python
# 使用環境變數
password = os.getenv('APP_PASSWORD', 'default_password')

# 在 README 中的說明
**存取密碼**: 請聯絡專案維護者取得存取密碼
```

## 🔄 密碼輪換

### 建議頻率
- **開發環境**: 每月
- **測試環境**: 每週
- **生產環境**: 每週或發生安全事件時立即更換

### 輪換步驟
1. 產生新的強密碼
2. 更新環境變數設定
3. 重新部署服務
4. 通知相關使用者
5. 撤銷舊密碼存取權限

## 📞 問題排解

### 常見問題
**Q: 環境變數設定後系統仍提示密碼錯誤？**
- 檢查環境變數名稱是否正確 (`APP_PASSWORD`)
- 確認沒有多餘的空格或特殊字元
- 重新啟動應用程式

**Q: Docker 容器無法讀取環境變數？**
- 確認使用 `-e` 參數或 `--env-file` 正確傳遞
- 檢查 .env 檔案格式是否正確

**Q: Cloud Run 部署後密碼不生效？**
- 確認環境變數已正確設定在 Cloud Run 服務中
- 檢查服務是否已重新部署

---

⚠️ **重要提醒**: 絕對不要將實際密碼提交到版本控制系統中！
