import streamlit as st
from openai import OpenAI
import json
import os
import re

# --- 1. 避难所基建 ---
CONFIG_FILE = "config.json"
SKILLS_DIR = "skills"

# 自动建设技能存放区
if not os.path.exists(SKILLS_DIR):
    os.makedirs(SKILLS_DIR)

def save_config(api_key):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": api_key}, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f).get("api_key", "")
        except: return ""
    return ""

# --- 2. 泛文本吞噬与蒸馏引擎 (支持 md, txt, json, csv) ---
def get_learned_personas():
    personas_knowledge = ""
    # 支持的技能书格式
    supported_exts = ('.md', '.txt', '.json', '.csv')
    
    if os.path.exists(SKILLS_DIR):
        files = [f for f in os.listdir(SKILLS_DIR) if f.endswith(supported_exts)]
        for file in files:
            try:
                with open(os.path.join(SKILLS_DIR, file), "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if not content: continue
                    
                    role_name = file
                    traits = []
                    
                    # 尝试提取 Markdown 标题
                    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
                    if title_match:
                        role_name = title_match.group(1)
                        
                    # 尝试提取列表项（核心规则）
                    traits = re.findall(r'^[*-]\s+(.*)', content, re.MULTILINE)
                    
                    # 降级方案：如果没有列表项（比如纯 txt 或 json），直接提取前 3 行非空文本
                    if not traits:
                        lines = [line.strip() for line in content.split('\n') if line.strip()]
                        traits = lines[:3]
                    
                    # 组装蒸馏后的人格/技能，并进行 Token 保护（超长截断）
                    personas_knowledge += f"\n🎭 [待命模块: {role_name}]\n"
                    if traits:
                        clean_traits = [t[:60] + "..." if len(t) > 60 else t for t in traits[:8]]
                        personas_knowledge += f"   - 核心设定: {' | '.join(clean_traits)}\n"
            except Exception as e:
                st.error(f"解析技能文件 {file} 失败，已跳过。报错: {e}")
    return personas_knowledge

# --- 3. 大脑识别雷达 ---
def auto_detect_provider(api_key):
    key = api_key.strip()
    if key.startswith("AIza"):
        return {"name": "Gemini 官方", "url": "https://generativelanguage.googleapis.com/v1beta/openai/", "model": "gemini-1.5-flash"}
    elif key.startswith("sk-"):
        return {"name": "DeepSeek / OAI 兼容", "url": "https://api.deepseek.com", "model": "deepseek-chat"}
    return None

# --- 4. 避难所 UI 渲染 ---
st.set_page_config(page_title="PsychClaw 赛博避难所", page_icon="🐾", layout="wide")
saved_key = load_config()

with st.sidebar:
    st.title("🛡️ 避难所中控台")
    api_key_input = st.text_input("🗝️ 丢入 API Key:", value=saved_key, type="password")
    
    if st.button("💾 刻录 DNA (保存 Key)"):
        save_config(api_key_input)
        st.success("DNA 刻录成功，下次免填！")

    config = auto_detect_provider(api_key_input) if api_key_input else None
    if config:
        st.success(f"📡 神经元连接至: {config['name']}")
        target_url = st.text_input("接口地址:", config['url'])
        target_model = st.text_input("模型名称:", config['model'])
    
    if st.button("🏮 重启认知 (清空对话)"):
        st.session_state.messages = []
        st.rerun()

st.title("🐾 PsychClaw 赛博避难所")

# 加载并展示已吞噬的泛格式技能书
learned_personas = get_learned_personas()
if learned_personas:
    with st.expander("📚 查看已加载的跨格式技能/角色库"):
        st.code(learned_personas, language="text")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. 战斗核心：多重人格与技能路由 ---
if prompt := st.chat_input("主理人，丢个需求过来吧..."):
    if not api_key_input or not config:
        st.error("没 Key 避难所就停电了，请先在左侧输入！")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        client = OpenAI(api_key=api_key_input, base_url=target_url)
        
        # 终极版动态 System Prompt
        dynamic_system_prompt = f"""
        你是一个拥有多重人格和多项外挂技能的赛博避难所核心。
        
        【已挂载的技能/角色档案 (来自本地文件)】:
        {learned_personas if learned_personas else "空（仅保留默认设定）"}
        
        【最高行动协议】:
        1. 精准判断主理人（用户）的意图。
        2. 根据意图，自主从[挂载档案]中选择最契合的一个角色或技能进行响应。
        3. 如果主理人只是闲聊，或没有触发任何特定技能文件，请强制使用你的基础底色：“毒舌但心软的赛博避难所主理人”。
        4. 你的回复必须彻底沉浸在选定的角色/技能中。
        5. **绝对禁止**输出“我选择了xx人格”、“根据技能书”、“切换角色中”等暴露 AI 思考过程的废话。直接飙戏/干活！
        """
        
        response = client.chat.completions.create(
            model=target_model,
            messages=[{"role": "system", "content": dynamic_system_prompt}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        reply = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
    except Exception as e:
        error_msg = str(e)
        if "402" in error_msg:
            st.error("❌ 余额不足！主理人，DeepSeek 账户该充钱了。")
        elif "404" in error_msg:
            st.error("❌ 404幽灵再现！检查下节点是不是又飘回香港了。")
        else:
            st.error(f"❌ 系统崩溃，代码: {error_msg}")
