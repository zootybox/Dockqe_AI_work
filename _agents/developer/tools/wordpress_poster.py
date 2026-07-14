#!/usr/bin/env python3
# version: wordpress_poster_v1
"""WordPress REST API를 이용해 글을 자동 발행하는 스킬입니다.

config:
  WP_URL - 워드프레스 주소
  WP_USER - 관리자 ID
  WP_APP_PASSWORD - 앱 비밀번호
  POST_STATUS - 발행 상태 (draft/publish)
  DEFAULT_CATEGORY - 기본 카테고리 ID
"""
import os
import json
import sys
import requests
from base64 import b64encode
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "wordpress_poster.json")
LOG_PATH = os.path.join(HERE, "wordpress_poster_log.md")

def _log(msg, kind="info"):
    icons = {"info": "📝", "ok": "✅", "warn": "⚠️", "err": "❌", "step": "▸"}
    print(f"{icons.get(kind, '•')} {msg}", flush=True)

def _load_config():
    if not os.path.exists(CONFIG_PATH):
        _log("설정 파일이 없습니다. wordpress_poster.json을 먼저 생성해 주세요.", "err")
        sys.exit(1)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        _log(f"설정 파일 읽기 실패: {e}", "err")
        sys.exit(1)

def post_to_wordpress(title, content, excerpt="", tags=None, categories=None):
    cfg = _load_config()
    wp_url = cfg.get("WP_URL", "").rstrip("/")
    user = cfg.get("WP_USER", "")
    app_pw = cfg.get("WP_APP_PASSWORD", "")
    status = cfg.get("POST_STATUS", "draft")
    default_cat = cfg.get("DEFAULT_CATEGORY", 1)

    if not wp_url or not user or not app_pw:
        _log("WP_URL, WP_USER, WP_APP_PASSWORD 설정을 채워주세요.", "err")
        sys.exit(1)

    # 기본 인증 헤더 구성
    creds = f"{user}:{app_pw}"
    encoded_creds = b64encode(creds.encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": f"Basic {encoded_creds}",
        "Content-Type": "application/json"
    }

    # PublishFlow Ad Inserter 광고 배치 표준 적용
    ad_header = '[adinserter disable="7,8,9,10,11"]\n[adinserter block="1"]\n\n'
    ad_mid = '\n\n[adinserter block="2"]\n\n'
    ad_bottom = '\n\n[adinserter block="3"]\n\n[adinserter block="5"]'
    
    full_content = ad_header + content + ad_mid + ad_bottom

    payload = {
        "title": title,
        "content": full_content,
        "excerpt": excerpt,
        "status": status,
        "tags": tags or [],
        "categories": categories or [default_cat]
    }

    _log(f"워드프레스 발행 시도 중: {title}", "step")
    try:
        res = requests.post(
            f"{wp_url}/wp-json/wp/v2/posts",
            headers=headers,
            json=payload,
            timeout=30
        )
    except Exception as e:
        _log(f"서버 접속 오류: {e}", "err")
        sys.exit(1)

    if res.status_code in (200, 201):
        data = res.json()
        link = data.get("link", "")
        post_id = data.get("id", "")
        _log(f"발행 완료! ID: {post_id}, URL: {link}", "ok")

        # 실행 기록 로그 작성
        try:
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(f"- [{datetime.now().strftime('%Y-%m-%d %H:%M')}] {title} 발행 완료 → {link}\n")
        except Exception:
            pass
        return {"id": post_id, "link": link}
    else:
        _log(f"발행 실패: 코드 {res.status_code} — {res.text[:300]}", "err")
        sys.exit(1)

if __name__ == "__main__":
    # 테스트 발행 실행 (인자가 주어지지 않았을 때 샘플 발행)
    if len(sys.argv) > 2:
        title_arg = sys.argv[1]
        content_arg = sys.argv[2]
        post_to_wordpress(title_arg, content_arg)
    else:
        post_to_wordpress(
            title="PublishFlow 스킬 테스트 포스트",
            content="<p>본 포스트는 PublishFlow AI 에이전트 개발자 도구의 wordpress_poster 스킬을 사용해 작성된 테스트 글입니다.</p>",
            excerpt="PublishFlow 스킬 테스트"
        )
