import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin

def get_text_length(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return 0
        soup = BeautifulSoup(response.text, 'html.parser')
        # 워드프레스 기본 본문 영역 추출 시도
        content = soup.find('article') or soup.find('main') or soup.find('div', class_='entry-content')
        if content:
            text = content.get_text(separator=' ', strip=True)
            return len(text)
        return len(soup.get_text(separator=' ', strip=True))
    except Exception as e:
        print(f"{url} 가져오기 오류: {e}")
        return 0

def analyze_site(base_url):
    results = {
        "total_posts": 0,
        "average_word_count": 0,
        "post_details": [],
        "essential_pages": {},
        "technical_seo": {},
        "low_value_posts": []
    }

    # 1. 사이트맵 분석 및 포스팅 리스트업
    sitemap_url = urljoin(base_url, 'wp-sitemap.xml')
    try:
        res = requests.get(sitemap_url, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'xml')
            # 포스트 관련 서브 사이트맵 탐색
            post_sitemaps = [loc.text for loc in soup.find_all('loc') if 'post' in loc.text]
            
            all_post_urls = []
            for ps in post_sitemaps:
                ps_res = requests.get(ps, timeout=10)
                ps_soup = BeautifulSoup(ps_res.content, 'xml')
                all_post_urls.extend([loc.text for loc in ps_soup.find_all('loc')])
            
            results["total_posts"] = len(all_post_urls)
            total_length = 0
            
            for url in all_post_urls:
                length = get_text_length(url)
                total_length += length
                results["post_details"].append({"url": url, "length": length})
                if length < 600: # 가치 낮은 콘텐츠 기준 (임의 600자)
                    results["low_value_posts"].append({"url": url, "length": length})
            
            if results["total_posts"] > 0:
                results["average_word_count"] = total_length / results["total_posts"]
    except Exception as e:
        print(f"사이트맵 오류: {e}")

    # 2. 필수 페이지 확인
    essential_slugs = {
        "개인정보처리방침": ["/privacy-policy", "/privacy"],
        "소개": ["/about", "/about-us"],
        "문의": ["/contact", "/contact-us", "/contact-me"]
    }
    
    for page_name, slugs in essential_slugs.items():
        found = False
        for slug in slugs:
            url = base_url + slug
            try:
                res = requests.get(url, timeout=10)
                if res.status_code == 200:
                    results["essential_pages"][page_name] = {"status": "OK", "url": url}
                    found = True
                    break
            except:
                continue
        if not found:
            results["essential_pages"][page_name] = {"status": "MISSING", "url": None}

    # 3. 기술적 SEO 확인 (Sitemap, RSS)
    for tech_page in ["sitemap.xml", "feed"]:
        url = urljoin(base_url, tech_page)
        try:
            res = requests.get(url, timeout=10)
            results["technical_seo"][tech_page] = "OK" if res.status_code == 200 else f"FAIL({res.status_code})"
        except:
            results["technical_seo"][tech_page] = "ERROR"

    return results

if __name__ == "__main__":
    import sys
    # 환경변수 또는 CLI 인자로 URL 주입 가능, 없으면 기본값 사용
    TARGET_URL = os.environ.get("WP_URL", sys.argv[1] if len(sys.argv) > 1 else "https://mapbogi.com")

    # 출력 경로를 스크립트 상대 경로로 동적 계산 (하드코딩 절대경로 제거)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "../../../_shared/adsense_audit_result.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"{TARGET_URL} 분석 중...")
    data = analyze_site(TARGET_URL)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"분석 완료. 결과가 {output_path}에 저장되었습니다.")
