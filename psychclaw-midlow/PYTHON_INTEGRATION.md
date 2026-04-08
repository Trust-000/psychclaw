# 🐍 Python 项目深度集成指南 (Advanced Integration)

本指南旨在帮助开发者将 **PsychClaw** 的技能逻辑（Skill Logic）无缝嵌入到任何 Python 驱动的 AI 应用、自动化脚本或终端工具中。

---

## 🛠️ 第一步：环境准备 (Dependencies)

PsychClaw 采用 `YAML Frontmatter` 格式管理技能元数据。首先，你需要在你的环境中安装解析库：

```bash
# 在终端中执行以下命令
pip install python-frontmatter
```

---

## 🧠 第二步：核心代码实现 (The Core Function)
将以下函数集成到你的 claw.py 或 main.py 中。该函数负责识别并提取 .md 文档中的“人格灵魂”（System Prompt）。
```Python
import os
import frontmatter

def load_psych_skill(file_path):
    """
    作用：解析 .md 或 .skill 文件，提取其中的系统提示词 (System Prompt)
    参数：file_path (str) - 技能文件的完整路径
    返回：skill_prompt (str) - 提取出的纯文本 Prompt 内容
    """
    
    # 1. 安全性检查：确认文件路径有效
    if not os.path.exists(file_path):
        print(f"❌ [IO_ERROR]: 无法定位文件 -> {file_path}")
        return None

    try:
        # 2. 读取文件：强制使用 UTF-8 编码避免中文乱码
        with open(file_path, 'r', encoding='utf-8') as f:
            # 加载并解析 Frontmatter (即文件开头的 --- 区域)
            post = frontmatter.load(f)
        
        # 3. 提取元数据 (Metadata)
        skill_name = post.get('name', '未命名模块')
        version = post.get('version', '1.0.0')
        
       # 4. 获取核心正文 (System Prompt)
        skill_prompt = post.content
        
        print(f"✅ [PsychClaw_Kernel]: 成功注入技能 [{skill_name}] v{version}")
        return skill_prompt

    except Exception as e:
        print(f"💥 [CRITICAL_ERROR]: 解析过程中发生崩溃。详情: {e}")
        return None
```

---

## 🎮 第三步：实战调用演示 (Quick Start)
你可以通过以下方式在你的 AI 逻辑中调用此模块：
```python
# 假设你的文件结构如下：根目录/psychclaw-midlow/skills/work_buddy.md

# 1. 定义文件路径
SKILL_PATH = "./psychclaw-midlow/skills/USER_GUIDE.md" 

# 2. 执行加载
system_instruction = load_psych_skill(SKILL_PATH)

# 3. 模拟输出确认
if system_instruction:
    print("\n--- 成功提取 Prompt (前 50 字) ---")
    print(system_instruction[:50] + "...")
```

---

## 📝 第四步：Skill 文件标准模板
为了保证解析成功，请确保你的技能文档（.md）开头包含以下格式：
```Markdown
---
name: "名称"
version: "版本号"
author: "你的名字"
---

# 这里是 Prompt 正文
你现在的身份是 PsychClaw，你的任务是陪用户在战壕里熬过这个深夜.
```
<div align="center">
<b>Powered by PsychClaw Engine 🐾</b>
</div>
