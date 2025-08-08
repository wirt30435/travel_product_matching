#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旅遊產品比對系統 Web 應用程式
使用 Streamlit 框架建立的網頁介面
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# 添加 src 目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from file_handler import FileHandler
    from translator import TranslationService
    from matcher import ProductMatcher
    from utils import (
        display_data_summary, display_missing_values, validate_data_quality,
        create_similarity_chart, create_price_difference_chart, 
        create_similarity_vs_price_chart, format_currency
    )
except ImportError as e:
    st.error(f"模組匯入錯誤: {e}")
    st.stop()

# 頁面配置
st.set_page_config(
    page_title="旅遊產品比對系統",
    page_icon="🧳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .result-section {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """初始化 session state"""
    if 'df_a' not in st.session_state:
        st.session_state.df_a = None
    if 'df_b' not in st.session_state:
        st.session_state.df_b = None
    if 'matched_results' not in st.session_state:
        st.session_state.matched_results = None
    if 'translation_service' not in st.session_state:
        st.session_state.translation_service = TranslationService()

def main():
    """主函數"""
    initialize_session_state()
    
    # 標題
    st.markdown('<h1 class="main-header">🧳 旅遊產品比對系統</h1>', unsafe_allow_html=True)
    st.markdown("### 比較兩個供應商的旅遊產品，找出相似商品並分析價格差異")
    
    # 側邊欄設定
    with st.sidebar:
        st.header("⚙️ 比對參數設定")
        
        similarity_threshold = st.slider(
            "相似度門檻",
            min_value=0.1,
            max_value=1.0,
            value=0.2,
            step=0.1,
            help="只顯示相似度大於此門檻的結果"
        )
        
        max_token_diff = st.slider(
            "最大詞彙數量差異",
            min_value=1,
            max_value=10,
            value=5,
            help="詞彙數量差異超過此值將跳過比較"
        )
        
        st.header("📊 檔案格式說明")
        st.info("""
        **必要欄位:**
        - product_id (產品ID)
        - product_name (產品名稱)
        - product_location_country (國家)
        - price (價格)
        
        **支援格式:** CSV, Excel (.xlsx/.xls)
        """)
    
    # 主要內容區域
    tab1, tab2, tab3, tab4 = st.tabs(["📁 檔案上傳", "👀 資料預覽", "🔍 執行比對", "📈 結果分析"])
    
    with tab1:
        upload_files_section()
    
    with tab2:
        preview_data_section()
    
    with tab3:
        matching_section(similarity_threshold, max_token_diff)
    
    with tab4:
        results_analysis_section()

def upload_files_section():
    """檔案上傳區域"""
    st.header("📁 檔案上傳")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.subheader("📤 供應商 A")
        uploaded_file_a = st.file_uploader(
            "選擇供應商 A 的產品檔案",
            type=['csv', 'xlsx', 'xls'],
            key="file_a",
            help="上傳 CSV 或 Excel 檔案"
        )
        
        if uploaded_file_a:
            with st.spinner("正在處理檔案 A..."):
                df_a = FileHandler.read_file(uploaded_file_a)
                if df_a is not None:
                    is_valid, missing_cols = FileHandler.validate_columns(df_a)
                    if is_valid:
                        st.session_state.df_a = FileHandler.standardize_columns(df_a)
                        st.success(f"✅ 檔案 A 上傳成功！共 {len(df_a)} 筆資料")
                    else:
                        st.error(f"❌ 檔案 A 缺少必要欄位: {', '.join(missing_cols)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.subheader("📤 供應商 B")
        uploaded_file_b = st.file_uploader(
            "選擇供應商 B 的產品檔案",
            type=['csv', 'xlsx', 'xls'],
            key="file_b",
            help="上傳 CSV 或 Excel 檔案"
        )
        
        if uploaded_file_b:
            with st.spinner("正在處理檔案 B..."):
                df_b = FileHandler.read_file(uploaded_file_b)
                if df_b is not None:
                    is_valid, missing_cols = FileHandler.validate_columns(df_b)
                    if is_valid:
                        st.session_state.df_b = FileHandler.standardize_columns(df_b)
                        st.success(f"✅ 檔案 B 上傳成功！共 {len(df_b)} 筆資料")
                    else:
                        st.error(f"❌ 檔案 B 缺少必要欄位: {', '.join(missing_cols)}")
        st.markdown('</div>', unsafe_allow_html=True)

def preview_data_section():
    """資料預覽區域"""
    st.header("👀 資料預覽")
    
    if st.session_state.df_a is None and st.session_state.df_b is None:
        st.info("📝 請先上傳檔案來預覽資料")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.df_a is not None:
            st.subheader("📊 供應商 A - 前10筆資料")
            display_data_summary(st.session_state.df_a, "供應商 A 摘要")
            
            # 資料品質檢查
            issues_a = validate_data_quality(st.session_state.df_a)
            if issues_a:
                st.warning("⚠️ 資料品質問題:")
                for issue in issues_a:
                    st.write(f"  - {issue}")
            
            preview_a = FileHandler.get_data_preview(st.session_state.df_a, 10)
            st.dataframe(preview_a, use_container_width=True)
            
            display_missing_values(st.session_state.df_a)
        else:
            st.info("📝 請上傳供應商 A 的檔案")
    
    with col2:
        if st.session_state.df_b is not None:
            st.subheader("📊 供應商 B - 前10筆資料")
            display_data_summary(st.session_state.df_b, "供應商 B 摘要")
            
            # 資料品質檢查
            issues_b = validate_data_quality(st.session_state.df_b)
            if issues_b:
                st.warning("⚠️ 資料品質問題:")
                for issue in issues_b:
                    st.write(f"  - {issue}")
            
            preview_b = FileHandler.get_data_preview(st.session_state.df_b, 10)
            st.dataframe(preview_b, use_container_width=True)
            
            display_missing_values(st.session_state.df_b)
        else:
            st.info("📝 請上傳供應商 B 的檔案")

def matching_section(similarity_threshold: float, max_token_diff: int):
    """比對執行區域"""
    st.header("🔍 執行比對")
    
    if st.session_state.df_a is None or st.session_state.df_b is None:
        st.info("📝 請先上傳兩個供應商的檔案才能進行比對")
        return
    
    st.info(f"""
    **比對設定:**
    - 相似度門檻: {similarity_threshold}
    - 最大詞彙差異: {max_token_diff}
    - 供應商 A: {len(st.session_state.df_a)} 筆產品
    - 供應商 B: {len(st.session_state.df_b)} 筆產品
    """)
    
    # 翻譯選項
    col1, col2 = st.columns(2)
    with col1:
        translate_option = st.radio(
            "翻譯選項",
            ["自動翻譯產品名稱", "假設已為英文"],
            help="選擇是否需要將中文產品名稱翻譯為英文"
        )
    
    with col2:
        if st.button("🗑️ 清除翻譯快取"):
            st.session_state.translation_service.clear_cache()
    
    # 執行比對按鈕
    if st.button("🚀 開始比對", type="primary", use_container_width=True):
        with st.spinner("正在執行產品比對..."):
            # 準備資料
            df_a_work = st.session_state.df_a.copy()
            df_b_work = st.session_state.df_b.copy()
            
            # 翻譯處理
            if translate_option == "自動翻譯產品名稱":
                st.info("🔤 正在翻譯產品名稱...")
                
                # 翻譯供應商 A
                df_a_work['product_name_en'] = st.session_state.translation_service.translate_batch(
                    df_a_work['product_name'].tolist(), show_progress=True
                )
                
                # 翻譯供應商 B
                df_b_work['product_name_en'] = st.session_state.translation_service.translate_batch(
                    df_b_work['product_name'].tolist(), show_progress=True
                )
            else:
                # 假設產品名稱已為英文
                df_a_work['product_name_en'] = df_a_work['product_name']
                df_b_work['product_name_en'] = df_b_work['product_name']
            
            # 執行比對
            st.info("🎯 正在進行產品比對...")
            matcher = ProductMatcher(similarity_threshold, max_token_diff)
            matched_results = matcher.compare_products(df_a_work, df_b_work, show_progress=True)
            
            # 儲存結果
            st.session_state.matched_results = matched_results
            
            if len(matched_results) > 0:
                st.success(f"🎉 比對完成！找到 {len(matched_results)} 組相似產品")
                
                # 顯示前10筆結果預覽
                st.subheader("📋 比對結果預覽 (前10筆)")
                preview_columns = [
                    'product_location_country', 'vendor_A_product_name', 
                    'vendor_B_product_name', 'jaccard_score', 'price_diff'
                ]
                st.dataframe(
                    matched_results[preview_columns].head(10),
                    use_container_width=True
                )
            else:
                st.warning("⚠️ 未找到符合條件的相似產品，請嘗試降低相似度門檻")

def results_analysis_section():
    """結果分析區域"""
    st.header("📈 結果分析")
    
    if st.session_state.matched_results is None:
        st.info("📝 請先執行產品比對來查看分析結果")
        return
    
    matched_df = st.session_state.matched_results
    
    if len(matched_df) == 0:
        st.warning("⚠️ 沒有比對結果可供分析")
        return
    
    # 統計摘要
    matcher = ProductMatcher()
    analysis = matcher.analyze_results(matched_df)
    
    # 顯示關鍵指標
    st.subheader("🎯 關鍵指標")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("總比對數", analysis['total_matches'])
    with col2:
        st.metric("涵蓋國家", analysis['unique_countries'])
    with col3:
        st.metric("平均相似度", f"{analysis['avg_similarity']:.3f}")
    with col4:
        st.metric("平均價差", format_currency(analysis['avg_price_diff']))
    
    # 圖表分析
    st.subheader("📊 視覺化分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 相似度分布圓餅圖
        similarity_chart = create_similarity_chart(analysis['similarity_distribution'])
        st.plotly_chart(similarity_chart, use_container_width=True)
    
    with col2:
        # 價格差異分布直方圖
        price_chart = create_price_difference_chart(matched_df)
        st.plotly_chart(price_chart, use_container_width=True)
    
    # 相似度 vs 價格差異散點圖
    scatter_chart = create_similarity_vs_price_chart(matched_df)
    st.plotly_chart(scatter_chart, use_container_width=True)
    
    # 按國家統計
    if len(analysis['country_stats']) > 0:
        st.subheader("🌍 各國家統計")
        st.dataframe(analysis['country_stats'], use_container_width=True)
    
    # 最高相似度產品
    st.subheader("🏆 相似度最高的產品 (前10名)")
    top_matches = matcher.get_top_matches(matched_df, 10)
    st.dataframe(top_matches, use_container_width=True)
    
    # 結果匯出
    st.subheader("💾 匯出結果")
    col1, col2 = st.columns(2)
    
    with col1:
        # 匯出 CSV
        csv_data = FileHandler.export_to_csv(matched_df)
        st.download_button(
            label="📁 下載 CSV 檔案",
            data=csv_data,
            file_name=f"產品比對結果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # 匯出 Excel
        excel_data = FileHandler.export_to_excel(matched_df)
        st.download_button(
            label="📊 下載 Excel 檔案",
            data=excel_data,
            file_name=f"產品比對結果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
