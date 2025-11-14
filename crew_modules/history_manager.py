"""
History Manager Module
管理文件生成歷史紀錄
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class HistoryManager:
    """文件歷史紀錄管理器"""
    
    def __init__(self, history_file: str = "history.json"):
        """
        初始化歷史紀錄管理器
        
        Args:
            history_file: 歷史紀錄檔案路徑
        """
        self.history_file = history_file
        self.history_data = self._load_history()
    
    def _load_history(self) -> Dict:
        """載入歷史紀錄"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"載入歷史紀錄失敗：{e}")
                return {"documentation": [], "refactoring": [], "research": []}
        return {"documentation": [], "refactoring": [], "research": []}
    
    def _save_history(self):
        """儲存歷史紀錄"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"儲存歷史紀錄失敗：{e}")
    
    def add_record(
        self,
        crew_type: str,
        input_files: List[str],
        output_file: str,
        success: bool = True,
        error_message: str = None
    ) -> Dict:
        """
        新增歷史紀錄
        
        Args:
            crew_type: Crew 類型 ('documentation', 'refactoring', 'research')
            input_files: 輸入檔案列表
            output_file: 輸出檔案路徑
            success: 是否成功
            error_message: 錯誤訊息（如果有）
            
        Returns:
            新增的紀錄
        """
        record = {
            "id": self._generate_id(),
            "timestamp": datetime.now().isoformat(),
            "crew_type": crew_type,
            "input_files": input_files,
            "output_file": output_file,
            "success": success,
            "error_message": error_message,
            "file_exists": os.path.exists(output_file) if output_file else False
        }
        
        if crew_type not in self.history_data:
            self.history_data[crew_type] = []
        
        self.history_data[crew_type].insert(0, record)  # 最新的放最前面
        
        # 限制每個類型最多保留 100 筆紀錄
        if len(self.history_data[crew_type]) > 100:
            self.history_data[crew_type] = self.history_data[crew_type][:100]
        
        self._save_history()
        return record
    
    def get_history(
        self,
        crew_type: str = None,
        limit: int = None,
        success_only: bool = False
    ) -> List[Dict]:
        """
        取得歷史紀錄
        
        Args:
            crew_type: Crew 類型，None 表示全部
            limit: 限制筆數
            success_only: 只顯示成功的紀錄
            
        Returns:
            歷史紀錄列表
        """
        if crew_type:
            records = self.history_data.get(crew_type, [])
        else:
            # 合併所有類型並按時間排序
            all_records = []
            for records in self.history_data.values():
                all_records.extend(records)
            records = sorted(all_records, key=lambda x: x['timestamp'], reverse=True)
        
        if success_only:
            records = [r for r in records if r.get('success', False)]
        
        if limit:
            records = records[:limit]
        
        # 更新 file_exists 狀態
        for record in records:
            if 'output_file' in record and record['output_file']:
                record['file_exists'] = os.path.exists(record['output_file'])
        
        return records
    
    def delete_record(self, record_id: str) -> bool:
        """
        刪除指定紀錄
        
        Args:
            record_id: 紀錄 ID
            
        Returns:
            是否刪除成功
        """
        for crew_type, records in self.history_data.items():
            for i, record in enumerate(records):
                if record.get('id') == record_id:
                    del self.history_data[crew_type][i]
                    self._save_history()
                    return True
        return False
    
    def clear_history(self, crew_type: str = None):
        """
        清除歷史紀錄
        
        Args:
            crew_type: Crew 類型，None 表示清除全部
        """
        if crew_type:
            self.history_data[crew_type] = []
        else:
            self.history_data = {"documentation": [], "refactoring": [], "research": []}
        self._save_history()
    
    def get_statistics(self) -> Dict:
        """
        取得統計資訊
        
        Returns:
            統計資訊字典
        """
        stats = {}
        for crew_type, records in self.history_data.items():
            total = len(records)
            success = sum(1 for r in records if r.get('success', False))
            failed = total - success
            
            stats[crew_type] = {
                "total": total,
                "success": success,
                "failed": failed,
                "success_rate": f"{(success/total*100):.1f}%" if total > 0 else "0%"
            }
        
        return stats
    
    def _generate_id(self) -> str:
        """生成唯一 ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def format_timestamp(self, timestamp: str) -> str:
        """
        格式化時間戳記
        
        Args:
            timestamp: ISO 格式時間戳記
            
        Returns:
            格式化的時間字串
        """
        try:
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return timestamp


# 全域實例
history_manager = HistoryManager()
