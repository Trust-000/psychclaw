# 🔌 跨 Skill 通用导入教程 (Adapter Guide)

如果你已经有了一个成熟的基于 Claude Code 开发的 Skill（例如 `Auto-Refactor-Bot`），你可以通过以下方式引入 PsychClaw 的灵魂。

## 步骤 1：建立依赖
在你的项目配置文件或 `README` 中声明依赖：
> "Dependency: PsychClaw-midlow/psych-core-adapter"

## 步骤 2：逻辑挂载 (Logic Hook)
在你的 Skill 逻辑中加入以下 Hook 指令：
```markdown
# 引用 PsychClaw 逻辑：
- 在输出技术方案前，先调用 `psych-core-adapter` 进行“情绪对齐”。
- 如果用户表现出沮丧（如：输入包含“烦”、“死掉”、“改不动”），强制切换至 `work-buddy` 模式。