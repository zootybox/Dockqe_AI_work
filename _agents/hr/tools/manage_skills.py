import os, sys, json, shutil, glob

def get_brain_root():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if "_company" in script_dir:
            brain_root = script_dir.split(os.sep + "_company")[0]
            if os.path.exists(brain_root):
                return brain_root
    except Exception:
        pass

    brain_root = os.environ.get("BRAIN_ROOT", "")
    if not brain_root:
        cands = [
            os.path.expanduser("~/Downloads/지식메모리"),
            os.path.expanduser("~/.connect-ai-brain"),
            os.path.expanduser("~/.publishflow-ai-brain"),
        ]
        for c in cands:
            if os.path.exists(c):
                return c
        return cands[2] # default to .publishflow-ai-brain
    return brain_root

def get_tool_seeds_dir():
    # 후보 1: 개발 모드 워크스페이스
    dev_path = "c:/Users/user/Documents/Publishflow_AI/connect-ai-main/connect-ai-main/assets/tool-seeds"
    if os.path.exists(dev_path):
        return dev_path

    # 후보 2: 사용자 홈 폴더의 extensions 디렉토리 자동 스캔 (Antigravity IDE 또는 VS Code)
    home = os.path.expanduser("~")
    ext_dirs = [
        os.path.join(home, ".antigravity-ide", "extensions"),
        os.path.join(home, ".vscode", "extensions")
    ]
    for ext_dir in ext_dirs:
        if os.path.exists(ext_dir):
            # publishflow-ai 익스텐션 폴더 매칭
            matches = glob.glob(os.path.join(ext_dir, "*publishflow*publishflow-ai-*"))
            if matches:
                # 버전 정렬 등으로 최신 버전의 폴더 선택
                matches.sort()
                latest = matches[-1]
                seeds_path = os.path.join(latest, "assets", "tool-seeds")
                if os.path.exists(seeds_path):
                    return seeds_path
    return None

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    brain_root = get_brain_root()

    # CLI arguments (Fallback to JSON config)
    action = sys.argv[1].strip().lower() if len(sys.argv) > 1 else os.environ.get("action", "").strip().lower()
    agent_id = sys.argv[2].strip().lower() if len(sys.argv) > 2 else os.environ.get("agent_id", "").strip().lower()
    skill_preset = sys.argv[3].strip() if len(sys.argv) > 3 else os.environ.get("skill_preset", "").strip()

    custom_skill_name = sys.argv[4].strip() if len(sys.argv) > 4 else os.environ.get("custom_skill_name", "").strip()
    custom_python_code = sys.argv[5] if len(sys.argv) > 5 else os.environ.get("custom_python_code", "")
    custom_json_schema = sys.argv[6] if len(sys.argv) > 6 else os.environ.get("custom_json_schema", "")
    custom_markdown_guide = sys.argv[7] if len(sys.argv) > 7 else os.environ.get("custom_markdown_guide", "")

    # Fallback to manage_skills.json if inputs are empty
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manage_skills.json")
    if not action:
        try:
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if not action:
                        action = data.get("action", "install").strip().lower()
                    if not agent_id:
                        agent_id = data.get("agent_id", "").strip().lower()
                    if not skill_preset:
                        skill_preset = data.get("skill_preset", "").strip()
                    if not custom_skill_name:
                        custom_skill_name = data.get("custom_skill_name", "").strip()
                    if not custom_python_code:
                        custom_python_code = data.get("custom_python_code", "")
                    if not custom_json_schema:
                        custom_json_schema = data.get("custom_json_schema", "")
                    if not custom_markdown_guide:
                        custom_markdown_guide = data.get("custom_markdown_guide", "")
        except Exception as e:
            print(f"⚠️ 설정 로드 경고: {str(e)}")

    if not action:
        print("에러: action(작업 선택)은 필수 매개변수입니다.")
        print("사용법: python manage_skills.py <action> [agent_id] [skill_preset] ...")
        sys.exit(1)

    # 1. 🔄 RESET ACTION (Factory reset of all skills for all agents)
    if action == "reset":
        print("🔄 모든 에이전트의 스킬 초기화를 진행합니다...")
        
        seeds_dir = get_tool_seeds_dir()
        if not seeds_dir:
            print("❌ 에러: 원본 스킬 라이브러리(assets/tool-seeds) 디렉토리를 찾을 수 없습니다.")
            sys.exit(1)
            
        company_dir = os.path.join(brain_root, "_company")
        agents_dir = os.path.join(company_dir, "_agents")
        
        if not os.path.exists(agents_dir):
            print("ℹ️ 초기화할 에이전트 폴더가 아직 존재하지 않습니다.")
            sys.exit(0)

        # 1-1) Clear all existing tools directories
        try:
            for aid in os.listdir(agents_dir):
                aid_path = os.path.join(agents_dir, aid)
                if os.path.isdir(aid_path):
                    tools_path = os.path.join(aid_path, "tools")
                    if os.path.exists(tools_path):
                        shutil.rmtree(tools_path)
                        print(f"🧹 {aid} 에이전트의 구버전/꼬인 스킬들을 삭제했습니다.")
        except Exception as e:
            print(f"❌ 구버전 스킬 삭제 실패: {str(e)}")
            sys.exit(1)

        # 1-2) Re-seed basic tools for each agent from tool-seeds
        try:
            for aid in os.listdir(seeds_dir):
                seed_aid_path = os.path.join(seeds_dir, aid)
                if os.path.isdir(seed_aid_path):
                    dest_tools_path = os.path.join(agents_dir, aid, "tools")
                    os.makedirs(dest_tools_path, exist_ok=True)
                    
                    for file in os.listdir(seed_aid_path):
                        src_file = os.path.join(seed_aid_path, file)
                        dest_file = os.path.join(dest_tools_path, file)
                        shutil.copy2(src_file, dest_file)
            print("💿 원본 기본 스킬 라이브러리(Seeds)로부터 깨끗한 초기 도구 복원을 마쳤습니다.")
        except Exception as e:
            print(f"❌ 스킬 시딩 복원 실패: {str(e)}")
            sys.exit(1)
            
        # 1-3) Reset custom_agents.json (Clear newly hired custom agents)
        custom_agents_path = os.path.join(company_dir, "_shared", "custom_agents.json")
        if os.path.exists(custom_agents_path):
            try:
                with open(custom_agents_path, "w", encoding="utf-8") as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
                print("👥 채용된 커스텀 직원 목록(custom_agents.json)도 초기화했습니다.")
            except Exception as e:
                print(f"⚠️ 커스텀 직원 목록 초기화 실패: {str(e)}")

        print("🎉 [초기화 완료] 모든 스킬과 인사가 공장 출하 초기 상태로 완벽히 복구되었습니다!")
        sys.exit(0)

    # 2. INSTALL/UNINSTALL ACTIONS (Agent-specific)
    if not agent_id:
        print("에러: 스킬 주입/제거 시에는 agent_id(대상 에이전트)가 필수 매개변수입니다.")
        sys.exit(1)

    target_tools_dir = os.path.join(brain_root, "_company", "_agents", agent_id, "tools")
    os.makedirs(target_tools_dir, exist_ok=True)

    if action == "install":
        # 2-1. Preset installation
        if skill_preset and skill_preset.strip():
            seeds_dir = get_tool_seeds_dir()
            if not seeds_dir:
                print("❌ 에러: 원본 스킬 라이브러리(assets/tool-seeds) 디렉토리를 찾을 수 없습니다.")
                sys.exit(1)
            
            preset_py = None
            preset_json = None
            preset_md = None
            
            for root, dirs, files in os.walk(seeds_dir):
                for file in files:
                    if file == f"{skill_preset}.py":
                        preset_py = os.path.join(root, file)
                    elif file == f"{skill_preset}.json":
                        preset_json = os.path.join(root, file)
                    elif file == f"{skill_preset}.md":
                        preset_md = os.path.join(root, file)

            if not preset_py:
                print(f"❌ 에러: 스킬 라이브러리에서 '{skill_preset}' 스킬을 찾을 수 없습니다.")
                sys.exit(1)

            try:
                shutil.copy2(preset_py, os.path.join(target_tools_dir, f"{skill_preset}.py"))
                if preset_json and os.path.exists(preset_json):
                    shutil.copy2(preset_json, os.path.join(target_tools_dir, f"{skill_preset}.json"))
                if preset_md and os.path.exists(preset_md):
                    shutil.copy2(preset_md, os.path.join(target_tools_dir, f"{skill_preset}.md"))

                print(f"💿 [프리셋 스킬 장착 완료] {agent_id} 에이전트에게 '{skill_preset}' 스킬이 이식되었습니다.")
                print(f"장착 경로: {target_tools_dir}")
            except Exception as e:
                print(f"❌ 프리셋 스킬 장착 실패: {str(e)}")
                sys.exit(1)

        # 2-2. Custom installation
        else:
            if not custom_skill_name or not custom_python_code:
                print("❌ 에러: 프리셋이 비어 있는 경우, 커스텀 스킬명(custom_skill_name)과 파이썬 소스코드(custom_python_code)를 입력해야 합니다.")
                sys.exit(1)

            if custom_skill_name.endswith(".py"):
                custom_skill_name = custom_skill_name[:-3]

            try:
                with open(os.path.join(target_tools_dir, f"{custom_skill_name}.py"), "w", encoding="utf-8") as f:
                    f.write(custom_python_code)
                if custom_json_schema and custom_json_schema.strip():
                    with open(os.path.join(target_tools_dir, f"{custom_skill_name}.json"), "w", encoding="utf-8") as f:
                        f.write(custom_json_schema)
                if custom_markdown_guide and custom_markdown_guide.strip():
                    with open(os.path.join(target_tools_dir, f"{custom_skill_name}.md"), "w", encoding="utf-8") as f:
                        f.write(custom_markdown_guide)

                print(f"✨ [커스텀 스킬 주입 완료] {agent_id} 에이전트에게 커스텀 스킬 '{custom_skill_name}'이 장착되었습니다.")
                print(f"장착 경로: {target_tools_dir}")
            except Exception as e:
                print(f"❌ 커스텀 스킬 주입 실패: {str(e)}")
                sys.exit(1)

    elif action == "uninstall":
        skill_to_remove = skill_preset if (skill_preset and skill_preset.strip()) else custom_skill_name
        if not skill_to_remove:
            print("❌ 에러: 삭제할 스킬명(프리셋 선택 또는 커스텀 스킬명)을 고르거나 입력해 주세요.")
            sys.exit(1)

        if skill_to_remove.endswith(".py"):
            skill_to_remove = skill_to_remove[:-3]

        files_to_remove = [
            os.path.join(target_tools_dir, f"{skill_to_remove}.py"),
            os.path.join(target_tools_dir, f"{skill_to_remove}.json"),
            os.path.join(target_tools_dir, f"{skill_to_remove}.md")
        ]

        removed_count = 0
        for fp in files_to_remove:
            if os.path.exists(fp):
                try:
                    os.remove(fp)
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️ 파일 제거 중 경고 ({fp}): {str(e)}")

        if removed_count > 0:
            print(f"🗑️ [스킬 제거 완료] {agent_id} 에이전트로부터 '{skill_to_remove}' 스킬(관련 파일 {removed_count}개)을 해제하였습니다.")
        else:
            print(f"ℹ️ {agent_id} 에이전트에게 '{skill_to_remove}' 스킬이 장착되어 있지 않습니다. (제거할 파일 없음)")

    else:
        print(f"❌ 에러: 지원되지 않는 작업 타입({action})입니다. 'install', 'uninstall', 'reset'만 지원합니다.")
        sys.exit(1)

if __name__ == "__main__":
    main()
