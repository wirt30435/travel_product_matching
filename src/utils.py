#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函數模組
提供通用的輔助函數
"""

import pandas as pd
import streamlit as st
from typing import Any, Dict, List
import plotly.express as px
import plotly.graph_objects as go
import logging


def format_number(num: float, decimal_places: int = 2) -> str:
    """
    格式化數字顯示
    
    Args:
        num: 要格式化的數字
        decimal_places: 小數位數
        
    Returns:
        str: 格式化後的字串
    """
    if num is None:
        return "N/A"
    return f"{num:,.{decimal_places}f}"


def format_percentage(ratio: float, decimal_places: int = 1) -> str:
    """
    格式化百分比顯示
    
    Args:
        ratio: 比例 (0.0-1.0)
        decimal_places: 小數位數
        
    Returns:
        str: 格式化後的百分比字串
    """
    if ratio is None:
        return "N/A"
    return f"{ratio * 100:.{decimal_places}f}%"


def create_similarity_chart(similarity_distribution: Dict[str, int]) -> go.Figure:
    """
    創建相似度分布圖表
    
    Args:
        similarity_distribution: 相似度分布資料
        
    Returns:
        plotly.graph_objects.Figure: 圖表物件
    """
    labels = list(similarity_distribution.keys())
    values = list(similarity_distribution.values())
    
    fig = px.pie(
        values=values,
        names=labels,
        title="相似度分布",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )
    
    return fig


def create_price_difference_chart(matched_df: pd.DataFrame) -> go.Figure:
    """
    創建價格差異分布圖表
    
    Args:
        matched_df: 比對結果資料框
        
    Returns:
        plotly.graph_objects.Figure: 圖表物件
    """
    if matched_df is None or len(matched_df) == 0:
        return go.Figure()
    
    fig = px.histogram(
        matched_df,
        x='price_diff',
        title='價格差異分布',
        labels={'price_diff': '價格差異', 'count': '數量'},
        nbins=20
    )
    
    fig.update_layout(
        xaxis_title="價格差異 (供應商B - 供應商A)",
        yaxis_title="產品數量"
    )
    
    return fig


def create_similarity_vs_price_chart(matched_df: pd.DataFrame) -> go.Figure:
    """
    創建相似度與價格差異的散點圖
    
    Args:
        matched_df: 比對結果資料框
        
    Returns:
        plotly.graph_objects.Figure: 圖表物件
    """
    if matched_df is None or len(matched_df) == 0:
        return go.Figure()
    
    fig = px.scatter(
        matched_df,
        x='jaccard_score',
        y='price_diff',
        color='product_location_country',
        title='相似度 vs 價格差異',
        labels={
            'jaccard_score': '相似度分數',
            'price_diff': '價格差異',
            'product_location_country': '國家'
        },
        hover_data=['vendor_A_product_name', 'vendor_B_product_name']
    )
    
    fig.update_layout(
        xaxis_title="相似度分數",
        yaxis_title="價格差異 (供應商B - 供應商A)"
    )
    
    return fig


def display_data_summary(df: pd.DataFrame, title: str = "資料摘要"):
    """
    顯示資料摘要資訊
    
    Args:
        df: 要顯示的資料框
        title: 摘要標題
    """
    if df is None or len(df) == 0:
        st.warning("📊 無資料可顯示")
        return
    
    st.subheader(title)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("總筆數", len(df))
    
    with col2:
        st.metric("欄位數", len(df.columns))
    
    if 'product_location_country' in df.columns:
        with col3:
            st.metric("國家數", df['product_location_country'].nunique())
    
    if 'price' in df.columns:
        with col4:
            avg_price = df['price'].mean()
            st.metric("平均價格", f"${avg_price:.2f}" if pd.notna(avg_price) else "N/A")


def display_missing_values(df: pd.DataFrame):
    """
    顯示缺失值資訊
    
    Args:
        df: 要檢查的資料框
    """
    if df is None:
        return
    
    missing_data = df.isnull().sum()
    if missing_data.sum() > 0:
        st.warning("⚠️ 發現缺失值:")
        for col, count in missing_data[missing_data > 0].items():
            st.write(f"  - {col}: {count} 筆缺失")
    else:
        st.success("✅ 無缺失值")


def validate_data_quality(df: pd.DataFrame) -> List[str]:
    """
    驗證資料品質並返回問題列表
    
    Args:
        df: 要驗證的資料框
        
    Returns:
        List[str]: 發現的問題列表
    """
    issues = []
    
    if df is None or len(df) == 0:
        issues.append("資料框為空")
        return issues
    
    # 檢查必要欄位
    required_columns = ['product_id', 'product_name', 'product_location_country', 'price']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        issues.append(f"缺少必要欄位: {', '.join(missing_columns)}")
    
    # 檢查重複的產品ID
    if 'product_id' in df.columns:
        duplicate_ids = df['product_id'].duplicated().sum()
        if duplicate_ids > 0:
            issues.append(f"發現 {duplicate_ids} 個重複的產品ID")
    
    # 檢查空的產品名稱
    if 'product_name' in df.columns:
        empty_names = df['product_name'].isnull().sum()
        if empty_names > 0:
            issues.append(f"發現 {empty_names} 個空的產品名稱")
    
    # 檢查負價格
    if 'price' in df.columns:
        negative_prices = (df['price'] < 0).sum()
        if negative_prices > 0:
            issues.append(f"發現 {negative_prices} 個負價格")
    
    return issues


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    格式化貨幣顯示
    
    Args:
        amount: 金額
        currency: 貨幣代碼
        
    Returns:
        str: 格式化後的貨幣字串
    """
    if amount is None or pd.isna(amount):
        return "N/A"
    
    currency_symbols = {
        "USD": "$",
        "EUR": "€", 
        "GBP": "£",
        "JPY": "¥",
        "TWD": "NT$"
    }
    
    symbol = currency_symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def setup_logging(level: int = logging.INFO) -> None:
    """
    設定基礎日誌輸出（供雲端與本機使用）
    
    Args:
        level: 日誌層級，預設 INFO
    """
    # 若已經設定過則略過
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    logging.getLogger(__name__).info("Logging initialized")
