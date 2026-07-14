import os, sys, json

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    agent_id = sys.argv[1].strip().lower() if len(sys.argv) > 1 else os.environ.get("agent_id", "").strip().lower()
    name = sys.argv[2].strip() if len(sys.argv) > 2 else os.environ.get("name", "").strip()
    role = sys.argv[3].strip() if len(sys.argv) > 3 else os.environ.get("role", "").strip()
    emoji = sys.argv[4].strip() if len(sys.argv) > 4 else os.environ.get("emoji", "").strip()
    specialty = sys.argv[5].strip() if len(sys.argv) > 5 else os.environ.get("specialty", "기본 업무 수행").strip()

    if not agent_id or not name or not role or not emoji:
        try:
            config_path = os.path.join(os.path.dirname(__file__), "hire_agent.json")
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                config = data.get("config", {})
                if not agent_id:
                    agent_id = config.get("agent_id", "").strip().lower()
                if not name:
                    name = config.get("name", "").strip()
                if not role:
                    role = config.get("role", "").strip()
                if not emoji:
                    emoji = config.get("emoji", "").strip()
                if specialty == "기본 업무 수행" and config.get("specialty"):
                    specialty = config.get("specialty", "").strip()
        except Exception:
            pass

    if not agent_id or not name or not role or not emoji:
        print("에러: 필요한 매개변수(agent_id, name, role, emoji)가 제공되지 않았습니다.")
        print("사용법: python hire_agent.py <agent_id> <name> <role> <emoji> [specialty]")
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
            
    shared_dir = os.path.join(brain_root, "_company", "_shared")
    os.makedirs(shared_dir, exist_ok=True)
    
    custom_agents_path = os.path.join(shared_dir, "custom_agents.json")
    
    custom_agents = {}
    if os.path.exists(custom_agents_path):
        try:
            with open(custom_agents_path, "r", encoding="utf-8") as f:
                custom_agents = json.load(f)
        except:
            pass
            
    custom_agents[agent_id] = {
        "id": agent_id,
        "name": name,
        "role": role,
        "emoji": emoji,
        "color": "#10B981",
        "specialty": specialty,
        "tagline": role + " 업무를 담당합니다",
        "persona": f"프로페셔널한 {role}. 사장님의 지시를 성실히 수행합니다."
    }
    
    try:
        with open(custom_agents_path, "w", encoding="utf-8") as f:
            json.dump(custom_agents, f, ensure_ascii=False, indent=2)
        print(f"✅ 신규 직원 {emoji} {name}({role}) 채용 완료!")
        print(f"이제 '{agent_id}' 아이디로 시스템에 합류하여 다음 업무부터 배정받을 수 있습니다.")
    except Exception as e:
        print(f"❌ 채용 실패: {str(e)}")

if __name__ == "__main__":
    main()
