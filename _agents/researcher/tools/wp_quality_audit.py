import requests
import json
import os

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(script_dir, '../../../_shared/wp_config.json')
OUTPUT_PATH = os.path.join(script_dir, '../../../_shared/content_quality_audit_list.json')

def audit():
    if not os.path.exists(CONFIG_PATH):
        print(f"오류: 설정 파일을 찾을 수 없습니다. {CONFIG_PATH}")
        return

    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    wp_url = config['wp_url'].rstrip('/')
    username = config['wp_username']
    password = config['wp_password']
    auth = (username, password)

    all_posts = []
    page = 1
    
    print("WordPress에서 모든 포스트를 불러오는 중...")
    while True:
        url = f"{wp_url}/wp-json/wp/v2/posts?per_page=100&page={page}"
        try:
            response = requests.get(url, auth=auth, timeout=30)
            if response.status_code != 200:
                break
            posts = response.json()
            if not posts:
                break
            all_posts.extend(posts)
            page += 1
        except Exception as e:
            print(f"오류: 페이지 {page}를 불러오는 중 문제가 발생했습니다: {e}")
            break

    print(f"총 불러온 포스트 수: {len(all_posts)}")
    
    report = []
    for post in all_posts:
        content = post.get('content', {}).get('rendered', '')
        title = post.get('title', {}).get('rendered', 'No Title')
        post_id = post.get('id')

        reasons = []
        # Criterion 1: Content Length (Low Value if < 1000 characters)
        content_len = len(content)
        if content_len < 1000:
            reasons.append(f"텍스트 분량 부족 ({content_len}자)")
        
        # Criterion 2: Structure (Low Quality if missing H2/H3 tags)
        if '<h2>' not in content and '<h3>' not in content:
            reasons.append("구조적 결함 (H2/H3 태그 누락)")
        
        # Criterion 3: AI-generated pattern (Basic check for repetitive phrases)
        if "본 포스팅에서는" in content and "살펴보도록 하겠습니다" in content and content_len < 800:
            reasons.append("AI 생성 패턴 감지됨")

        if reasons:
            report.append({
                "id": post_id,
                "title": title,
                "decision": "Delete",
                "reasons": reasons,
                "metrics": {
                    "length": content_len,
                    "has_structure": '<h2>' in content or '<h3>' in content
                }
            })

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"품질 검사 완료. 저품질 포스트 {len(report)}건 발견됨.")
    for r in report[:20]:
        print(f"- [ID: {r['id']}] {r['title'][:40]}... (길이: {r['metrics']['length']}, H2/H3여부: {r['metrics']['has_structure']}) - {', '.join(r['reasons'])}")
    if len(report) > 20:
        print(f"... 외 {len(report) - 20}건 추가.")
    print(f"보고서 저장 완료: {OUTPUT_PATH}")

if __name__ == "__main__":
    audit()
