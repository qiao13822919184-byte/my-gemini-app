import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI 诊断模式")
st.title("🛠️ AI 助手 - 深度诊断模式")

# 1. 检查 API Key 是否正确配置
st.subheader("第一步：检查 API Key")
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    # 隐藏部分密钥以保护隐私，只显示前后几位
    masked_key = f"{api_key[:5]}...{api_key[-4:]}" if len(api_key) > 10 else "密钥格式可能不正确"
    st.success(f"✅ 成功从云端读取到 API Key！长度为 {len(api_key)} 个字符。({masked_key})")
except KeyError:
    st.error("❌ 找不到 API Key！请确保你在 Streamlit 的 'Advanced settings -> Secrets' 中正确填写了变量名！")
    st.stop()
except Exception as e:
    st.error(f"❌ 读取 API Key 时发生未知错误: {e}")
    st.stop()

# 2. 尝试连接 Google 服务器并获取模型列表
st.subheader("第二步：测试 Google 服务器连接")
genai.configure(api_key=api_key)

try:
    with st.spinner("正在连接 Google 服务器获取可用模型..."):
        # 获取支持生成内容的模型列表
        available_models =[m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
    if not available_models:
        st.warning("⚠️ 连接成功，但你的账号似乎没有任何可用的文本模型。")
        st.stop()
        
    st.success(f"✅ 连接成功！你的 API Key 支持以下 {len(available_models)} 个模型：")
    st.write(available_models)

    # 3. 自动测试对话
    st.subheader("第三步：自动测试对话")
    # 自动挑选列表里的第一个可用模型（通常是 'models/gemini-1.5-flash'）
    target_model = available_models[0]
    st.info(f"👉 正在使用模型 **{target_model}** 进行测试呼叫...")
    
    model = genai.GenerativeModel(target_model)
    response = model.generate_content("你好，请用一句话证明你在线。")
    
    st.success("🎉 测试完美成功！AI 的回复如下：")
    st.code(response.text)
    
    st.balloons() # 播放成功动画

except Exception as e:
    st.error("❌ 呼叫 Google 大模型失败！这就是导致你之前报错的真正原因，请看下方详细信息：")
    # 这里会把 Streamlit 隐藏的真实错误暴露出来
    st.exception(e)
