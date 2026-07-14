import requests
import json
import os
import argparse
from bs4 import BeautifulSoup

def analyze_post(post):
    """
    단일 포스트의 HTML 본문을 파싱하여 품질 평가(글자 수, H2/H3 태그 개수)를 수행합니다.
    """
    title = post.get('title', {}).get('rendered', '')
    content_html = post.get('content', {}).get('rendered', '')
    soup = BeautifulSoup(content_html, 'html.parser')
    
    # 순수 텍스트(공백, HTML 태그 제외) 글자 수 계산
    pure_text = soup.get_text(separator=' ', strip=True)
    # 글자 수 카운팅 (공백 포함 여부에 따라 달라질 수 있으나, 보통 공백 포함 길이를 기본으로 하되 엄격히 하려면 replace(' ', '') 사용)
    # 여기서는 보수적으로 공백을 제외한 글자 수를 셉니다.
    char_count = len(pure_text.replace(' ', '').replace('\n', ''))
    
    # H 태그 개수 세기
    h2_count = len(soup.find_all('h2'))
    h3_count = len(soup.find_all('h3'))
    
    # 위험도 판별 로직
    # CRITICAL: 글자 수 800자 미만 OR H2 태그 0개
    # WARNING: 글자 수 800~1500자 미만 OR H2 태그 2개 미만
    # SAFE: 그 외 (글자수 >= 1500 AND H2 >= 2)
    
    if char_count < 800 or h2_count == 0:
        status = "CRITICAL"
        reason = "글자 수 800자 미만 또는 H2 태그 누락 (즉시 비공개/삭제 권장)"
    elif char_count < 1500 or h2_count < 2:
        status = "WARNING"
        reason = "글자 수 부족 또는 H2 태그 구조 부실 (내용 보강 필요)"
    else:
        status = "SAFE"
        reason = "기본 요건 충족"

    return {
        'id': post.get('id'),
        'url': post.get('link'),
        'title': title,
        'char_count': char_count,
        'h2_count': h2_count,
        'h3_count': h3_count,
        'status': status,
        'reason': reason
    }

def main():
    parser = argparse.ArgumentParser(description="WordPress AdSense Content Quality Auditor")
    parser.add_argument("--url", default="https://mapbogi.com", help="워드프레스 사이트 URL (기본값: https://mapbogi.com)")
    parser.add_argument("--output", default="C:/Users/user/Documents/Publishflow_AI/Dockqe_AI_work/_company/_shared/danger_content_list.json", help="결과물 저장 경로")
    args = parser.parse_args()

    api_url = f"{args.url.rstrip('/')}/wp-json/wp/v2/posts"
    print(f"🚀 {args.url} 에서 데이터 추출 및 진단 시작...")

    page = 1
    per_page = 100
    all_results = []
    danger_results = []

    while True:
        params = {
            'per_page': per_page,
            'page': page,
            'status': 'publish'
        }
        
        try:
            print(f"⚙️ Fetching page {page}...")
            response = requests.get(api_url, params=params, timeout=30)
            
            if response.status_code == 400:
                # WP API는 더 이상 페이지가 없으면 400을 반환합니다.
                break
                
            response.raise_for_status()
            posts = response.json()
            
            if not posts:
                break
                
            for post in posts:
                analysis = analyze_post(post)
                all_results.append(analysis)
                
                # CRITICAL 또는 WARNING인 위험 콘텐츠만 별도 수집
                if analysis['status'] in ['CRITICAL', 'WARNING']:
                    danger_results.append(analysis)
            
            # 페이지 헤더 확인 (선택 사항)
            total_pages = int(response.headers.get('X-WP-TotalPages', 1))
            if page >= total_pages:
                break
                
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API 요청 에러 (Page {page}): {e}")
            break
        except Exception as e:
            print(f"❌ 알 수 없는 에러 (Page {page}): {e}")
            break

    # 결과 저장 (위험 콘텐츠 리스트)
    output_dir = os.path.dirname(args.output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump({
            "total_posts_analyzed": len(all_results),
            "danger_posts_count": len(danger_results),
            "danger_posts": danger_results
        }, f, ensure_ascii=False, indent=4)
        
    print(f"🏁 진단 완료! 총 {len(all_results)}개의 포스트 중 {len(danger_results)}개의 위험 콘텐츠가 발견되었습니다.")
    print(f"📁 분석 결과가 {args.output} 에 저장되었습니다.")

if __name__ == "__main__":
    main()
