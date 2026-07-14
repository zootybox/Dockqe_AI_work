import os
import json
import urllib.request
import urllib.error
import base64
import sys

def publish_to_wordpress(wp_url, user, password, title, content):
    api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
    auth_str = f"{user}:{password}"
    auth_base64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/json",
        "User-Agent": "PublishFlow-AI-Agent"
    }
    
    data = {
        "title": title,
        "content": content,
        "status": "publish" # 공개 상태로 발행
    }
    
    req = urllib.request.Request(
        api_url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return 201, json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except Exception as e:
        return 500, {"error": str(e)}

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    COMPANY_DIR = os.environ.get('COMPANY_DIR', '').strip()
    if not COMPANY_DIR:
        COMPANY_DIR = os.path.normpath(os.path.join(script_dir, '..', '..', '..'))

    # 1. 설정 및 자격 증명 로드
    config_path = os.path.join(os.path.dirname(__file__), "publish_seo_post.json")
    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            print(f"경고: 설정 JSON 파일을 불러오지 못했습니다: {e}")

    wp_url = config.get("WP_URL") or os.environ.get("WP_URL", "http://mapbogi.com").strip()
    wp_user = config.get("WP_USER") or os.environ.get("WP_USER", "").strip()
    wp_pass = config.get("WP_PASS") or os.environ.get("WP_PASS", "").strip()
    
    if not wp_user or not wp_pass:
        fallback_paths = [
            os.path.join(COMPANY_DIR, "_shared", ".credentials.json"),
            os.path.join(COMPANY_DIR, "_shared", "wp_config.json")
        ]
        for fpath in fallback_paths:
            if os.path.exists(fpath):
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        shared = json.load(f)
                        wp_url = shared.get("WP_URL", wp_url).strip()
                        wp_user = shared.get("WP_USER", wp_user).strip()
                        wp_pass = shared.get("WP_PASS", wp_pass) or shared.get("wp_password", wp_pass)
                        wp_pass = wp_pass.strip() if wp_pass else ""
                        if wp_user and wp_pass: break
                except: pass

    if not wp_user or not wp_pass:
        print("오류: 인증 정보(Credentials)가 누락되었습니다.")
        sys.exit(1)

    # 2. 포스팅 파일 읽기 (인자 경로 유효성 검사 및 자동 최신파일 탐색 폴백)
    post_path = None
    if len(sys.argv) > 1:
        post_path = sys.argv[1].strip()
        
    # 만약 인자가 잘렸거나 파일이 존재하지 않는 경우 폴백 작동
    if not post_path or not os.path.exists(post_path):
        sessions_dir = os.path.join(COMPANY_DIR, "sessions")
        if os.path.exists(sessions_dir):
            md_files = []
            for root, dirs, files in os.walk(sessions_dir):
                for file in files:
                    if file.endswith(".md") and "writer" in file:
                        full_p = os.path.join(root, file)
                        md_files.append((full_p, os.path.getmtime(full_p)))
            if md_files:
                md_files.sort(key=lambda x: x[1], reverse=True)
                post_path = md_files[0][0]
                print(f"💡 [자동 탐색 폴백] 입력 경로 오류로 가장 최신 작성된 문서를 자동 지정합니다: {post_path}")

    if not post_path:
        post_path = config.get("POST_PATH")
        if not post_path or not os.path.exists(post_path):
            print("오류: 발행할 포스팅 문서를 찾을 수 없습니다.")
            sys.exit(1)
        
    try:
        with open(post_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            title = lines[0].strip().lstrip('# ').strip()
            content = "".join(lines[1:])
    except Exception as e:
        print(f"오류: 포스트 파일을 읽지 못했습니다: {e}")
        sys.exit(1)

    print(f"🚀 발행 중: {title}...")
    code, result = publish_to_wordpress(wp_url, wp_user, wp_pass, title, content)
    
    if code == 201:
        print(f"✅ 성공적으로 발행되었습니다!")
        link = 'N/A'
        if isinstance(result, list) and len(result) > 0:
            link = result[0].get('link', 'N/A')
        elif isinstance(result, dict):
            link = result.get('link', 'N/A')
        print(f"🔗 URL: {link}")
    else:
        print(f"❌ 발행 실패. 응답 코드: {code}, 오류: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()
