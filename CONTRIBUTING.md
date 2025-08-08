# 🤝 貢獻指南

感謝您對旅遊產品比對系統的興趣！我們歡迎各種形式的貢獻。

## 🌟 如何貢獻

### 報告問題
1. 檢查是否已有相似的 Issue
2. 使用 Issue 模板描述問題
3. 提供詳細的重現步驟
4. 包含環境資訊和錯誤訊息

### 建議功能
1. 檢查 Issues 和 Projects 看是否已有相關討論
2. 開啟新的 Issue 描述您的想法
3. 說明功能的使用場景和預期效益

### 提交程式碼
1. Fork 此專案
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 遵循程式碼風格指南
4. 撰寫測試（如適用）
5. 提交變更 (`git commit -m 'Add some amazing feature'`)
6. 推送到分支 (`git push origin feature/amazing-feature`)
7. 開啟 Pull Request

## 📝 程式碼風格

### Python 風格
- 遵循 PEP 8 標準
- 使用 `black` 格式化程式碼
- 使用中文註解和文件字串
- 函數名稱使用英文，但加上中文說明

### 檔案結構
```python
def process_data() -> pd.DataFrame:
    """處理資料並返回清理後的 DataFrame
    
    Returns:
        pd.DataFrame: 清理後的資料框
    """
    # 中文註解說明邏輯
    pass
```

### 提交訊息格式
```
類型(範圍): 簡短描述

詳細說明（可選）

關閉 #issue編號（如適用）
```

類型：
- `feat`: 新功能
- `fix`: 錯誤修復
- `docs`: 文件更新
- `style`: 程式碼風格（不影響功能）
- `refactor`: 重構
- `test`: 測試相關
- `chore`: 其他變更

## 🧪 測試

### 本機測試
```bash
# 安裝開發依賴
pip install -r requirements.txt
pip install pytest flake8 black

# 執行程式碼檢查
flake8 .
black --check .

# 測試模組匯入
python -c "from src import file_handler, matcher, translator, utils"
```

### Docker 測試
```bash
# 建立並測試 Docker 映像
docker build -t travel-product-matching .
docker run -p 8080:8080 -e APP_PASSWORD=test_password travel-product-matching
```

## 📋 開發環境設定

### 必要工具
- Python 3.8+
- Git
- VS Code (推薦)

### 推薦擴充功能
- Python
- Black Formatter
- GitLens
- GitHub Copilot

### 環境設定
```bash
# 複製專案
git clone https://github.com/your-username/travel-product-matching.git
cd travel-product-matching

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安裝依賴
pip install -r requirements.txt
```

## 🔍 Code Review 準則

### 提交前檢查
- [ ] 程式碼遵循風格指南
- [ ] 所有測試通過
- [ ] 新功能有適當的文件
- [ ] 沒有明顯的效能問題
- [ ] 變更不會破壞現有功能

### Review 重點
1. **可讀性**: 程式碼是否清晰易懂
2. **正確性**: 邏輯是否正確
3. **效率性**: 是否有效能瓶頸
4. **安全性**: 是否有安全隱患
5. **維護性**: 是否易於維護和擴展

## 🎯 開發優先級

### 高優先級
- 錯誤修復
- 安全性改進
- 效能優化
- 核心功能增強

### 中優先級
- 新功能開發
- 使用者體驗改善
- 文件完善

### 低優先級
- 程式碼重構
- 非必要功能
- 實驗性功能

## 📞 聯絡方式

- **Issues**: 技術問題和錯誤報告
- **Discussions**: 功能討論和想法交流
- **Email**: eztravel.dev@example.com（如有重要問題）

## 🏆 貢獻者

感謝所有為此專案做出貢獻的開發者！

---

再次感謝您的貢獻！每一個改進都讓這個專案變得更好。🙏
