"""
Authentication Module
使用者登入/註冊身份驗證系統
"""

import streamlit as st
import os
from pathlib import Path
import json
from datetime import datetime, timedelta
import hashlib


# 用戶資料存儲文件
USERS_FILE = "users_db.json"
SESSIONS_FILE = "sessions.json"


def load_users():
    """載入用戶資料"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"users": []}
    return {"users": []}


def save_users(users_data):
    """儲存用戶資料"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)


def load_sessions():
    """載入 session 資料"""
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"sessions": []}
    return {"sessions": []}


def save_sessions(sessions_data):
    """儲存 session 資料"""
    with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(sessions_data, f, ensure_ascii=False, indent=2)


def hash_password(password):
    """密碼雜湊"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed):
    """驗證密碼"""
    return hash_password(password) == hashed


def add_user(email, password, name=None, google_id=None):
    """新增用戶"""
    users_data = load_users()
    
    # 檢查是否已存在
    for user in users_data["users"]:
        if user["email"] == email:
            return False, "此電子郵件已被註冊"
    
    # 新增用戶
    new_user = {
        "email": email,
        "password": hash_password(password) if password else None,
        "name": name or email.split('@')[0],
        "google_id": google_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": None
    }
    
    users_data["users"].append(new_user)
    save_users(users_data)
    return True, "註冊成功"


def authenticate_user(email, password):
    """驗證用戶"""
    users_data = load_users()
    
    for user in users_data["users"]:
        if user["email"] == email:
            if user["password"] and verify_password(password, user["password"]):
                # 更新最後登入時間
                user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_users(users_data)
                return True, user
            else:
                return False, "密碼錯誤"
    
    return False, "用戶不存在"


def create_session(user_email):
    """創建 session"""
    sessions_data = load_sessions()
    
    session_id = hashlib.sha256(f"{user_email}{datetime.now()}".encode()).hexdigest()
    
    new_session = {
        "session_id": session_id,
        "email": user_email,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expires_at": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    }
    
    sessions_data["sessions"].append(new_session)
    save_sessions(sessions_data)
    
    return session_id


def verify_session(session_id):
    """驗證 session"""
    sessions_data = load_sessions()
    
    for session in sessions_data["sessions"]:
        if session["session_id"] == session_id:
            expires_at = datetime.strptime(session["expires_at"], "%Y-%m-%d %H:%M:%S")
            if expires_at > datetime.now():
                return True, session["email"]
            else:
                # Session 過期，刪除
                sessions_data["sessions"].remove(session)
                save_sessions(sessions_data)
                return False, "Session 已過期"
    
    return False, "無效的 session"


def logout_user(session_id):
    """登出用戶"""
    sessions_data = load_sessions()
    
    sessions_data["sessions"] = [s for s in sessions_data["sessions"] if s["session_id"] != session_id]
    save_sessions(sessions_data)


def init_session_state():
    """初始化 session state"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None


def show_login_page():
    """顯示登入頁面"""
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 30px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .login-title {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="login-title">🤖 CrewAI Code Agent</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["登入", "註冊"])
        
        with tab1:
            st.markdown("### 🔐 登入")
            
            email = st.text_input("電子郵件", key="login_email")
            password = st.text_input("密碼", type="password", key="login_password")
            
            if st.button("🔑 登入", type="primary", use_container_width=True):
                if email and password:
                    success, result = authenticate_user(email, password)
                    if success:
                        session_id = create_session(email)
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_name = result["name"]
                        st.session_state.session_id = session_id
                        st.success("登入成功！")
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.warning("請填寫所有欄位")
        
        with tab2:
            st.markdown("### 📝 註冊")
            
            new_email = st.text_input("電子郵件", key="register_email")
            new_name = st.text_input("姓名", key="register_name")
            new_password = st.text_input("密碼", type="password", key="register_password")
            new_password_confirm = st.text_input("確認密碼", type="password", key="register_password_confirm")
            
            if st.button("✅ 註冊", type="primary", use_container_width=True):
                if new_email and new_name and new_password and new_password_confirm:
                    if new_password == new_password_confirm:
                        if len(new_password) >= 6:
                            success, message = add_user(new_email, new_password, new_name)
                            if success:
                                st.success(message + " 請使用登入頁面登入")
                            else:
                                st.error(message)
                        else:
                            st.warning("密碼長度至少 6 個字元")
                    else:
                        st.error("兩次密碼不一致")
                else:
                    st.warning("請填寫所有欄位")


def require_authentication():
    """要求身份驗證"""
    init_session_state()
    
    # 檢查是否已登入
    if not st.session_state.authenticated:
        # 嘗試從 session 恢復
        if st.session_state.session_id:
            success, email = verify_session(st.session_state.session_id)
            if success:
                st.session_state.authenticated = True
                st.session_state.user_email = email
                return True
        
        # 顯示登入頁面
        show_login_page()
        st.stop()
        return False
    
    return True


def show_user_info():
    """顯示用戶資訊在側邊欄底部"""
    if st.session_state.authenticated:
        st.markdown("---")
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.markdown(f"📧 {st.session_state.user_email}")
        
        if st.button("🚪 登出", use_container_width=True):
            if st.session_state.session_id:
                logout_user(st.session_state.session_id)
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.session_state.session_id = None
            st.rerun()
