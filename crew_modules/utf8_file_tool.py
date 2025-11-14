"""
Custom File Reading Tool
自定義文件讀取工具，支援 UTF-8 編碼
"""

import os
from typing import List


def read_files_content(file_paths: List[str]) -> str:
    """
    批量讀取多個文件的內容（UTF-8 編碼）
    
    Args:
        file_paths: 文件路徑列表
        
    Returns:
        所有文件的合併內容
    """
    results = []
    
    for file_path in file_paths:
        try:
            abs_path = os.path.abspath(file_path)
            
            if not os.path.exists(abs_path):
                results.append(f"\n{'='*80}\nFile: {abs_path}\nError: File not found\n{'='*80}\n")
                continue
            
            with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            results.append(f"\n{'='*80}\nFile: {abs_path}\n{'='*80}\n\n{content}\n")
        
        except Exception as e:
            results.append(f"\n{'='*80}\nFile: {abs_path}\nError: {str(e)}\n{'='*80}\n")
    
    return "\n".join(results)
