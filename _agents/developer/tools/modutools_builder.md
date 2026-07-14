<!-- version: modutools_builder_v1 -->
# 🛠 modutools_builder 스킬

이 도구는 `modutools.com` 테마 규격(Pretendard 폰트, 라이트 테마, 둥근 카드 모던 UI)을 충족하는 단일 파일 HTML/JS/CSS 웹 유틸리티를 자동으로 빌드 및 스캐폴딩해 줍니다. 

## 📋 사전 준비 사항
- Python 3 설치 환경
- `requests` 패키지 설치 (`pip install requests`)
- `modutools_builder.json` 에 필요한 로컬 LLM 설정 기입

## ⚙️ 설정값 구성 (`modutools_builder.json`)
- `OLLAMA_URL` — 백엔드 AI 서버 주소 (기본값: `http://127.0.0.1:11434`)
- `MODEL` — 코드 빌드에 사용할 AI 모델명
- `OUTPUT_DIR` — 웹 유틸리티가 빌드되어 저장될 대상 디렉토리 절대 경로

## 🖥️ 실행 방식
```bash
python3 modutools_builder.py
```
도구 스키마 및 공통 모듈 가이드라인을 참조하여 자동으로 프론트엔드 단일 파일을 완성합니다.
