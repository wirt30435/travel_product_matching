"""
GCP 版本的主應用程式
包含密碼保護功能
"""

import streamlit as st
import os
from datetime import datetime, timedelta

# 導入原有模組
try:
    from src.file_handler import FileHandler
    from src.matcher import ProductMatcher
    from src.translator import TranslationService
    from src.utils import setup_logging
except ImportError as e:
    st.error(f"模組載入失敗: {e}")
    st.stop()

# 設定頁面
st.set_page_config(
    page_title="旅遊產品比對系統",
    page_icon="🧳",
    layout="wide",
    initial_sidebar_state="expanded"
)


def check_password():
    """檢查密碼"""
    def password_entered():
        """檢查輸入的密碼"""
        app_password = os.getenv('APP_PASSWORD')
        if not app_password:
            st.error("⚠️ 系統配置錯誤：未設定存取密碼。請聯絡系統管理員。")
            st.stop()
        
        if st.session_state.get("password", "") == app_password:
            st.session_state["password_correct"] = True
            st.session_state["login_time"] = datetime.now()
            st.session_state.pop("password", None)  # 清除密碼
        else:
            st.session_state["password_correct"] = False

    # 檢查是否已登入且未過期（24小時）
    if st.session_state.get("password_correct"):
        login_time = st.session_state.get("login_time", datetime.now())
        if datetime.now() - login_time < timedelta(hours=24):
            return True
        else:
            # 登入過期，清除狀態
            st.session_state.pop("password_correct", None)
            st.session_state.pop("login_time", None)

    # 顯示登入表單
    st.markdown("# 🔐 旅遊產品比對系統")
    st.markdown("## 請輸入存取密碼")

    st.text_input(
        "密碼",
        type="password",
        on_change=password_entered,
        key="password",
        help="請聯繫系統管理員取得密碼"
    )

    if st.session_state.get("password_correct") is False:
        st.error("密碼錯誤，請重新輸入")

    return False


def add_usage_tracking():
    """添加使用統計"""
    if "usage_count" not in st.session_state:
        st.session_state.usage_count = 0

    # 在側邊欄顯示使用統計
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"**本次 Session 使用次數**: {st.session_state.usage_count}")
        st.markdown(f"**登入時間**: {st.session_state.get('login_time', '未知')}")


def main():
    """主應用程式"""
    # 設定日誌（在任何 UI 前呼叫）
    setup_logging()

    # 檢查密碼
    if not check_password():
        st.stop()

    # 添加使用統計
    add_usage_tracking()

    # 主標題
    st.title("🧳 旅遊產品比對系統")
    st.markdown("### 智慧比對，精準分析")

    # 建立分頁
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 檔案上傳",
        "👀 資料預覽",
        "🔍 執行比對",
        "📊 結果分析"
    ])

    # 初始化處理器
    file_handler = FileHandler()

    with tab1:
        st.header("📁 檔案上傳")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("供應商 A")
            uploaded_file_a = st.file_uploader(
                "選擇供應商 A 的檔案",
                type=['csv', 'xlsx', 'xls'],
                key="file_a",
                help="支援 CSV 和 Excel 格式"
            )

            if uploaded_file_a:
                try:
                    df_a = file_handler.read_file(uploaded_file_a)
                    if df_a is None:
                        raise ValueError("檔案格式或內容不正確")
                    st.session_state.df_a = file_handler.standardize_columns(df_a)
                    st.success(f"✅ 檔案載入成功！共 {len(df_a)} 筆資料")
                except Exception as e:
                    st.error(f"❌ 檔案載入失敗: {str(e)}")

        with col2:
            st.subheader("供應商 B")
            uploaded_file_b = st.file_uploader(
                "選擇供應商 B 的檔案",
                type=['csv', 'xlsx', 'xls'],
                key="file_b",
                help="支援 CSV 和 Excel 格式"
            )

            if uploaded_file_b:
                try:
                    df_b = file_handler.read_file(uploaded_file_b)
                    if df_b is None:
                        raise ValueError("檔案格式或內容不正確")
                    st.session_state.df_b = file_handler.standardize_columns(df_b)
                    st.success(f"✅ 檔案載入成功！共 {len(df_b)} 筆資料")
                except Exception as e:
                    st.error(f"❌ 檔案載入失敗: {str(e)}")

    with tab2:
        st.header("👀 資料預覽")

        if 'df_a' in st.session_state and 'df_b' in st.session_state:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("供應商 A - 前10筆資料")
                st.dataframe(file_handler.get_data_preview(st.session_state.df_a, 10))

            with col2:
                st.subheader("供應商 B - 前10筆資料")
                st.dataframe(file_handler.get_data_preview(st.session_state.df_b, 10))
        else:
            st.info("📝 請先在「檔案上傳」分頁中上傳兩個檔案")

    with tab3:
        st.header("🔍 執行比對")

        if 'df_a' in st.session_state and 'df_b' in st.session_state:
            # 比對參數設定
            col1, col2 = st.columns(2)

            with col1:
                similarity_threshold = st.slider(
                    "相似度門檻",
                    min_value=0.1,
                    max_value=1.0,
                    value=0.5,
                    step=0.1,
                    help="低於此門檻的比對結果將被過濾"
                )

            with col2:
                translate_names = st.checkbox(
                    "翻譯產品名稱",
                    value=True,
                    help="將中文產品名稱翻譯成英文進行比對"
                )

            # 執行比對按鈕
            if st.button("🚀 開始比對", type="primary"):
                with st.spinner("正在執行比對，請稍候..."):
                    try:
                        # 增加使用次數
                        st.session_state.usage_count += 1

                        # 初始化比對器
                        matcher = ProductMatcher(similarity_threshold=similarity_threshold)
                        translator = TranslationService() if translate_names else None

                        # 執行比對
                        results = matcher.compare_products(
                            st.session_state.df_a,
                            st.session_state.df_b,
                            similarity_threshold=similarity_threshold,
                            translator=translator
                        )

                        st.session_state.results = results
                        st.success("✅ 比對完成！")

                        # 顯示基本統計
                        st.info(f"📊 找到 {len(results)} 組相似產品")

                    except Exception as e:
                        st.error(f"❌ 比對過程發生錯誤: {str(e)}")
        else:
            st.info("📝 請先在「檔案上傳」分頁中上傳兩個檔案")

    with tab4:
        st.header("📊 結果分析")

        if 'results' in st.session_state:
            results = st.session_state.results

            if len(results) > 0:
                # 顯示結果表格
                st.subheader("🔍 比對結果")
                st.dataframe(results)

                # 下載按鈕
                col1, col2 = st.columns(2)

                with col1:
                    csv_data = file_handler.export_to_csv(results)
                    st.download_button(
                        label="📥 下載 CSV",
                        data=csv_data,
                        file_name=f"比對結果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )

                with col2:
                    excel_data = file_handler.export_to_excel(results)
                    st.download_button(
                        label="📥 下載 Excel",
                        data=excel_data,
                        file_name=f"比對結果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                # 分析統計
                st.subheader("📈 統計分析")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("總比對數", len(results))

                with col2:
                    avg_similarity = results['jaccard_score'].mean() if 'jaccard_score' in results else 0
                    st.metric("平均相似度", f"{avg_similarity:.2%}")

                with col3:
                    high_similarity = len(results[results['jaccard_score'] > 0.8]) if 'jaccard_score' in results else 0
                    st.metric("高相似度 (>80%)", high_similarity)

            else:
                st.warning("⚠️ 沒有找到符合條件的相似產品")
        else:
            st.info("📝 請先在「執行比對」分頁中完成比對")


if __name__ == "__main__":
    main()
