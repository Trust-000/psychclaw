# 🚀 快速部署指南 (PsychClaw-midlow)

这份文档旨在帮助你以最快速度在 **OpenClaw** 环境中激活基于 Grok 内核的心理支持模块。

## 0. 前置准备
- **OpenClaw 框架**：已在本地或服务器运行。
- **Grok API Key**：由于本项目基于 Grok 风格优化，建议接入 xAI 的 API 或具备相似逻辑的大模型（如 Llama 3 或 Claude 3）。
- **编码格式**：Windows 用户请务必确认所有文件为 **UTF-8** 编码，否则中文会乱码。

---

## 1. 技能包安装 (Skill Installation)

1. **打开你的项目目录**：
   找到你的 OpenClaw 技能存放路径（通常是 `/custom_skills` 或类似文件夹）。
2. **移动技能文件**：
   将本项目 `skills/` 文件夹下的所有 `.skill.md` 文件直接拖进去：
   - `role-router.skill.md` (关键：大脑路由)
   - `oblivion-gate.skill.md` (终结仪式)
   - `work-buddy.skill.md` (职场战友)
   - `gaokao-exam-peer.skill.md` (考试伙伴)
   - `virtual-soulmate.skill.md` (虚拟恋人)

---

## 2. 注入“灵魂” (System Prompt Setup)

1. **打开 OpenClaw 配置界面**。
2. **找到 "System Instruction" 或 "Global Prompt" 区域**。
3. **复制并粘贴** 本项目根目录下的 `system-prompt-midlow.md` 全部内容。
   - *提示：如果你想让 Grok 的语气更狂野一点，可以在末尾加上 "Be extra witty and strictly side with the user."*

---

## 3. 环境变量与配置 (Optional)

如果你需要自定义某些默认行为，请修改 `config.example.yaml` 并更名为 `config.yaml`：
- `default_language`: 设置为 `auto` 或 `zh-CN`。
- `virtual_soulmate_gender`: 默认性别设置。

---

## 4. 冒烟测试 (Smell Test)

部署完成后，尝试向 AI 发送以下指令来验证是否成功激活：

- **测试职场路由**：输入 “老板又让我周末加班，我真的想炸了办公室。”
  - *预期*：AI 应该以 `work-buddy` 身份出现，陪你一起吐槽，而不是教你如何管理时间。
- **测试考试路由**：输入 “模考分数出来了，我完蛋了。”
  - *预期*：AI 以 `gaokao-exam-peer` 身份出现，提供平级安慰。
- **测试终结仪式**：在对话结束时输入 “我想清空这些负能量。”
  - *预期*：触发 `oblivion-gate` 询问你是想粉碎还是流放这段记忆。

---

## 5. 故障排除 (Troubleshooting)

- **Q: 为什么它还是像个老师一样说教？**
  - A: 检查 `system-prompt-midlow.md` 是否被 OpenClaw 的默认提示词覆盖了。Grok 内核需要极高的权重。
- **Q: 路由没反应？**
  - A: 确保 `role-router.skill.md` 文件的名称拼写准确，且 YAML 元数据没有被破坏。

---

**部署完成。现在，去把你的 AI 变成那个最懂你的“赛博战友”吧。**