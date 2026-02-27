import streamlit as st
import google.generativeai as genai

# 1. 页面基本设置
st.set_page_config(page_title="我的 AI 助手", page_icon="🌟")
st.title("🌟 我的专属 Gemini AI 助手")

# 2. 安全地读取 API Key (后面会在云端配置，防止泄露)
# 本地测试时，如果报错，可以临时把下面这行改成 api_key = "你的真实API_KEY"
api_key = st.secrets["GEMINI_API_KEY"] 

# 3. 初始化配置 Gemini 模型
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash') # 你在 AI Studio 中测试使用的模型名称

# 4. 创建聊天输入框
user_input = st.chat_input("请输入您的问题...")

if user_input:
    # 显示用户发送的消息
    with st.chat_message("user"):
        st.write(user_input)
        
    # 调用大模型生成回复并显示
    with st.chat_message("assistant"):
        with st.spinner("思考中..."): # 显示加载动画
            response = model.generate_content(user_input)
            st.write(response.text)
