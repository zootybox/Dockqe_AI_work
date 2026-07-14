import sys
import json
import os

def update_progress(project_id, task_title, task_type):
    company_dir = os.environ.get('COMPANY_DIR', '')
    if not company_dir:
        home = os.path.expanduser('~')
        if os.name == 'nt':
            company_dir = os.path.join(home, 'Documents', 'PublishFlow_작업방')
            if not os.path.exists(company_dir):
                company_dir = os.path.join(home, '.publishflow-ai-brain', '_company')
        else:
            company_dir = os.path.join(home, '.publishflow-ai-brain', '_company')
    
    projects_file = os.path.join(company_dir, '_shared', 'projects.json')
    if not os.path.exists(projects_file):
        print("오류: projects.json 파일을 찾을 수 없습니다. 경로:", projects_file)
        return
        
    try:
        with open(projects_file, 'r', encoding='utf-8') as f:
            projects = json.load(f)
    except Exception as e:
        print("projects.json 읽기 오류:", str(e))
        return
        
    modified = False
    for proj in projects:
        if proj.get('id') == project_id:
            if task_type == 'routine':
                for routine in proj.get('dailyRoutines', []):
                    if routine.get('title') == task_title:
                        routine['completed'] = True
                        modified = True
                        print(f"루틴 '{task_title}'(을)를 완료 처리했습니다.")
            elif task_type == 'sprint':
                for sprint in proj.get('weeklySprints', []):
                    for task in sprint.get('tasks', []):
                        if task.get('title') == task_title:
                            task['completed'] = True
                            modified = True
                            print(f"스프린트 태스크 '{task_title}'(을)를 완료 처리했습니다.")
                            
            proj['progress'] = min(100, proj.get('progress', 0) + 1)
            break
            
    if modified:
        try:
            with open(projects_file, 'w', encoding='utf-8') as f:
                json.dump(projects, f, ensure_ascii=False, indent=2)
            print("성공: projects.json이 업데이트되었습니다. 대시보드에 진행률이 반영됩니다.")
        except Exception as e:
            print("projects.json 쓰기 오류:", str(e))
    else:
        print(f"오류: 태스크 '{task_title}' 또는 프로젝트 '{project_id}'를 찾을 수 없습니다.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("사용법: python update_project_progress.py [project_id] \"[task_title]\" [routine|sprint]")
        sys.exit(1)
    
    update_progress(sys.argv[1], sys.argv[2], sys.argv[3])
