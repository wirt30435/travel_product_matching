#!/bin/bash

# GCP 部署腳本 - 旅遊產品比對系統
# 使用前請確保已安裝 Google Cloud CLI

echo "================================================"
echo "旅遊產品比對系統 - GCP 部署腳本"
echo "================================================"

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
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable logging.googleapis.com

# 建立 App Engine 應用程式（如果尚未建立）
echo "🏗️ 檢查 App Engine 應用程式..."
if ! gcloud app describe >/dev/null 2>&1; then
    echo "📝 建立 App Engine 應用程式..."
    echo "請選擇地區（建議選擇 asia-east1 或 asia-northeast1）："
    gcloud app create
else
    echo "✅ App Engine 應用程式已存在"
fi

# 複製配置檔案
echo "📁 準備部署檔案..."
cp main_gcp.py main.py
cp requirements-gcp.txt requirements.txt

# 提醒修改密碼
echo "⚠️  重要提醒："
echo "請確保已修改 app.yaml 中的密碼設定："
echo "  - APP_PASSWORD: 存取密碼"
echo "  - SECRET_KEY: Session 密鑰"
echo ""
read -p "是否已修改密碼設定？(y/N): " confirm

if [[ $confirm != [yY] ]]; then
    echo "❌ 請先修改 app.yaml 中的密碼設定後再執行部署"
    exit 1
fi

# 部署到 App Engine
echo "🚀 開始部署到 App Engine..."
gcloud app deploy app.yaml --quiet

# 取得應用程式網址
APP_URL=$(gcloud app browse --no-launch-browser)
echo ""
echo "================================================"
echo "🎉 部署完成！"
echo "📱 應用程式網址: $APP_URL"
echo "🔐 記得使用設定的密碼登入"
echo "================================================"

# 清理暫時檔案
rm -f main.py requirements.txt

echo "✅ 部署腳本執行完成"
