@echo off
chcp 65001 > nul

echo ================================================
echo 旅遊產品比對系統 - 本機啟動腳本
echo ================================================

REM 檢查 Python 是否已安裝
echo 🔍 檢查 Python 環境...
where python >nul 2>&1
if errorlevel 1 (
    echo ❌ 尚未安裝 Python
    echo 請前往 https://www.python.org/downloads/ 安裝 Python 3.8+
    pause
    exit /b 1
)

REM 如果存在 Pipfile，優先使用 pipenv 啟動
if exist "Pipfile" (
    echo 🔧 偵測到 Pipfile，使用 pipenv 啟動...
    pipenv --version >nul 2>&1
    if errorlevel 1 (
        echo 📦 安裝 pipenv...
        pip install --upgrade pip
        pip install pipenv
    )
    echo 📦 安裝相依套件（pipenv）...
    pipenv install
    echo 🚀 啟動應用程式...
    pipenv run streamlit run app.py --browser.serverAddress=localhost --server.address=localhost
    goto :end
)

REM 否則使用 venv + requirements.txt
if not exist "venv" (
    echo 📦 建立虛擬環境...
    python -m venv venv
)

echo 🚀 啟動虛擬環境...
call venv\Scripts\activate.bat

echo 📦 更新 pip 並安裝相依套件...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo 🚀 啟動應用程式...
streamlit run app.py --browser.serverAddress=localhost --server.address=localhost

:end
pause