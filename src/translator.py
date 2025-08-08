#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻譯模組
處理中文到英文的翻譯功能
"""

from deep_translator import GoogleTranslator
import streamlit as st
from typing import Optional, List
import time
import random


class TranslationService:
    """翻譯服務類別"""
    
    def __init__(self):
        """初始化翻譯器"""
        self.translator = GoogleTranslator(source='zh-TW', target='en')
        self.translation_cache = {}  # 翻譯快取
    
    def translate_to_english(self, text: str, use_cache: bool = True) -> str:
        """
        將中文文字翻譯成英文
        
        Args:
            text: 要翻譯的中文文字
            use_cache: 是否使用快取
            
        Returns:
            str: 翻譯後的英文文字
        """
        if not isinstance(text, str) or not text.strip():
            return ""
        
        # 檢查快取
        if use_cache and text in self.translation_cache:
            return self.translation_cache[text]
        
        try:
            # 加入隨機延遲避免 API 限制
            time.sleep(random.uniform(0.1, 0.3))
            
            translated_text = self.translator.translate(text)
            
            # 儲存到快取
            if use_cache:
                self.translation_cache[text] = translated_text
            
            return translated_text
            
        except Exception as e:
            st.warning(f"⚠️ 翻譯失敗: {text} -> {str(e)}")
            return text  # 翻譯失敗時返回原文
    
    def translate_batch(self, texts: List[str], show_progress: bool = True) -> List[str]:
        """
        批次翻譯文字列表
        
        Args:
            texts: 要翻譯的文字列表
            show_progress: 是否顯示進度條
            
        Returns:
            List[str]: 翻譯後的文字列表
        """
        translated_texts = []
        
        if show_progress:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        for i, text in enumerate(texts):
            translated_text = self.translate_to_english(text)
            translated_texts.append(translated_text)
            
            if show_progress:
                progress = (i + 1) / len(texts)
                progress_bar.progress(progress)
                status_text.text(f"翻譯進度: {i + 1}/{len(texts)} ({progress:.1%})")
        
        if show_progress:
            progress_bar.empty()
            status_text.empty()
        
        return translated_texts
    
    def clear_cache(self):
        """清除翻譯快取"""
        self.translation_cache.clear()
        st.success("✅ 翻譯快取已清除")
    
    def get_cache_info(self) -> dict:
        """
        獲取快取資訊
        
        Returns:
            dict: 快取統計資訊
        """
        return {
            'cache_size': len(self.translation_cache),
            'cached_translations': list(self.translation_cache.keys())[:10]  # 只顯示前10個
        }
