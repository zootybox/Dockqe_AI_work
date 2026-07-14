import requests
import json
import re
import os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
COMPANY_DIR = os.environ.get('COMPANY_DIR', '').strip()
if not COMPANY_DIR:
    COMPANY_DIR = os.path.normpath(os.path.join(script_dir, '..', '..', '..'))
SHARED_DIR = os.path.join(COMPANY_DIR, '_shared')

# 설정 로드
CONFIG_PATH = os.path.join(SHARED_DIR, 'wp_config.json')
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

WP_URL = config['wp_url']
WP_USER = config['wp_username']
WP_PASS = config['wp_password']
AUTH = (WP_USER, WP_PASS)

def get_all_items(endpoint):
    items = []
    page = 1
    while True:
        params = {'per_page': 100, 'page': page}
        response = requests.get(f"{WP_URL}/wp-json/wp/v2/{endpoint}", auth=AUTH, params=params, timeout=30)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        items.extend(data)
        page += 1
    return items

def analyze_content(content_html):
    # HTML 태그 제거
    text = re.sub('<[^<]+?>', '', content_html)
    length = len(text)
    # H2, H3 태그 확인
    has_h2 = '<h2>' in content_html.lower()
    has_h3 = '<h3>' in content_html.lower()
    return text, length, has_h2, has_h3

def main():
    print("🔍 사이트 전수 조사 시작...")
    
    # 1. 포스팅 분석
    posts = get_all_items('posts')
    post_results = []
    total_length = 0
    all_titles = []

    for p in posts:
        title = p['title']['rendered']
        content = p['content']['rendered']
        text, length, h2, h3 = analyze_content(content)
        
        all_titles.append(title)
        total_length += length
        
        # 결격 사유 판별
        reasons = []
        if length < 1000: reasons.append(f"글자수 부족({length}자)")
        if not h2 and not h3: reasons.append("구조화(H2/H3) 누락")
        
        post_results.append({
            "id": p['id'],
            "title": title,
            "length": length,
            "reasons": reasons
        })

    avg_length = total_length / len(posts) if posts else 0
    
    # 2. 주제 일관성 분석 (간이 키워드 분석)
    title_text = " ".join(all_titles)
    # 실제로는 더 정교한 분석이 필요하나, 여기서는 빈도수 기반으로 요약
    
    # 3. 필수 페이지 확인
    pages = get_all_items('pages')
    page_titles = [p['title']['rendered'].lower() for p in pages]
    
    required_pages = {
        "개인정보처리방침": ["privacy", "개인정보"],
        "이용약관": ["terms", "이용약관"],
        "소개페이지": ["about", "소개"]
    }
    
    missing_pages = []
    for page_name, keywords in required_pages.items():
        if not any(any(kw in pt for kw in keywords) for pt in page_titles):
            missing_pages.append(page_name)

    # 최종 보고서 생성
    report = {
        "summary": {
            "total_posts": len(posts),
            "avg_length": avg_length,
            "missing_pages": missing_pages,
            "low_quality_count": len([p for p in post_results if p['reasons']])
        },
        "low_quality_posts": [p for p in post_results if p['reasons']],
        "site_navigation_issues": missing_pages
    }

    # [수정] 하드코딩 절대경로 제거 → SHARED_DIR 변수 사용 (COMPANY_DIR env로 자동 결정)
    output_path = os.path.join(SHARED_DIR, 'site_audit_report.json')
    os.makedirs(SHARED_DIR, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 조사 완료. 보고서 저장됨: {output_path}")
    print(f"RESULT_SUMMARY: {json.dumps(report['summary'], ensure_ascii=False)}")

if __name__ == "__main__":
    main()