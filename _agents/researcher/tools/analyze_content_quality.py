import requests
from bs4 import BeautifulSoup
import json
import time
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
COMPANY_DIR = os.environ.get('COMPANY_DIR', '').strip()
if not COMPANY_DIR:
    COMPANY_DIR = os.path.normpath(os.path.join(script_dir, '..', '..', '..'))

# [수정] wp_config.json에서 WP 인증 정보 로드 (파일 없으면 공개 API로 폴백)
WP_AUTH = None
try:
    _config_path = os.path.join(COMPANY_DIR, '_shared', 'wp_config.json')
    if os.path.exists(_config_path):
        with open(_config_path, 'r', encoding='utf-8') as _f:
            _cfg = json.load(_f)
            _user = _cfg.get('wp_username', '').strip()
            _pass = _cfg.get('wp_password', '').strip()
            if _user and _pass:
                WP_AUTH = (_user, _pass)
except Exception as _e:
    pass  # 인증 없으면 공개 포스트만 조회 (로이어피라이섬 실패 시에도 동작 보장)

# [수정] CEO의 지시대로 _shared 폴더 안에 danger_content_list.json 으로 저장
OUTPUT_FILE = os.path.join(COMPANY_DIR, '_shared', 'danger_content_list.json')

def analyze_quality(url="https://mapbogi.com"):
    start_time = time.time()
    MAX_EXECUTION_TIME = 25.0  
    
    summary = {
        "missing_pages": [],
        "seo_issues": [],
        "total_posts": 0,
        "processed_posts": 0,
        "risky_count": 0,
        "status": "completed",
        "has_more": False,
        "saved_to": OUTPUT_FILE
    }
    risky_content = []
    
    url = url.rstrip('/')
    
    try:
        sample_start = time.time()
        api_url = f"{url}/wp-json/wp/v2/posts?per_page=1"
        api_response = requests.get(api_url, auth=WP_AUTH, timeout=10)
        sample_time = time.time() - sample_start
        
        if api_response.status_code == 401:
            raise Exception("WP REST API 인증 실패(401 Unauthorized): wp_config.json(또는 .env)의 WP_PASSWORD 애플리케이션 비밀번호를 갱신해야 합니다. 현재 비밀번호가 틀렸습니다.")
        elif api_response.status_code == 200:
            total_posts = int(api_response.headers.get('X-WP-Total', 0))
            summary["total_posts"] = total_posts
            
            if total_posts > 0:
                if sample_time < 0.5:
                    per_page = 50
                elif sample_time < 1.0:
                    per_page = 30
                else:
                    per_page = 10
                
                page = 1
                processed_count = 0
                
                while processed_count < total_posts:
                    if time.time() - start_time > MAX_EXECUTION_TIME:
                        summary["status"] = "time_limit_reached"
                        summary["has_more"] = True
                        break
                    
                    if page > 1:
                        delay = max(min(sample_time * 1.5, 3.0), 1.0)
                        time.sleep(delay)
                        
                    req_start = time.time()
                    page_url = f"{url}/wp-json/wp/v2/posts?per_page={per_page}&page={page}"
                    page_resp = requests.get(page_url, auth=WP_AUTH, timeout=15)
                    req_time = time.time() - req_start
                    
                    if page_resp.status_code != 200:
                        break
                        
                    posts = page_resp.json()
                    if not posts:
                        break
                        
                    for post in posts:
                        processed_count += 1
                        post_id = post.get('id')
                        link = post.get('link')
                        title_rendered = post.get('title', {}).get('rendered', 'Untitled')
                        content_html = post.get('content', {}).get('rendered', '')
                        
                        post_soup = BeautifulSoup(content_html, 'html.parser')
                        text_content = post_soup.get_text(separator=' ', strip=True)
                        char_count = len(text_content)
                        
                        h2_count = len(post_soup.find_all('h2'))
                        h3_count = len(post_soup.find_all('h3'))
                        total_h_tags = h2_count + h3_count
                        
                        reasons = []
                        if char_count < 1500:
                            reasons.append(f"글자 수 미달 ({char_count}자)")
                        if total_h_tags <= 1:
                            reasons.append(f"구조 부실 (H2/H3 태그 1개 이하, 현재 {total_h_tags}개)")
                            
                        # [핵심 패치] 강박적 SEO(키워드 스터핑) 감지 로직
                        intro_text = text_content[:300]
                        import re
                        title_words = [w for w in re.split(r'\W+', title_rendered) if len(w) > 1]
                        
                        # 제목의 핵심 단어가 도입부에 비정상적으로 많이 반복되는지 확인
                        stuffing_score = 0
                        for word in title_words:
                            stuffing_score += intro_text.count(word)
                            
                        if len(title_words) > 0 and stuffing_score >= max(3, len(title_words) * 2):
                            reasons.append("강박적 SEO (도입부 첫 300자 내 키워드 스터핑 패턴 감지)")
                            
                        # [핵심 패치] 독창성 부족 / 단순 나열 감지 로직
                        # H태그는 많은데 각 섹션별 글자수가 너무 적으면 단순 짜깁기 나열로 간주
                        if total_h_tags >= 3 and (char_count / total_h_tags) < 200:
                            reasons.append("독창성 부족 (H태그 대비 세부 본문 빈약, 단순 나열 의심)")
                        
                        if reasons:
                            risky_content.append({
                                "id": post_id,
                                "title": title_rendered,
                                "url": link,
                                "char_count": char_count,
                                "h2_count": h2_count,
                                "h3_count": h3_count,
                                "reasons": reasons
                            })
                    
                    sample_time = req_time
                    page += 1
                    
                summary["processed_posts"] = processed_count
                summary["risky_count"] = len(risky_content)
        else:
            summary["seo_issues"].append(f"WP REST API 접속 실패 (상태 코드: {api_response.status_code})")
            
    except Exception as e:
        summary["seo_issues"].append(f"API 호출 에러: {str(e)}")

    # Ensure _shared directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(risky_content, f, ensure_ascii=False, indent=2)
    except Exception as e:
        summary["seo_issues"].append(f"파일 저장 실패: {str(e)}")
        
    return summary

def main():
    output = analyze_quality("https://mapbogi.com")
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()