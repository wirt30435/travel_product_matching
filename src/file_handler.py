#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檔案處理模組
處理 CSV 和 Excel 檔案的上傳、讀取和驗證
"""

import pandas as pd
import streamlit as st
from typing import Optional, Tuple, Dict, Any
import io


class FileHandler:
    """檔案處理類別"""
    
    REQUIRED_COLUMNS = ['product_id', 'product_name', 'product_location_country', 'price']
    SUPPORTED_FORMATS = ['csv', 'xlsx', 'xls']
    
    @staticmethod
    def validate_file_format(file) -> bool:
        """
        驗證檔案格式是否支援
        
        Args:
            file: 上傳的檔案物件
            
        Returns:
            bool: 是否為支援的格式
        """
        if file is None:
            return False
        
        file_extension = file.name.lower().split('.')[-1]
        return file_extension in FileHandler.SUPPORTED_FORMATS
    
    @staticmethod
    def read_file(file) -> Optional[pd.DataFrame]:
        """
        讀取上傳的檔案
        
        Args:
            file: 上傳的檔案物件
            
        Returns:
            pd.DataFrame or None: 讀取成功返回 DataFrame，失敗返回 None
        """
        if not FileHandler.validate_file_format(file):
            st.error(f"❌ 不支援的檔案格式。支援格式: {', '.join(FileHandler.SUPPORTED_FORMATS)}")
            return None
        
        try:
            file_extension = file.name.lower().split('.')[-1]
            
            if file_extension == 'csv':
                # 嘗試不同的編碼格式
                try:
                    df = pd.read_csv(file, encoding='utf-8')
                except UnicodeDecodeError:
                    file.seek(0)  # 重置檔案指標
                    try:
                        df = pd.read_csv(file, encoding='big5')
                    except UnicodeDecodeError:
                        file.seek(0)
                        df = pd.read_csv(file, encoding='gbk')
            
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(file)
            
            return df
            
        except Exception as e:
            st.error(f"❌ 檔案讀取失敗: {str(e)}")
            return None
    
    @staticmethod
    def validate_columns(df: pd.DataFrame) -> Tuple[bool, list]:
        """
        驗證 DataFrame 是否包含必要欄位
        
        Args:
            df: 要驗證的 DataFrame
            
        Returns:
            Tuple[bool, list]: (是否通過驗證, 缺少的欄位列表)
        """
        if df is None:
            return False, FileHandler.REQUIRED_COLUMNS
        
        missing_columns = []
        df_columns = [col.lower() for col in df.columns]
        
        for required_col in FileHandler.REQUIRED_COLUMNS:
            if required_col.lower() not in df_columns:
                missing_columns.append(required_col)
        
        return len(missing_columns) == 0, missing_columns
    
    @staticmethod
    def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        標準化欄位名稱
        
        Args:
            df: 要標準化的 DataFrame
            
        Returns:
            pd.DataFrame: 標準化後的 DataFrame
        """
        if df is None:
            return None
        
        # 建立欄位名稱對應表
        column_mapping = {}
        df_columns_lower = {col.lower(): col for col in df.columns}
        
        for required_col in FileHandler.REQUIRED_COLUMNS:
            if required_col.lower() in df_columns_lower:
                original_col = df_columns_lower[required_col.lower()]
                column_mapping[original_col] = required_col
        
        # 重新命名欄位
        df_standardized = df.rename(columns=column_mapping)
        
        # 只保留必要欄位
        return df_standardized[FileHandler.REQUIRED_COLUMNS]
    
    @staticmethod
    def get_data_preview(df: pd.DataFrame, num_rows: int = 10) -> pd.DataFrame:
        """
        獲取資料預覽
        
        Args:
            df: 要預覽的 DataFrame
            num_rows: 預覽行數
            
        Returns:
            pd.DataFrame: 預覽資料
        """
        if df is None:
            return pd.DataFrame()
        
        return df.head(num_rows)
    
    @staticmethod
    def get_data_info(df: pd.DataFrame) -> Dict[str, Any]:
        """
        獲取資料基本資訊
        
        Args:
            df: 要分析的 DataFrame
            
        Returns:
            Dict: 包含資料統計資訊的字典
        """
        if df is None:
            return {}
        
        info = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.to_dict(),
            'unique_countries': df['product_location_country'].nunique() if 'product_location_country' in df.columns else 0,
            'price_range': {
                'min': df['price'].min() if 'price' in df.columns else None,
                'max': df['price'].max() if 'price' in df.columns else None,
                'mean': df['price'].mean() if 'price' in df.columns else None
            }
        }
        
        return info
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filename: str = "比對結果.csv") -> bytes:
        """
        匯出 DataFrame 為 CSV 格式
        
        Args:
            df: 要匯出的 DataFrame
            filename: 檔案名稱
            
        Returns:
            bytes: CSV 檔案的二進位資料
        """
        output = io.StringIO()
        df.to_csv(output, index=False, encoding='utf-8-sig')
        return output.getvalue().encode('utf-8-sig')
    
    @staticmethod
    def export_to_excel(df: pd.DataFrame, filename: str = "比對結果.xlsx") -> bytes:
        """
        匯出 DataFrame 為 Excel 格式
        
        Args:
            df: 要匯出的 DataFrame
            filename: 檔案名稱
            
        Returns:
            bytes: Excel 檔案的二進位資料
        """
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='比對結果', index=False)
        return output.getvalue()
