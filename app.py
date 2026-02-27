import streamlit as st
from openai import OpenAI

# ==========================================
# ⬇️ 请在下方引号内填写第三方网站提供的信息 ⬇️
# ==========================================
API_BASE_URL = "https://once.novai.su"  # 填入模型地址 (例如: "https://api.第三方网站.com/v1")
API_KEY = "sk-rjivzXSFhrH9kpKy6yGOXyskFywGgLkv51cLwuEyTtmkkzWZ"       # 填入密钥 (例如: "sk-xxxxxxxxxxxxxxxxxxxx")
MODEL_NAME = "[次]gemini-2.5-flash"    # 填入模型名称 (例如: "gemini-2.0-flash" 或第三方网站要求填的名字)
# ==========================================


st.set_page_config(page_title="我的 AI 助手", page_icon="🌟")
st.title("🌟 专属 AI 助手 (第三方 API 版)")

# 检查用户是否填写了配置
if not API_BASE_URL or not API_KEY or not MODEL_NAME:
    st.warning("⚠️ 开发者请注意：请先在代码顶部填写 API_BASE_URL, API_KEY 和 MODEL_NAME。")
    st.stop()

# 初始化 AI 客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE_URL
)

# 创建聊天输入框
user_input = st.chat_input("请输入您的问题...")

if user_input:
    # 1. 在屏幕上显示用户的提问
    with st.chat_message("user"):
        st.write(user_input)
        
    # 2. 调用第三方 API 生成回复并显示
    with st.chat_message("assistant"):
        with st.spinner("AI 思考中..."):
            try:
                # 向第三方服务器发送请求
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "user", "content": user_input}
                    ]
                )
                # 提取并打印 AI 的回答
                st.write(response.choices[0].message.content)
                
            except Exception as e:
                # 如果第三方网站连接失败、密钥错误或余额不足，会在这里报错
                st.error(f"❌ 呼叫第三方接口失败，请检查网络或配置。详细错误：\n{e}")
