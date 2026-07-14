# -*- coding: utf-8 -*-
import sys
import os
import json
import requests
from requests.auth import HTTPBasicAuth

def main():
    # 1) 스키마 파라미터 로드
    try:
        config_path = sys.argv[1] if len(sys.argv) > 1 else 'manage_wordpress.json'
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ 설정 파일 로드 실패: {e}")
        sys.exit(1)

    # 자격증명 로드
    wp_url = config.get("WP_URL", "").strip()
    wp_user = config.get("WP_USER", "").strip()
    wp_pass = config.get("WP_PASS", "").strip()

    # 자격증명 검증 및 사용자 요구사항 반영 에러 메시지
    if not wp_user or not wp_pass:
        print("❌ 먼저 코다리 자격증명 입력 후 재요청해주세요.")
        print("💡 워드프레스 사용자명(WP_USER)과 애플리케이션 패스워드(WP_PASS) 설정이 누락되었습니다. 대시보드 [전체 자격증명 일괄 설정]에서 입력 가능합니다.")
        sys.exit(1)

    if not wp_url:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        COMPANY_DIR = os.environ.get('COMPANY_DIR', '').strip()
        if not COMPANY_DIR:
            COMPANY_DIR = os.path.normpath(os.path.join(script_dir, '..', '..', '..'))
        
        shared_cfg = os.path.join(COMPANY_DIR, '_shared', 'wp_config.json')
        if os.path.exists(shared_cfg):
            try:
                with open(shared_cfg, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    wp_url = cfg.get("WP_URL") or cfg.get("wp_url", "")
            except:
                pass

    if not wp_url:
        print("❌ 워드프레스 URL(WP_URL)이 설정되지 않았습니다.")
        sys.exit(1)

    print(f"📡 워드프레스 연결 시도 중: {wp_url} (계정: {wp_user})")

    # 예시 연동: 포스트 목록 가져오기 테스트
    api_url = f"{wp_url}/wp-json/wp/v2/posts"
    try:
        response = requests.get(
            api_url,
            auth=HTTPBasicAuth(wp_user, wp_pass),
            params={"per_page": 5},
            timeout=10
        )
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ 성공적으로 {len(posts)}개의 최신 포스트를 불러왔습니다.")
            for post in posts:
                print(f"   - [{post.get('status')}] {post.get('title', {}).get('rendered')} (ID: {post.get('id')})")
        elif response.status_code in [401, 403]:
            print("❌ 먼저 코다리 자격증명 입력 후 재요청해주세요.")
            print(f"💡 워드프레스 인증 실패 (사용자명: {wp_user}). 발급받은 애플리케이션 패스워드가 올바른지 확인해주세요. (서버 응답: {response.status_code})")
            sys.exit(1)
        else:
            print(f"❌ 워드프레스 API 연동 실패. 상태 코드: {response.status_code}")
            print(response.text[:200])
            sys.exit(1)
    except Exception as e:
        print(f"❌ 워드프레스 연결 중 네트워크 에러 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
