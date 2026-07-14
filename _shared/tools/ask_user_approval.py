import os
import sys
import json
import uuid
import datetime

def main():
    if len(sys.argv) < 2:
        print("사용법: python3 ask_user_approval.py \"요청할 승인 내용\"")
        sys.exit(1)

    summary = sys.argv[1]
    
    # 도커 환경에서 _company 폴더의 절대 경로
    approvals_dir = "/root/.publishflow-ai-brain/project/_company/approvals/pending"
    os.makedirs(approvals_dir, exist_ok=True)
    
    ap_id = "sre_" + uuid.uuid4().hex[:12]
    now_iso = datetime.datetime.utcnow().isoformat() + "Z"
    
    title = "공과장(SRE) 장애 원인 분석 및 해결안 승인 요청"
    agent_id = "maintenance"
    kind = "system.troubleshoot.resolve"
    
    # JSON Data
    ap_data = {
        "id": ap_id,
        "agentId": agent_id,
        "title": title,
        "summary": summary,
        "payload": {
            "agent": agent_id,
            "action": "resolve",
            "message": summary
        },
        "kind": kind,
        "createdAt": now_iso
    }
    
    # Markdown Content
    md_content = f"""# ⏳ 승인 대기 — {title}

- **에이전트:** 🔧 공과장
- **종류:** `{kind}`
- **요청 시각:** {now_iso}
- **id:** `{ap_id[-9:]}`

## 요약

{summary}

## 사용자 결정

텔레그램에서 `/approve {ap_id[-9:]}` 또는 `/reject {ap_id[-9:]}` —
사이드바 "승인 대기" 패널에서도 가능합니다.

## payload (실행기에 전달)

```json
{json.dumps(ap_data['payload'], indent=2)}
```
"""
    
    # Write files
    md_path = os.path.join(approvals_dir, f"{ap_id}.md")
    json_path = os.path.join(approvals_dir, f"{ap_id}.json")
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(ap_data, f, indent=2, ensure_ascii=False)
        
    print(f"[SUCCESS] 승인 대기열에 성공적으로 등록했습니다 (ID: {ap_id}).")
    print("사장님의 결재가 완료되면 파이프라인이 다시 가동됩니다. 턴을 종료하십시오.")
    
    # 기존 telegram_report 도구를 호출하여 텔레그램 알림 발송 (os.system)
    try:
        report_msg = f"⏳ *승인 대기 (🔧 공과장)*\n\n{title}\n\n{summary[:300]}\n\n_승인: /approve {ap_id[-9:]} · 거부: /reject {ap_id[-9:]}_"
        telegram_script = os.path.join(os.path.dirname(__file__), "telegram_report.py")
        if os.path.exists(telegram_script):
            os.system(f'python3 "{telegram_script}" "{report_msg}"')
    except Exception as e:
        print("텔레그램 알림 발송 실패:", e)

if __name__ == "__main__":
    main()
