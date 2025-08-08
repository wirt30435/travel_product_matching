# 🧳 旅遊產品比對系統 Web 版本 - 使用說明

## 🎉 恭喜！專案已成功建立

你的旅遊產品比對系統 Web 版本已經準備就緒！這是一個基於 Streamlit 的現代化網頁應用程式。

## 🚀 快速啟動

### 1. 啟動應用程式

- 方法 1: 使用批次檔（推薦）
  - 直接雙擊 `start.bat`
- 方法 2: 手動啟動（已安裝 pipenv 可用）
  - 使用 pipenv 啟動：`pipenv run streamlit run app.py`
  - 或使用虛擬環境後：`streamlit run app.py`

### 2. 開啟網頁
- 應用程式啟動後會自動開啟瀏覽器
- 或手動開啟：http://localhost:8501

## 📁 專案結構

```
travel_product_matching_public/
├── app.py                    # 🌟 主應用程式（本機）
├── main_gcp.py               # ☁️ 雲端入口（Cloud Run）
├── src/                      # 📦 核心模組
│   ├── file_handler.py       # 📁 檔案處理
│   ├── translator.py         # 🌐 翻譯服務
│   ├── matcher.py            # 🔍 比對邏輯
│   └── utils.py              # 🛠️ 工具函數（含 setup_logging）
├── data/                     # 📊 範例資料
│   ├── vendor_A_sample.csv   # 供應商A範例
│   └── vendor_B_sample.csv   # 供應商B範例
├── requirements.txt          # 📋 本機依賴
├── requirements-gcp.txt      # 📋 雲端依賴（Cloud Run）
├── Dockerfile                # 🐳 Docker 設定
├── .streamlit/config.toml    # ⚙️ Streamlit 設定（不硬編碼 port）
├── Pipfile / Pipfile.lock    # 🐍 Pipenv 配置與鎖定
└── README.md                 # 📖 說明文件
```

## ✨ 功能特色

- 檔案上傳（CSV/Excel）與格式驗證
- 中文產品名稱翻譯（deep-translator）
- Jaccard 相似度比對與參數調整
- 視覺化分析與結果匯出（CSV/Excel）

## 🎯 使用流程

1. 上傳兩個供應商檔案
2. 檢查資料摘要與品質
3. 設定相似度門檻與翻譯選項
4. 執行比對
5. 檢視統計與圖表
6. 匯出結果

## 🐛 疑難排解

- 檔案上傳失敗：確認格式與必要欄位
- 翻譯出錯：檢查網路並可在 UI 清除翻譯快取
- 比對為空：降低相似度門檻，確認國家欄位一致

## 📞 技術支援自檢

- Python 環境設定正確
- 依賴已完整安裝
- 網路連線正常
- 檔案格式與欄位正確

---

🚀 立即啟動 `start.bat`，上傳你的產品檔案並開始比對！
