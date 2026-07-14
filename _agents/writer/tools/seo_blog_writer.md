<!-- version: seo_blog_writer_v1 -->
# ✍️ seo_blog_writer 스킬

이 도구는 `zootybox.com`의 타겟 유저(정부 복지 혜택, 금융 정보 등)에 맞춰 검색 순위를 높일 수 있는 **SEO 최적화 마크다운 블로그 본문**을 자동 집필해 줍니다. 

제목의 글자수 조건(55~60자) 및 키워드 배치 규칙을 지키고, 본문 내 검색 크롤 예산 분산용 키워드 매핑 및 광고 배치 가이드를 적용합니다.

## 📋 사전 준비 사항
- Python 3 설치 환경
- `requests` 패키지 설치 (`pip install requests`)
- `seo_blog_writer.json` 에 필요한 로컬 LLM 설정 기입

## ⚙️ 설정값 구성 (`seo_blog_writer.json`)
- `OLLAMA_URL` — 백엔드 AI 서버 주소 (기본값: `http://127.0.0.1:11434`)
- `MODEL` — 집필에 사용할 AI 모델명
- `KEYWORDS` — 타겟팅할 주요 검색 키워드 목록 (쉼표로 구분)

## 🖥️ 실행 방식
```bash
python3 seo_blog_writer.py
```
완성된 본문 글은 같은 폴더의 `seo_article_output.md` 파일로 저장되며, 바로 워드프레스에 포스팅할 수 있는 형태로 규격화됩니다.
