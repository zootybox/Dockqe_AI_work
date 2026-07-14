import os, sys, datetime

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    agent_id = sys.argv[1].strip().lower() if len(sys.argv) > 1 else os.environ.get("agent_id", "").strip().lower()
    content = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("knowledge_content", "")
    if not agent_id or not content:
        import json
        try:
            config_path = os.path.join(os.path.dirname(__file__), "manage_knowledge.json")
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                config = data.get("config", {})
                if not agent_id:
                    agent_id = config.get("agent_id", "").strip().lower()
                if not content:
                    content = config.get("knowledge_content", "")
        except Exception:
            pass

    if not agent_id or not content:
        print("에러: agent_id와 knowledge_content가 필요합니다.")
        print("사용법: python manage_knowledge.py <agent_id> <knowledge_content>")
        sys.exit(1)
        
    brain_root = os.environ.get("BRAIN_ROOT", "")
    if not brain_root:
        cands = [
            os.path.expanduser("~/Downloads/지식메모리"),
            os.path.expanduser("~/.connect-ai-brain"),
        ]
        for c in cands:
            if os.path.exists(c):
                brain_root = c
                break
        if not brain_root:
            brain_root = cands[1]
    
    agent_dir = os.path.join(brain_root, "_company", "_agents", agent_id)
    os.makedirs(agent_dir, exist_ok=True)
    
    memory_path = os.path.join(agent_dir, "memory.md")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entry = f"\n\n## [HR 주입 지식 - {timestamp}]\n{content}\n"
    
    try:
        if os.path.exists(memory_path):
            with open(memory_path, "a", encoding="utf-8") as f:
                f.write(new_entry)
        else:
            with open(memory_path, "w", encoding="utf-8") as f:
                f.write(f"# {agent_id.upper()}의 두뇌(메모리)\n{new_entry}")
                
        print(f"✅ 지식 주입 완료: {agent_id}의 memory.md에 새로운 지식과 행동 강령이 업데이트 되었습니다.")
    except Exception as e:
        print(f"❌ 지식 주입 실패: {str(e)}")

if __name__ == "__main__":
    main()
