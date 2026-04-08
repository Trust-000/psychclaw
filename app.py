import streamlit as st
import frontmatter
import os

st.set_page_config(page_title="PsychClaw 赛博避难所", page_icon="🐾")

# 你的最优版路径
SOUL_PATH = "./psychclaw-midlow/system-prompt-midlow.md"

def load_soul(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            return post.content
    return None

st.title("🐾 PsychClaw 赛博避难所")
st.caption("“系统是用来打破的，压力是用来倾诉的。”")

if "messages" not in st.session_state:
    soul_content = load_soul(SOUL_PATH)
    if soul_content:
        st.session_state.messages = [{"role": "system", "content": soul_content}]
    else:
        st.error("找不到灵魂文件，请确认在 D:\AI 目录下运行！")
        st.stop()

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("说吧，今天又遇到什么破事了？"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        response = "（Agent 躯体已激活。主理人，请在下一步填入 API Key 来开启我的正式回复。）"
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
