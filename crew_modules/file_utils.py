"""
File Utilities Module
文件掃描和過濾功能
"""

import os
from pathlib import Path
from typing import List, Set

# 敏感文件模式 - 應該被排除的文件
SENSITIVE_FILE_PATTERNS = {
    # 環境變數和配置
    '.env', '.env.local', '.env.development', '.env.production', '.env.test',
    
    # 憑證和金鑰
    'credentials.json', 'credentials.yaml', 'credentials.yml',
    'secrets.json', 'secrets.yaml', 'secrets.yml',
    'service-account.json', 'serviceaccount.json',
    
    # SSH 和加密金鑰
    'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519',
    'private_key.pem', 'private.key', 'privatekey.pem',
    
    # AWS 和雲端憑證
    'aws_credentials', 'config.credentials',
    
    # 資料庫配置
    'database.ini', 'db.config',
    
    # 其他敏感文件
    'password.txt', 'passwords.txt', 'secret.txt',
}

# 敏感文件副檔名
SENSITIVE_EXTENSIONS = {
    '.key', '.pem', '.p12', '.pfx', '.keystore', '.jks',
    '.crt', '.cer', '.der', '.csr',
}

# 應該被排除的目錄
EXCLUDED_DIRECTORIES = {
    '__pycache__', '.git', '.svn', '.hg',
    'node_modules', 'venv', 'env', '.venv',
    'dist', 'build', '.egg-info',
    '.idea', '.vscode', '.vs',
}


def is_sensitive_file(file_path: str) -> bool:
    """
    檢查文件是否為敏感文件
    
    Args:
        file_path: 文件路徑
        
    Returns:
        True 如果是敏感文件，否則 False
    """
    path = Path(file_path)
    filename = path.name.lower()
    
    # 檢查完整文件名
    if filename in SENSITIVE_FILE_PATTERNS:
        return True
    
    # 檢查副檔名
    if path.suffix.lower() in SENSITIVE_EXTENSIONS:
        return True
    
    # 檢查是否包含敏感關鍵字
    sensitive_keywords = ['credential', 'secret', 'password', 'private', 'key']
    for keyword in sensitive_keywords:
        if keyword in filename:
            return True
    
    return False


def should_exclude_directory(dir_name: str) -> bool:
    """
    檢查目錄是否應該被排除
    
    Args:
        dir_name: 目錄名稱
        
    Returns:
        True 如果應該被排除，否則 False
    """
    return dir_name in EXCLUDED_DIRECTORIES


def scan_directory_for_python_files(
    directory: str,
    recursive: bool = True,
    exclude_sensitive: bool = True
) -> tuple[List[str], List[str]]:
    """
    掃描目錄中的 Python 文件
    
    Args:
        directory: 目錄路徑
        recursive: 是否遞迴掃描子目錄
        exclude_sensitive: 是否排除敏感文件
        
    Returns:
        (有效文件列表, 被排除的敏感文件列表)
    """
    valid_files = []
    excluded_files = []
    
    if not os.path.exists(directory):
        return valid_files, excluded_files
    
    if not os.path.isdir(directory):
        # 如果是單個文件
        if directory.endswith('.py'):
            if exclude_sensitive and is_sensitive_file(directory):
                excluded_files.append(directory)
            else:
                valid_files.append(directory)
        return valid_files, excluded_files
    
    # 掃描目錄
    for root, dirs, files in os.walk(directory):
        # 排除特定目錄
        if exclude_sensitive:
            dirs[:] = [d for d in dirs if not should_exclude_directory(d)]
        
        # 處理文件
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                if exclude_sensitive and is_sensitive_file(file_path):
                    excluded_files.append(file_path)
                else:
                    valid_files.append(file_path)
        
        # 如果不遞迴，只處理第一層
        if not recursive:
            break
    
    return valid_files, excluded_files


def scan_multiple_paths(
    paths: List[str],
    recursive: bool = True,
    exclude_sensitive: bool = True
) -> tuple[List[str], List[str]]:
    """
    掃描多個路徑（可以是文件或目錄）
    
    Args:
        paths: 路徑列表
        recursive: 是否遞迴掃描
        exclude_sensitive: 是否排除敏感文件
        
    Returns:
        (有效文件列表, 被排除的敏感文件列表)
    """
    all_valid_files = []
    all_excluded_files = []
    
    for path in paths:
        path = path.strip()
        if not path:
            continue
        
        valid_files, excluded_files = scan_directory_for_python_files(
            path, recursive, exclude_sensitive
        )
        all_valid_files.extend(valid_files)
        all_excluded_files.extend(excluded_files)
    
    # 去重
    all_valid_files = list(dict.fromkeys(all_valid_files))
    all_excluded_files = list(dict.fromkeys(all_excluded_files))
    
    return all_valid_files, all_excluded_files


def format_file_list(files: List[str], max_display: int = 20) -> str:
    """
    格式化文件列表為易讀的字串
    
    Args:
        files: 文件列表
        max_display: 最多顯示的文件數量
        
    Returns:
        格式化的文件列表字串
    """
    if not files:
        return "無"
    
    displayed_files = files[:max_display]
    result = "\n".join([f"  - {file}" for file in displayed_files])
    
    if len(files) > max_display:
        result += f"\n  ... 以及其他 {len(files) - max_display} 個文件"
    
    return result
