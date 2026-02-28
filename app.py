import streamlit as st
import requests

# ==========================================
# ⬇️ 请在下方引号内填写第三方网站提供的信息 ⬇️
# ==========================================
API_BASE_URL = "https://once.novai.su"  
# 2. 从 Streamlit 云端保险箱安全读取密钥 (不要加引号)
API_KEY = st.secrets["THIRD_PARTY_API_KEY"] 
# 3. 填入第三方网站支持的模型名称 (保留引号)
MODEL_NAME = "[次]deepseek-v3.2-speciale" 
# ==========================================

st.set_page_config(page_title="我的 AI 助手", page_icon="🌟")
def check_password():
    """返回 True 表示密码正确，返回 False 表示未解锁"""
    # 1. 如果用户在这个网页已经验证过密码，直接放行
    if st.session_state.get("password_correct", False):
        return True

    # 2. 如果还没验证，显示密码输入框
    st.title("🔒 专属 AI 助手已加密")
    pwd = st.text_input("请输入访问密码：", type="password") # type="password" 会让输入变成小黑点
    
    if pwd:
        # 去云端保险箱里核对密码
        if pwd == st.secrets["APP_PASSWORD"]:
            st.session_state["password_correct"] = True
            st.rerun() # 密码正确，立刻刷新页面显示聊天界面
        else:
            st.error("❌ 密码错误，请重新输入！")
            
    return False

# 检查密码，如果不通过，就让程序在这里停下，不加载后面的聊天代码
if not check_password():
    st.stop()
# ------------------------------------------------
# 🔐 核心密码锁逻辑 结束
# ------------------------------------------------

if not API_BASE_URL or not API_KEY or not MODEL_NAME:
    st.warning("⚠️ 请先在代码顶部填写配置。")
    st.stop()

user_input = st.chat_input("请输入您的问题...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
        
    with st.chat_message("assistant"):
        with st.spinner("请求第三方接口中..."):
            try:
                # 自动为你补全标准的 URL 路径后缀
                url = API_BASE_URL.rstrip("/")
                if not url.endswith("/chat/completions"):
                    if not url.endswith("/v1"):
                        url = f"{url}/v1/chat/completions"
                    else:
                        url = f"{url}/chat/completions"
                        
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": MODEL_NAME,
                    "messages":[{"role": "user", "content": user_input}]
                }
                
                # 发送请求
                response = requests.post(url, headers=headers, json=payload)
                
                # 1. 如果请求成功 (状态码 200)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if "choices" in data:
                            st.write(data["choices"][0]["message"]["content"])
                        else:
                            st.warning("⚠️ 接口返回成功，但格式很奇怪，原始内容如下：")
                            st.write(data)
                    except Exception:
                        st.success("✅ 第三方接口直接返回了纯文本回答：")
                        st.write(response.text)
                        
                # 2. 如果请求失败 (报错)
                else:
                    st.error(f"❌ 接口拒绝了请求！状态码: {response.status_code}")
                    st.info("第三方服务器给出的真实报错原因如下：")
                    st.code(response.text) # 这行会把真实的报错原因打印出来！
                    
            except Exception as e:
                st.error(f"网络连接完全失败：\n{e}")



