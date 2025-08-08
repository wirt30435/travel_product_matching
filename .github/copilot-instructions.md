<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# 旅遊產品比對系統 - Copilot 指令

## 專案概述
這是一個基於 Streamlit 的旅遊產品比對網頁應用程式，用於比較兩個供應商的產品並找出相似商品。

## 技術規範
- **前端框架**: Streamlit
- **資料處理**: Pandas
- **檔案格式**: CSV, Excel
- **比對算法**: Jaccard 相似度
- **翻譯服務**: Google Translate
- **Python 版本**: 3.8+

## 程式碼風格指南
- 使用中文註解和變數名稱
- 函數名稱使用英文，但加上中文說明
- 遵循 PEP 8 程式碼風格
- 使用 type hints
- 加入適當的錯誤處理

## 核心功能
1. 檔案上傳 (CSV/Excel)
2. 資料預覽 (前10筆)
3. 產品名稱翻譯
4. Jaccard 相似度比對
5. 結果展示和匯出

## 重要提醒
- 注重使用者體驗和介面友善性
- 確保檔案處理的安全性
- 提供清楚的錯誤訊息
- 支援中英文產品名稱
