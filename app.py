import streamlit as st
import requests

# ==========================================
# ⬇️ 请在下方引号内填写第三方网站提供的信息 ⬇️
# ==========================================
API_BASE_URL = "https://once.novai.su"  # 填入模型地址 (例如: "https://api.第三方网站.com/v1")
API_KEY = st.secrets["GEMINI_API_KEY"]
MODEL_NAME = "[次]gemini-2.5-flash"    # 填入模型名称 (例如: "gemini-2.0-flash" 或第三方网站要求填的名字)
# ==========================================

st.set_page_config(page_title="我的 AI 助手", page_icon="🌟")
st.title("🌟 专属 AI 助手 (诊断加强版)")

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


