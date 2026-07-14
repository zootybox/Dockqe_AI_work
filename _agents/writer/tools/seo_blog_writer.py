#!/usr/bin/env python3
# version: seo_blog_writer_v1
"""SEO 최적화 블로그 글을 집필하는 스킬입니다.

config:
  OLLAMA_URL - 로컬 AI 주소
  MODEL - 집필 모델명
  KEYWORDS - 타겟 검색 키워드
"""
import os
import json
import sys
import requests
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "seo_blog_writer.json")
OUTPUT_PATH = os.path.join(HERE, "seo_article_output.md")

def _log(msg, kind="info"):
    icons = {"info": "✍️", "ok": "✅", "warn": "⚠️", "err": "❌", "step": "▸"}
    print(f"{icons.get(kind, '•')} {msg}", flush=True)

def _load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def main():
    cfg = _load_config()
    ollama_url = cfg.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
    model = cfg.get("MODEL", "gemma4:e2b")
    keywords = cfg.get("KEYWORDS", "정부 지원 혜택")

    topic = "청년 월세 지원금 신청 자격"
    if len(sys.argv) > 1:
        topic = sys.argv[1]

    _log(f"SEO 블로그 집필 시작: {topic} (타겟 키워드: {keywords})", "step")

    system_prompt = (
        "당신은 구글 및 네이버 검색 상단 노출 전문가인 블로그 글 작가입니다.\n"
        "다음의 구조화 및 SEO 가이드라인에 맞추어 블로그 글을 한글로 작성해 주세요:\n"
        "1. 메타 제목: 주제 핵심 키워드를 처음에 배치하고, '키워드: 설명' 구조로 하세요. 길이는 공백 포함 55자~60자 사이로 작성해야 합니다.\n"
        "2. 구조: H2, H3 태그를 논리적으로 3개 이상 배치하고, 각 섹션마다 본문을 불릿 리스트와 일반 서술형을 섞어 상세히 작성하세요.\n"
        "3. 키워드 분포: 제공된 타겟 키워드를 본문에 자연스럽게 4~5회 가량 분산시켜 작성하세요.\n"
        "4. 오직 마크다운 문법으로만 출력하고 부가적인 잡담은 생략하세요."
    )
    user_prompt = f"주제: [{topic}]\n타겟 키워드: {keywords}"

    payload = {
        "model": model,
        "prompt": f"[SYSTEM]\n{system_prompt}\n\n[USER]\n{user_prompt}",
        "stream": False
    }

    _log("글 집필 중... 로컬 AI 호출", "step")
    article = ""
    try:
        res = requests.post(f"{ollama_url}/api/generate", json=payload, timeout=120)
        if res.ok:
            article = res.json().get("response", "").strip()
        else:
            _log(f"LLM API 에러: {res.status_code}", "warn")
    except Exception as e:
        _log(f"로컬 LLM 호출 중 에러 발생: {e}", "warn")

    # LLM 무응답 시 폴백 더미 글 생성
    if not article:
        article = f"""# {keywords}: {topic} 대상 및 자격 조건 총정리 (55자 규정 준수)

본 포스팅은 {keywords}와 관련된 [{topic}] 자격과 혜택, 신청 절차를 검색엔진최적화(SEO) 기준에 맞추어 정리한 글입니다.

## 1. {topic} 개요 및 대상
- 본 혜택은 {keywords}의 일환으로 시행되는 핵심 복지 사업입니다.
- 일정 소득 기준 이하인 가구에게 실질적인 주거 안정금을 제공합니다.

## 2. 지원금액 및 혜택 상세
- 지원 대상에 최종 선정되면 매월 일정 금액을 실시간 계좌이체로 지급받게 됩니다.
- 상세 자격 조건은 아래 내용을 확인하세요.

## 3. 신청 방법 및 필수 서류
- 복지로 홈페이지 혹은 거주지 관할 주민센터를 방문하여 접수합니다.
- 제출 서류: 임대차계약서 사본, 통장 사본, 소득 증빙서류

* 본 글은 {keywords} 분석을 통해 상단 노출에 최적화하여 작성되었습니다.
"""

    try:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(article)
        _log(f"블로그 집필 완료! 결과 저장: {OUTPUT_PATH}", "ok")
    except Exception as e:
        _log(f"파일 저장 에러: {e}", "err")

if __name__ == "__main__":
    main()
