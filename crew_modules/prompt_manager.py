"""
System Prompts 管理模組
用於讀取和應用自訂的 system prompts
"""

import configparser
import os


class PromptManager:
    """管理自訂 System Prompts"""
    
    def __init__(self, config_file='custom_prompts.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """載入設定檔"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
        else:
            # 如果設定檔不存在，使用預設值
            self._create_default_config()
    
    def _create_default_config(self):
        """建立預設設定"""
        self.config['GLOBAL_RULES'] = {
            'global_prompt': """
重要規則（每次執行都必須遵守）：
1. 所有輸出必須使用繁體中文
2. 代碼註解和文檔請使用繁體中文
3. 保持專業和友善的語氣
4. 提供具體可行的建議
5. 引用來源時提供連結
"""
        }
        
        # 儲存預設設定
        self.save_config()
    
    def save_config(self):
        """儲存設定到檔案"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get_global_rules(self):
        """取得全域規則"""
        if 'GLOBAL_RULES' in self.config:
            return self.config['GLOBAL_RULES'].get('global_prompt', '')
        return ''
    
    def get_agent_prompt(self, section, key):
        """
        取得特定 Agent 的自訂 prompt
        
        Args:
            section: 設定區段名稱 (如 'DOCUMENTATION_CREW')
            key: prompt key (如 'senior_dev_prompt')
        """
        if section in self.config:
            return self.config[section].get(key, '')
        return ''
    
    def update_global_rules(self, new_rules):
        """更新全域規則"""
        if 'GLOBAL_RULES' not in self.config:
            self.config['GLOBAL_RULES'] = {}
        self.config['GLOBAL_RULES']['global_prompt'] = new_rules
        self.save_config()
    
    def update_agent_prompt(self, section, key, prompt):
        """更新特定 Agent 的 prompt"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = prompt
        self.save_config()
    
    def get_enhanced_backstory(self, section, key, original_backstory):
        """
        取得增強版的 backstory（原始 + 全域規則 + 自訂規則）
        
        Args:
            section: 設定區段
            key: prompt key
            original_backstory: 原始的 backstory
            
        Returns:
            增強後的 backstory
        """
        global_rules = self.get_global_rules()
        custom_prompt = self.get_agent_prompt(section, key)
        
        enhanced = original_backstory
        
        if global_rules.strip():
            enhanced += f"\n\n{global_rules}"
        
        if custom_prompt.strip():
            enhanced += f"\n\n{custom_prompt}"
        
        return enhanced
    
    def get_all_sections(self):
        """取得所有設定區段"""
        return self.config.sections()
    
    def get_section_keys(self, section):
        """取得特定區段的所有 keys"""
        if section in self.config:
            return list(self.config[section].keys())
        return []


# 全域實例
prompt_manager = PromptManager()
