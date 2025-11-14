"""
File Picker Module
使用 tkinter 提供圖形化檔案/目錄選擇對話框
"""

import tkinter as tk
from tkinter import filedialog
import os
from typing import List, Optional


def pick_file(
    title: str = "選擇文件",
    filetypes: List[tuple] = None,
    initialdir: str = None
) -> Optional[str]:
    """
    開啟檔案選擇對話框
    
    Args:
        title: 對話框標題
        filetypes: 檔案類型過濾器，例如 [("Python files", "*.py"), ("All files", "*.*")]
        initialdir: 初始目錄
        
    Returns:
        選擇的檔案路徑，如果取消則返回 None
    """
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗
    root.wm_attributes('-topmost', 1)  # 置頂
    
    if filetypes is None:
        filetypes = [("Python files", "*.py"), ("All files", "*.*")]
    
    if initialdir is None:
        initialdir = os.getcwd()
    
    file_path = filedialog.askopenfilename(
        parent=root,
        title=title,
        filetypes=filetypes,
        initialdir=initialdir
    )
    
    root.destroy()
    
    return file_path if file_path else None


def pick_multiple_files(
    title: str = "選擇多個文件",
    filetypes: List[tuple] = None,
    initialdir: str = None
) -> List[str]:
    """
    開啟多檔案選擇對話框
    
    Args:
        title: 對話框標題
        filetypes: 檔案類型過濾器
        initialdir: 初始目錄
        
    Returns:
        選擇的檔案路徑列表
    """
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    
    if filetypes is None:
        filetypes = [("Python files", "*.py"), ("All files", "*.*")]
    
    if initialdir is None:
        initialdir = os.getcwd()
    
    file_paths = filedialog.askopenfilenames(
        parent=root,
        title=title,
        filetypes=filetypes,
        initialdir=initialdir
    )
    
    root.destroy()
    
    return list(file_paths) if file_paths else []


def pick_directory(
    title: str = "選擇目錄",
    initialdir: str = None
) -> Optional[str]:
    """
    開啟目錄選擇對話框
    
    Args:
        title: 對話框標題
        initialdir: 初始目錄
        
    Returns:
        選擇的目錄路徑，如果取消則返回 None
    """
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    
    if initialdir is None:
        initialdir = os.getcwd()
    
    dir_path = filedialog.askdirectory(
        parent=root,
        title=title,
        initialdir=initialdir
    )
    
    root.destroy()
    
    return dir_path if dir_path else None


def pick_files_and_directories(
    title_file: str = "選擇文件",
    title_dir: str = "選擇目錄",
    filetypes: List[tuple] = None,
    initialdir: str = None
) -> tuple[List[str], List[str]]:
    """
    組合式選擇：可以選擇多個檔案和多個目錄
    
    Args:
        title_file: 檔案選擇對話框標題
        title_dir: 目錄選擇對話框標題
        filetypes: 檔案類型過濾器
        initialdir: 初始目錄
        
    Returns:
        (檔案列表, 目錄列表)
    """
    files = pick_multiple_files(title_file, filetypes, initialdir)
    directories = []
    
    # 詢問是否還要選擇目錄
    root = tk.Tk()
    root.withdraw()
    
    from tkinter import messagebox
    if messagebox.askyesno("選擇目錄", "是否要選擇目錄？"):
        while True:
            dir_path = pick_directory(title_dir, initialdir)
            if dir_path:
                directories.append(dir_path)
                if not messagebox.askyesno("繼續選擇", "是否要繼續選擇其他目錄？"):
                    break
            else:
                break
    
    root.destroy()
    
    return files, directories
