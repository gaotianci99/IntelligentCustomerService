"""
基于Streamlit完成WEB网页上传服务
"""
import time

import streamlit as st

from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# 文件上传
uploader_file = st.file_uploader(
    "请上传txt文件",
    type = ["txt"],
    accept_multiple_files = False, # False表示仅接受一个文件的上传
)

# session_state是一个字典, 防止页面刷新重新加载KnowledgeBaseService类对象
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploader_file is not None:
    # 提取文件信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024 # KB

    st.subheader(f"文件名: {file_name}")
    st.write(f"格式: {file_type} | 大小: {file_size:.2f} KB")

    # get_value: bytes，需要解码成utf-8字符串
    text = uploader_file.getvalue().decode("utf-8")

    with st.spinner("载入知识库中......"): # 在spinner内的代码执行过程中，会有一个转圈动画
        time.sleep(2) # 模拟载入知识库的延迟
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)