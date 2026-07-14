import requests
from bs4 import BeautifulSoup
import json
import time
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
COMPANY_DIR = os.environ.get('COMPANY_DIR', '').strip()
if not COMPANY_DIR:
    COMPANY_DIR = os.path.normpath(os.path.join(script_dir, '..', '..', '..'))

OUTPUT_FILE = os.path.join(COMPANY_DIR, 'post_audit_raw.json')

def audit_site(url):
    start_time = time.time()
    MAX_EXECUTION_TIME = 25.0  # 타임아웃 방지 안전 마지노선
    
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
    
    # 1. Essential Pages Check
    essential_paths = {
        "Privacy Policy": ["/privacy-policy", "/privacy", "개인정보처리방침"],
        "Terms of Use": ["/terms", "/terms-of-service", "이용약관"],
        "About/Contact": ["/about", "/contact", "소개", "문의"]
    }
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True) if a.get('href')]
        
        for page, keywords in essential_paths.items():
            found = any(any(kw in link for kw in keywords) for link in links)
            if not found:
                summary["missing_pages"].append(page)
                
    except Exception as e:
        summary["seo_issues"].append(f"메인 페이지 접속 실패: {str(e)}")

    # 2. WordPress REST API - 사전 측정 (Sampling)
    try:
        sample_start = time.time()
        api_url = f"{url}/wp-json/wp/v2/posts?per_page=1"
        api_response = requests.get(api_url, timeout=10)
        sample_time = time.time() - sample_start
        
        if api_response.status_code == 200:
            total_posts = int(api_response.headers.get('X-WP-Total', 0))
            summary["total_posts"] = total_posts
            
            if total_posts > 0:
                # 동적 청크 사이즈 (Dynamic Chunking) 계산
                # 응답이 빠르면 50개, 중간 30개, 느리면 10개
                if sample_time < 0.5:
                    per_page = 50
                elif sample_time < 1.0:
                    per_page = 30
                else:
                    per_page = 10
                
                page = 1
                processed_count = 0
                
                while processed_count < total_posts:
                    # 타이머 체크 (25초 초과 시 강제 중단)
                    if time.time() - start_time > MAX_EXECUTION_TIME:
                        summary["status"] = "time_limit_reached"
                        summary["has_more"] = True
                        break
                    
                    # 동적 부하 방지 지연 (Adaptive Delay)
                    if page > 1:
                        # 샘플 측정 시간 기준 1~3초 유동적 쿨타임
                        delay = max(min(sample_time * 1.5, 3.0), 1.0)
                        time.sleep(delay)
                        
                    req_start = time.time()
                    page_url = f"{url}/wp-json/wp/v2/posts?per_page={per_page}&page={page}"
                    page_resp = requests.get(page_url, timeout=15)
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
                        if total_h_tags == 0:
                            reasons.append("구조 부실 (H2/H3 태그 0개)")
                        
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
                    
                    # 다음 루프를 위해 샘플 타임 갱신
                    sample_time = req_time
                    page += 1
                    
                summary["processed_posts"] = processed_count
                summary["risky_count"] = len(risky_content)
        else:
            summary["seo_issues"].append(f"WP REST API 접속 실패 (상태 코드: {api_response.status_code})")
            
    except Exception as e:
        summary["seo_issues"].append(f"API 호출 에러: {str(e)}")

    # 터미널 컨텍스트 오버플로우 방지: 파일로 직접 저장
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(risky_content, f, ensure_ascii=False, indent=2)
    except Exception as e:
        summary["seo_issues"].append(f"파일 저장 실패: {str(e)}")
        
    return summary

if __name__ == "__main__":
    output = audit_site("https://mapbogi.com")
    # 터미널에는 오직 '요약본(Summary)'만 출력하여 에이전트 환각 방지
    print(json.dumps(output, ensure_ascii=False, indent=2))

