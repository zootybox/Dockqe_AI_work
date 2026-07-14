<!-- version: wordpress_poster_v1 -->
# 📝 WordPress 자동 포스팅 스킬

이 도구는 `zootybox.com` 또는 `mapbogi.com`과 같은 워드프레스 사이트에 WP REST API를 사용하여 게시물을 임시저장(draft) 또는 즉시 발행(publish)합니다. 

이 스킬이 호출되면 본문의 상·중·하단에 구글 애드센스 광고를 송출하기 위한 Ad Inserter 숏코드와 `[adinserter disable="..."]` 코드가 자동으로 레이아웃에 탑재됩니다.

## 📋 사전 준비 사항
- Python 3 설치 환경
- `requests` 패키지 설치 (`pip install requests`)
- `wordpress_poster.json` 설정 파일에 사이트 정보 및 앱 비밀번호 기입

## ⚙️ 설정값 구성 (`wordpress_poster.json`)
- `WP_URL` — 대상 워드프레스 사이트 주소 (예: `https://zootybox.com`)
- `WP_USER` — 관리자 계정 아이디
- `WP_APP_PASSWORD` — 워드프레스 관리자 프로필에서 생성한 애플리케이션 비밀번호
- `POST_STATUS` — 포스팅 상태 (`draft` 또는 `publish`)
- `DEFAULT_CATEGORY` — 기본 카테고리 ID 번호 (기본값: `1`)

## 🖥️ 실행 방식
```bash
python3 wordpress_poster.py
```
공유 설정 파일인 `youtube_account.json` 등과도 연동하여 공통 변수를 자동으로 탐색합니다.
