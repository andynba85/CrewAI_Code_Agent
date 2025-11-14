"""
Streamlit Callback Handler
用於在 Streamlit UI 中即時顯示 CrewAI Agent 執行進度
"""

import streamlit as st
from typing import Any, Dict, Optional
from datetime import datetime


class StreamlitCallbackHandler:
    """
    CrewAI 回調處理器，用於在 Streamlit 中顯示執行進度
    """
    
    def __init__(self, status_container):
        """
        初始化回調處理器
        
        Args:
            status_container: Streamlit 容器用於顯示狀態
        """
        self.status_container = status_container
        self.agent_status = {}
        self.task_status = {}
        self.start_time = datetime.now()
    
    def on_agent_start(self, agent_name: str):
        """Agent 開始執行"""
        self.agent_status[agent_name] = {
            'status': 'running',
            'start_time': datetime.now(),
            'end_time': None
        }
        self._update_display()
    
    def on_agent_end(self, agent_name: str):
        """Agent 完成執行"""
        if agent_name in self.agent_status:
            self.agent_status[agent_name]['status'] = 'completed'
            self.agent_status[agent_name]['end_time'] = datetime.now()
        self._update_display()
    
    def on_task_start(self, task_name: str, agent_name: str):
        """Task 開始執行"""
        self.task_status[task_name] = {
            'status': 'running',
            'agent': agent_name,
            'start_time': datetime.now(),
            'end_time': None
        }
        self._update_display()
    
    def on_task_end(self, task_name: str):
        """Task 完成執行"""
        if task_name in self.task_status:
            self.task_status[task_name]['status'] = 'completed'
            self.task_status[task_name]['end_time'] = datetime.now()
        self._update_display()
    
    def _update_display(self):
        """更新 Streamlit 顯示"""
        with self.status_container:
            st.empty()  # 清空容器
            
            # 顯示總體進度
            total_agents = len(self.agent_status)
            completed_agents = sum(1 for s in self.agent_status.values() if s['status'] == 'completed')
            
            if total_agents > 0:
                progress = completed_agents / total_agents
                st.progress(progress, text=f"整體進度：{completed_agents}/{total_agents} Agents 完成")
            
            # 顯示每個 Agent 的狀態
            st.markdown("### 🤖 AI Agents 執行狀態")
            
            for agent_name, status in self.agent_status.items():
                col1, col2, col3 = st.columns([3, 1, 2])
                
                with col1:
                    if status['status'] == 'running':
                        st.markdown(f"🔄 **{agent_name}** - 執行中...")
                    elif status['status'] == 'completed':
                        st.markdown(f"✅ **{agent_name}** - 已完成")
                
                with col2:
                    if status['status'] == 'completed' and status['end_time']:
                        duration = (status['end_time'] - status['start_time']).total_seconds()
                        st.markdown(f"⏱️ {duration:.1f}s")
                
                with col3:
                    # 顯示相關的 task
                    related_tasks = [t for t, info in self.task_status.items() 
                                   if info.get('agent') == agent_name]
                    if related_tasks:
                        task_status = self.task_status[related_tasks[0]]['status']
                        if task_status == 'running':
                            st.markdown("📝 處理任務中")
                        else:
                            st.markdown("📝 任務完成")
            
            # 顯示總執行時間
            elapsed = (datetime.now() - self.start_time).total_seconds()
            st.markdown(f"**總執行時間：** {elapsed:.1f} 秒")


def create_progress_container():
    """創建進度顯示容器"""
    return st.container()


def update_agent_progress(container, agent_name: str, status: str, total: int, completed: int):
    """
    簡單的進度更新函數
    
    Args:
        container: Streamlit 容器
        agent_name: Agent 名稱
        status: 狀態 ('running', 'completed')
        total: 總 Agent 數量
        completed: 已完成 Agent 數量
    """
    with container:
        # 進度條
        progress = completed / total if total > 0 else 0
        st.progress(progress, text=f"進度：{completed}/{total} Agents 完成")
        
        # 當前 Agent 狀態
        if status == 'running':
            st.markdown(f"🔄 **正在執行：** {agent_name}")
        elif status == 'completed':
            st.markdown(f"✅ **已完成：** {agent_name}")
