import streamlit as st
from rag import RagService
import config_data as config

# 1. 页面基础配置 (建议在 st.title 之前)
st.set_page_config(page_title="智能客服助手", page_icon="🤖", layout="centered")

# 2. 标题与样式
st.title("🤖 智能客服助手")
st.caption("基于 LangChain + ChromaDB + 通义千问构建")
st.divider()

# 3. 初始化 Session State
# 使用 "is_first_run" 标记来确保 RagService 只初始化一次，避免刷新页面时重新加载模型导致变慢
if "rag" not in st.session_state:
    with st.spinner("正在加载模型服务，请稍候..."):
        st.session_state["rag"] = RagService()

if "messages" not in st.session_state:  # 建议变量名用复数 messages
    st.session_state["messages"] = [{"role": "assistant", "content": "你好！我是您的智能客服，有什么可以帮您？"}]

# 4. 渲染历史消息
# 使用 st.chat_message 上下文管理器，代码更整洁
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. 处理用户输入
if prompt := st.chat_input("请输入您的问题（例如：我体重180斤，尺码推荐）"):
    # A. 显示用户消息
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # B. 生成 AI 回复
    with st.chat_message("assistant"):
        # 使用 st.status 或 spinner 提示正在思考
        with st.spinner("正在查询知识库并生成回答..."):
            try:
                # 注意：这里假设你的 chain 返回的是字符串流
                # 如果你的 chain 输出是字典（如 {'input': '...', 'context': '...'}），需要调整
                stream = st.session_state["rag"].chain.stream({"input": prompt}, config=config.session_config)

                # 直接使用 st.write_stream 处理生成器，Streamlit 会自动处理流式显示
                # 同时我们需要收集完整回复存入 history
                full_response = st.write_stream(stream)

                # 如果 write_stream 返回 None (旧版本 Streamlit)，则需要手动收集
                if full_response is None:
                    # 兼容旧逻辑，手动收集
                    chunks = []
                    for chunk in stream:
                        chunks.append(chunk)
                    full_response = "".join(chunks)
                    st.write(full_response)

            except Exception as e:
                st.error(f"生成回答时出错: {e}")
                full_response = "抱歉，回答生成失败。"

    # C. 将 AI 回复存入历史
    st.session_state["messages"].append({"role": "assistant", "content": full_response})
