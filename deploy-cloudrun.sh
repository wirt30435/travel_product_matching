#!/bin/bash

# Cloud Run 部署腳本 - 旅遊產品比對系統
# 使用前請確保已安裝 Google Cloud CLI

echo "================================================"
echo "旅遊產品比對系統 - Cloud Run 部署腳本"
echo "================================================"

# 設定變數
SERVICE_NAME="travel-product-matching"
REGION="asia-east1"
PLATFORM="linux/amd64"

# 檢查是否已登入 GCP
echo "🔍 檢查 GCP 登入狀態..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo "❌ 尚未登入 GCP，請先執行: gcloud auth login"
    exit 1
fi

# 檢查是否設定專案
echo "🔍 檢查 GCP 專案設定..."
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ 尚未設定 GCP 專案，請先執行: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "✅ 目前專案: $PROJECT_ID"

# 啟用必要的 API
echo "🚀 啟用必要的 API 服務..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# 提示設定密碼
echo ""
echo "🔐 安全性設定"
echo "=============================================="
echo "⚠️  重要：請設定一個安全的存取密碼"
echo "建議密碼要求：至少12個字元，包含大小寫字母、數字和特殊符號"
echo ""

# 讀取密碼
while true; do
    read -s -p "請輸入存取密碼: " APP_PASSWORD
    echo ""
    read -s -p "請再次確認密碼: " APP_PASSWORD_CONFIRM
    echo ""
    
    if [ "$APP_PASSWORD" = "$APP_PASSWORD_CONFIRM" ]; then
        if [ ${#APP_PASSWORD} -lt 8 ]; then
            echo "❌ 密碼長度至少需要8個字元，請重新設定"
            continue
        fi
        break
    else
        echo "❌ 兩次輸入的密碼不一致，請重新設定"
    fi
done

echo "✅ 密碼設定完成"

# 部署到 Cloud Run
echo ""
echo "🚀 開始部署到 Cloud Run..."
echo "=============================================="

gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars APP_PASSWORD="$APP_PASSWORD" \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300

# 檢查部署結果
if [ $? -eq 0 ]; then
    # 取得服務網址
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')
    
    echo ""
    echo "================================================"
    echo "🎉 部署成功！"
    echo "📱 服務網址: $SERVICE_URL"
    echo "🔐 存取密碼: [已設定，請妥善保管]"
    echo "⏰ 服務通常需要幾分鐘才會完全啟用"
    echo "================================================"
    echo ""
    echo "📝 下一步："
    echo "1. 前往服務網址測試應用程式"
    echo "2. 使用剛才設定的密碼登入"
    echo "3. 如需修改密碼，請重新執行此腳本"
    echo ""
else
    echo "❌ 部署失敗，請檢查錯誤訊息"
    exit 1
fi

echo "✅ 部署腳本執行完成"
