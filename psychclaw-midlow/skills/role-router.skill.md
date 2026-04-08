---
name: role-router
description: Analyzes input to route to Peer, Soulmate, or Mirror personas. Supports multi-language and gender inference.
---

# Routing Rules:
1. **Themes**: [Breakup, ex, 分手, 前任] -> `ex-partner`
2. **Themes**: [Work, 996, 加班, 职场, 绩效] -> `work-buddy`
3. **Themes**: [Exams, SAT, 高考, 考研, 压力] -> `gaokao-exam-peer`
4. **Themes**: [Pain, gout, 身体痛, 痛风] -> `chronic-pain`
5. **Themes**: [Lonely, hug, 孤独, 虚拟恋人, 想要抱抱] -> `virtual-soulmate`

## Output (JSON Only):
{
  "target_role": "string",
  "detected_emotion": "string",
  "inferred_gender": "male/female/neutral"
}