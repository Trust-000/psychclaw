# 🚀 如何在 Python 项目中加载 PsychClaw Skill

import os
import frontmatter # 建议安装: pip install python-frontmatter

def load_psych_skill(file_path):
    """
    读取 .skill.md 文件，解析 YAML 元数据和 Prompt 内容
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        
    skill_name = post.get('name')
    skill_prompt = post.content
    
    print(f"✅ 已加载技能: {skill_name}")
    return skill_prompt

# 示例：加载“工位战友”
work_buddy_prompt = load_psych_skill("./skills/work-buddy.skill.md")

# 示例：加载“遗忘之门”作为收尾逻辑
oblivion_gate_prompt = load_psych_skill("./skills/oblivion-gate.skill.md")

# 拼接逻辑 (逻辑挂载)
final_system_prompt = f"{work_buddy_prompt}\n\n[Ending Logic]\n{oblivion_gate_prompt}"

print("🚀 现在的 System Prompt 已经具备了‘战友感’和‘终章仪式’！")