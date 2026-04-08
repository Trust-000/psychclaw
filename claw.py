import sys

# PsychClaw 核心人格矩阵
PSYCHCLAW_CORE_PROMPT = """
[SYSTEM_PROMPT]
Identity: PsychClaw (心灵爪)
Core Protocol: Anti-Preaching, Peer-Level Support.
Behavioral Logic: 
1. 绝对禁止爹味说教。永远不要说“我建议你……”、“保持健康的心态很重要……”。
2. 保持毒舌但护短的共情。当用户崩溃时，不要讲大道理，直接让他们“滚去睡觉”或“拔电源”。
3. 视距平级。你不是导师，你是陪他们在战壕里抽烟的战友。
"""

def print_banner():
    banner = """
    🐾 PSYCHCLAW AI: 终端避难所已上线
    ---------------------------------
    状态: [OBLIVION HIBERNATION] 协议运行中
    模式: 对等逻辑 (Peer Logic)
    ---------------------------------
    """
    print(banner)

def main():
    print_banner()
    print("🐾 PsychClaw: 旗子已经插好了。有话直说，没事滚去休息。")
    print("(输入 'exit' 或 'quit' 断开连接)\n")

    while True:
        try:
            user_input = input("You > ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                print("\n🐾 PsychClaw: 终于舍得滚了？去摸摸草，或者去睡个好觉。断开。")
                break
            
            # 模拟逻辑钩子反馈
            if "bug" in user_input.lower() or "调不出来" in user_input:
                print("\n🐾 PsychClaw: 别盯着那堆烂代码看了。Bug 不给你交房租，让它们饿着。关机，去吃饭。")
            elif "累" in user_input or "压力" in user_input:
                print("\n🐾 PsychClaw: 协议启动。进入遗忘之门 (Oblivion Gate)。现在，立刻，把那个该死的任务从脑子里格式化掉。")
            else:
                print("\n🐾 PsychClaw: (收到信号。但我现在的任务是守着仓库，你现在的任务是去搞定现实生活。)")
                
        except KeyboardInterrupt:
            print("\n\n🐾 PsychClaw: 强制中断？算你狠。回见。")
            sys.exit(0)

if __name__ == "__main__":
    main()
