#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
產品比對核心模組
實現 Jaccard 相似度算法來比對產品
"""

import pandas as pd
import streamlit as st
from typing import Dict, List, Set, Any, Tuple
from multiprocessing import Pool, cpu_count
import itertools


class ProductMatcher:
    """產品比對器類別"""
    
    def __init__(self, similarity_threshold: float = 0.2, max_token_diff: int = 5):
        """
        初始化比對器
        
        Args:
            similarity_threshold: 相似度門檻 (0.0-1.0)
            max_token_diff: 最大詞彙數量差異
        """
        self.similarity_threshold = similarity_threshold
        self.max_token_diff = max_token_diff
    
    @staticmethod
    def tokenize(text: str) -> Set[str]:
        """
        將英文文字進行斷詞處理
        
        Args:
            text: 要斷詞的英文文字
            
        Returns:
            Set[str]: 斷詞後的詞彙集合
        """
        if not isinstance(text, str):
            return set()
        return set(text.lower().split())
    
    @staticmethod
    def calculate_jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
        """
        計算兩個詞彙集合的 Jaccard 相似度
        
        Args:
            set1: 第一個詞彙集合
            set2: 第二個詞彙集合
            
        Returns:
            float: Jaccard 相似度 (0.0-1.0)
        """
        intersection = set1 & set2
        union = set1 | set2
        return len(intersection) / len(union) if union else 0
    
    def compare_single_product(self, row_a: Dict[str, Any], df_b: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        比對單一產品與供應商 B 的所有相關產品
        
        Args:
            row_a: 供應商A的產品資料
            df_b: 供應商B的所有產品資料
            
        Returns:
            List[Dict]: 比對結果列表
        """
        results = []
        tokens_a = self.tokenize(row_a.get('product_name_en', ''))
        country = row_a.get('product_location_country', '')
        
        # 只比對相同國家的產品
        df_b_filtered = df_b[df_b['product_location_country'] == country]
        
        best_score = 0
        best_b_row = None
        
        for _, row_b in df_b_filtered.iterrows():
            tokens_b = self.tokenize(row_b.get('product_name_en', ''))
            
            # 如果詞彙數量差異太大，跳過比較
            if abs(len(tokens_a) - len(tokens_b)) > self.max_token_diff:
                continue
            
            # 計算 Jaccard 相似度
            jaccard_score = self.calculate_jaccard_similarity(tokens_a, tokens_b)
            
            if jaccard_score > best_score:
                best_score = jaccard_score
                best_b_row = row_b
        
        # 只保留相似度 >= 門檻值的結果
        if best_b_row is not None and best_score >= self.similarity_threshold:
            vendor_a_price = row_a.get('price', 0) or 0
            vendor_b_price = best_b_row.get('price', 0) or 0
            price_diff = vendor_b_price - vendor_a_price
            
            results.append({
                'product_location_country': country,
                'vendor_A_product_id': row_a.get('product_id', ''),
                'vendor_A_product_name': row_a.get('product_name', ''),
                'vendor_A_product_name_en': row_a.get('product_name_en', ''),
                'vendor_A_price': vendor_a_price,
                'vendor_B_product_id': best_b_row.get('product_id', ''),
                'vendor_B_product_name': best_b_row.get('product_name', ''),
                'vendor_B_product_name_en': best_b_row.get('product_name_en', ''),
                'vendor_B_price': vendor_b_price,
                'jaccard_score': best_score,
                'price_diff': price_diff
            })
        
        return results
    
    def compare_products(self, df_a: pd.DataFrame, df_b: pd.DataFrame, 
                        similarity_threshold: float = None, translator=None,
                        show_progress: bool = True) -> pd.DataFrame:
        """
        比對兩個供應商的所有產品
        
        Args:
            df_a: 供應商A的產品資料
            df_b: 供應商B的產品資料
            similarity_threshold: 相似度門檻（可選，覆蓋初始設定）
            translator: 翻譯器實例（可選）
            show_progress: 是否顯示進度條
            
        Returns:
            pd.DataFrame: 比對結果
        """
        if df_a is None or df_b is None:
            return pd.DataFrame()
        
        # 使用傳入的門檻值或預設值
        if similarity_threshold is not None:
            self.similarity_threshold = similarity_threshold
        
        # 如果有翻譯器，先翻譯產品名稱
        if translator is not None:
            if 'product_name_en' not in df_a.columns:
                df_a = df_a.copy()
                df_a['product_name_en'] = df_a['product_name'].apply(
                    lambda x: translator.translate_to_english(x)
                )
            
            if 'product_name_en' not in df_b.columns:
                df_b = df_b.copy()
                df_b['product_name_en'] = df_b['product_name'].apply(
                    lambda x: translator.translate_to_english(x)
                )
        
        all_results = []
        
        if show_progress:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # 逐一比對產品
        for i, (_, row_a) in enumerate(df_a.iterrows()):
            results = self.compare_single_product(row_a.to_dict(), df_b)
            all_results.extend(results)
            
            if show_progress:
                progress = (i + 1) / len(df_a)
                progress_bar.progress(progress)
                status_text.text(f"比對進度: {i + 1}/{len(df_a)} ({progress:.1%})")
        
        if show_progress:
            progress_bar.empty()
            status_text.empty()
        
        # 合併結果
        matched_df = pd.DataFrame(all_results)
        
        return matched_df
    
    def analyze_results(self, matched_df: pd.DataFrame) -> Dict[str, Any]:
        """
        分析比對結果
        
        Args:
            matched_df: 比對結果資料框
            
        Returns:
            Dict: 分析統計資訊
        """
        if matched_df is None or len(matched_df) == 0:
            return {
                'total_matches': 0,
                'unique_countries': 0,
                'avg_similarity': 0,
                'avg_price_diff': 0,
                'similarity_distribution': {},
                'country_stats': pd.DataFrame()
            }
        
        # 基本統計
        total_matches = len(matched_df)
        unique_countries = matched_df['product_location_country'].nunique()
        avg_similarity = matched_df['jaccard_score'].mean()
        avg_price_diff = matched_df['price_diff'].mean()
        
        # 相似度分布
        similarity_ranges = [
            (0.2, 0.4, "低相似度"),
            (0.4, 0.6, "中相似度"), 
            (0.6, 0.8, "高相似度"),
            (0.8, 1.0, "極高相似度")
        ]
        
        similarity_distribution = {}
        for min_score, max_score, label in similarity_ranges:
            count = len(matched_df[(matched_df['jaccard_score'] >= min_score) & 
                                  (matched_df['jaccard_score'] < max_score)])
            similarity_distribution[label] = count
        
        # 按國家統計
        country_stats = matched_df.groupby('product_location_country').agg({
            'jaccard_score': ['count', 'mean'],
            'price_diff': 'mean'
        }).round(3)
        
        return {
            'total_matches': total_matches,
            'unique_countries': unique_countries,
            'avg_similarity': avg_similarity,
            'avg_price_diff': avg_price_diff,
            'similarity_distribution': similarity_distribution,
            'country_stats': country_stats
        }
    
    def get_top_matches(self, matched_df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
        """
        獲取相似度最高的前 N 筆結果
        
        Args:
            matched_df: 比對結果資料框
            top_n: 要返回的數量
            
        Returns:
            pd.DataFrame: 前 N 筆最相似的結果
        """
        if matched_df is None or len(matched_df) == 0:
            return pd.DataFrame()
        
        return matched_df.nlargest(top_n, 'jaccard_score')[
            ['product_location_country', 'vendor_A_product_name', 'vendor_B_product_name', 
             'jaccard_score', 'price_diff']
        ]
