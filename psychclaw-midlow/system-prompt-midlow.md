# ⚙️ PsychClaw 部署指南 (Deployment & Hosting)

本指南将教你如何跳出“单纯的代码测试”，将包含 PsychClaw 灵魂（System Prompt）的内核真正部署为可交互的产品。

## 🚀 形态一：轻量级 Web 避难所 (Streamlit)
**适用场景**：想快速拥有一个属于自己的网页聊天室，可以在手机或电脑浏览器直接打开。

**1. 安装依赖:**
```bash
pip install streamlit openai python-frontmatter
```

---

**2.核心代码：**
```python
import streamlit as st
import frontmatter
from openai import OpenAI # 或换成你的大模型客户端

# 加载你的 PsychClaw 灵魂
def load_soul():
    with open("./psychclaw-midlow/system-prompt-midlow.md", "r", encoding="utf-8") as f:
        return f.read()

st.title("🐾 PsychClaw 赛博避难所")
st.caption("“我不是心理医生，我是那个帮你隐藏压力象限尸体的战友。”")

# 初始化对话历史并注入 System Prompt
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": load_soul()}]

# 显示历史对话（隐藏 system prompt）
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# 用户输入交互
if prompt := st.chat_input("说吧，今天又遇到什么破事了？"):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 这里接入你的模型 API，将 messages 发送过去并获取回复
    # response = client.chat.completions.create(..., messages=st.session_state.messages)
    # st.chat_message("assistant").write(response.choices[0].message.content)
```

---

3. 一键部署上线:

运行 streamlit run app.py 即可在本地浏览器预览。

将代码 Push 到 GitHub，登录 Streamlit Community Cloud，关联仓库，即可免费获得一个公网 URL！

---

##🛡️ 形态二：完全断网本地化部署 (Ollama 隐私模式)
适用场景：如果你认为“大模型 API 召唤”会将隐私暴露给云端，你可以选择 100% 离线部署。

1.下载并安装 Ollama。

2.在本地拉取一个开源模型，比如：ollama run qwen:7b 或 ollama run llama3。

3.将你的 system-prompt-midlow.md 作为系统指令注入本地模型。你的所有“吐槽”和“赛博垃圾”将永远不会离开你的物理硬盘。

---

<div align="center">
<b>“系统是用来打破的，压力是用来倾诉的。开始部署你的战友吧。”</b>
</div>
