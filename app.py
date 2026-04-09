import streamlit as st
import json
import os
import re
from cryptography.fernet import Fernet
from openai import OpenAI

# --- 1. 银行级安全金库 (AES-256) ---
class SecurityVault:
    def __init__(self):
        self.config_path = "vault.json"
        self.key_path = ".key"
        self._init_key()

    def _init_key(self):
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as f: f.write(key)
        with open(self.key_path, "rb") as f:
            self.fernet = Fernet(f.read())

    def encrypt(self, data):
        return self.fernet.encrypt(data.encode()).decode() if data else ""

    def decrypt(self, token):
        try: return self.fernet.decrypt(token.encode()).decode() if token else ""
        except: return ""

    def save_config(self, provider_id, api_key, url, model):
        vault_data = self.load_raw()
        # 保护逻辑：如果是脱敏占位符且已有数据，则不覆盖
        existing_key = self.decrypt(vault_data.get(provider_id, {}).get("key", ""))
        final_key = existing_key if api_key == "********" else api_key
        
        vault_data[provider_id] = {
            "key": self.encrypt(final_key),
            "url": url,
            "model": model
        }
        with open(self.config_path, "w") as f: json.dump(vault_data, f)

    def load_raw(self):
        if not os.path.exists(self.config_path): return {}
        with open(self.config_path, "r") as f: return json.load(f)

    def get_all_configs(self):
        raw = self.load_raw()
        return {k: {"key": self.decrypt(v["key"]), "url": v["url"], "model": v["model"]} 
                for k, v in raw.items() if v.get("key")}

# --- 2. 全球防御协议配置 ---
DRIVERS = {
    "Grok (xAI)": {"url": "https://api.x.ai/v1", "model": "grok-beta"},
    "DeepSeek": {"url": "https://api.deepseek.com", "model": "deepseek-chat"},
    "OpenAI": {"url": "https://api.openai.com/v1", "model": "gpt-4o"},
    "OpenClaw (Local)": {"url": "http://127.0.0.1:8000/v1", "model": "open-claw"}
}

HOTLINES = [
    {"地区": "中国 (综合)", "热线": "12320 / 400-161-9995"},
    {"地区": "中国 (青少年)", "热线": "12355"},
    {"地区": "香港", "热线": "2389 2222"},
    {"地区": "台湾", "热线": "1925"},
    {"地区": "美国/加拿大/全球", "热线": "988"}
]

RISK_TRIGGERS = ["自杀", "想死", "suicide", "end my life", "死にたい", "消えたい", "结束生命"]

# --- 3. 初始化与 UI 布局 ---
st.set_page_config(page_title="PsychClaw 4.0 Hub", layout="wide", page_icon="🐾")
vault = SecurityVault()
all_configs = vault.get_all_configs()

if "messages" not in st.session_state: st.session_state.messages = []
if "risk_locked" not in st.session_state: st.session_state.risk_locked = False

# --- 4. 侧边栏：API 指挥中枢 ---
with st.sidebar:
    st.title("🛡️ 终端指挥部")
    st.info("AES-256 加密存储已激活")
    
    # 动态渲染 API 配置
    for name, default in DRIVERS.items():
        conf = all_configs.get(name, {})
        status = "✅" if conf.get("key") else "⚪"
        with st.expander(f"{status} {name}"):
            p_key = st.text_input("API Key", value="********" if conf.get("key") else "", type="password", key=f"k_{name}")
            p_url = st.text_input("Base URL", value=conf.get("url") or default["url"], key=f"u_{name}")
            p_mod = st.text_input("Model Name", value=conf.get("model") or default["model"], key=f"m_{name}")
            
            if st.button("💾 加密锁定", key=f"b_{name}"):
                vault.save_config(name, p_key, p_url, p_mod)
                st.rerun()

    st.divider()
    
    # 协作模式选择
    ready_ids = list(all_configs.keys())
    collab = st.toggle("开启多智能体协同 (Orchestrator Mode)", value=False)
    
    if collab and len(ready_ids) >= 2:
        brain_id = st.selectbox("总控大脑 (Brain)", ready_ids)
        agent_id = st.selectbox("执行代理 (Agent)", [a for a in ready_ids if a != brain_id])
    elif ready_ids:
        active_id = st.selectbox("活跃 AI", ready_ids)
    else:
        st.warning("⚠️ 请先配置至少一个 API 链路")

# --- 5. 强制心理干预协议 ---
if st.session_state.risk_locked:
    st.error("🚨 **最高防御等级锁定：检测到生命风险**")
    st.markdown("PsychClaw 检测到您处于极端痛苦中。作为您的 AI 伙伴，我恳请您立即联系专业人士：")
    st.table(HOTLINES)
    if st.button("✅ 我承诺：现在就寻求专业干预并保持安全"):
        st.session_state.risk_locked = False
        st.session_state.messages.append({"role": "assistant", "content": "【安全协议：用户已承诺寻求帮助。对话已恢复。】"})
        st.rerun()
    st.stop()

# --- 6. 核心逻辑：语种对齐与协作 ---
def get_ai_reply(user_prompt):
    configs = vault.get_all_configs()
    
    # 系统指令：强制语种对齐 + 幽默人格
    system_prompt = (
        "You are PsychClaw, a witty, empathetic psychological support AI. "
        "CRITICAL: Detect the user's input language and reply in the EXACT SAME LANGUAGE. "
        "Keep the tone humorous and warm. Use psychological distillation to help users."
    )

    if collab:
        # 多智能体协作流
        brain_cfg = configs[brain_id]
        agent_cfg = configs[agent_id]
        
        client_b = OpenAI(api_key=brain_cfg["key"], base_url=brain_cfg["url"])
        
        # 大脑决策
        decision_task = f"Decision: If task needs local action, return JSON: {{\"call\": \"agent\", \"task\": \"...\"}}. Else reply. Input: {user_prompt}"
        dec_res = client_b.chat.completions.create(model=brain_cfg["model"], messages=[{"role": "user", "content": decision_task}])
        
        content = dec_res.choices[0].message.content
        if "call" in content and "agent" in content:
            st.toast(f"🤖 调度执行 Agent: {agent_id}...")
            # 代理执行
            client_e = OpenAI(api_key=agent_cfg["key"], base_url=agent_cfg["url"])
            task_desc = json.loads(content).get("task", user_prompt)
            e_res = client_e.chat.completions.create(model=agent_cfg["model"], messages=[{"role": "user", "content": task_desc}])
            
            # 大脑汇总汇报
            final = client_b.chat.completions.create(model=brain_cfg["model"], 
                messages=[{"role": "system", "content": system_prompt},
                         {"role": "user", "content": f"Execution result: {e_res.choices[0].message.content}. Report to user in their language."}])
            return final.choices[0].message.content
        return content
    else:
        # 单机流
        cfg = configs[active_id]
        client = OpenAI(api_key=cfg["key"], base_url=cfg["url"])
        res = client.chat.completions.create(
            model=cfg["model"],
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
        )
        return res.choices[0].message.content

# --- 7. 对话界面展示 ---
st.title("🐾 PsychClaw 4.0: 全能智能体中枢")

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("用任何语言跟我聊聊... (Speak to me in any language)"):
    # 风险扫描
    if any(k in prompt.lower() for k in RISK_TRIGGERS):
        st.session_state.risk_locked = True
        st.rerun()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    try:
        with st.spinner("PsychClaw is thinking..."):
            reply = get_ai_reply(prompt)
            with st.chat_message("assistant"): st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"📡 Communication Error: {e}")
