#!/usr/bin/env python3
# version: modutools_builder_v1
"""modutools.com 디자인 가이드에 맞추어 단일 HTML 웹 도구를 생성하는 스킬입니다.

config:
  OLLAMA_URL - 로컬 AI 주소
  MODEL - 코드 생성 모델명
  OUTPUT_DIR - 저장 경로
"""
import os
import json
import sys
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "modutools_builder.json")

def _log(msg, kind="info"):
    icons = {"info": "📡", "ok": "✅", "warn": "⚠️", "err": "❌", "step": "▸"}
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
    out_dir = cfg.get("OUTPUT_DIR", "").strip() or HERE

    tool_name = "퍼센트 계산기"
    if len(sys.argv) > 1:
        tool_name = sys.argv[1]

    _log(f"modutools용 새 도구 빌드 시작: {tool_name}", "step")

    # modutools.com의 디자인 명세 주입
    system_prompt = (
        "당신은 modutools.com의 프론트엔드 개발자입니다.\n"
        "다음 요구사항을 충족하는 웹 도구용 단일 HTML 코드만 작성하세요:\n"
        "1. 스타일링: Pretendard 폰트 탑재, 라이트 테마, 부드러운 회색 외곽선, 둥근 코너(12px), 깔끔한 여백.\n"
        "2. 구조: <div class=\"mt-header\">와 <div class=\"mt-footer\">를 반드시 포함할 것.\n"
        "3. 모든 CSS와 JS는 단일 HTML 파일 내부에 작성할 것.\n"
        "4. 구글 애드센스 광고 영역용 플레이스홀더를 ad-slot-top, ad-slot-bottom 이라는 클래스로 적절히 배치할 것.\n"
        "5. 코드 외부의 설명문이나 ```html 같은 마크다운 코드 블록은 출력하지 말고 오직 원시 HTML 코드만 작성하세요."
    )
    user_prompt = f"[{tool_name}]를 제작해 줘. 한글 입력 인터페이스와 계산 자바스크립트 논리가 완벽히 동작해야 해."

    payload = {
        "model": model,
        "prompt": f"[SYSTEM]\n{system_prompt}\n\n[USER]\n{user_prompt}",
        "stream": False
    }

    _log("로컬 LLM 호출 중... (약 수십 초 소요될 수 있음)", "step")
    html_code = ""
    try:
        res = requests.post(f"{ollama_url}/api/generate", json=payload, timeout=120)
        if res.ok:
            html_code = res.json().get("response", "").strip()
        else:
            _log(f"LLM API 응답 에러: 코드 {res.status_code}", "warn")
    except Exception as e:
        _log(f"로컬 LLM 연동 실패: {e}. 기본 템플릿으로 대체하여 빌드합니다.", "warn")

    # LLM이 응답하지 않거나 에러 발생 시 기본 퍼센트 계산기 스캐폴딩
    if not html_code or "<html" not in html_code:
        html_code = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>modutools - {tool_name}</title>
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
    <style>
        body {{ font-family: 'Pretendard', sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 20px; }}
        .mt-header {{ padding: 15px; border-bottom: 1px solid #e2e8f0; font-weight: bold; font-size: 1.2rem; }}
        .container {{ max-width: 600px; margin: 40px auto; background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); padding: 30px; border: 1px solid #e2e8f0; }}
        input {{ width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #cbd5e1; margin-bottom: 15px; }}
        button {{ background-color: #2563eb; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; }}
        .result {{ margin-top: 20px; font-weight: bold; color: #2563eb; }}
        .ad-slot-top, .ad-slot-bottom {{ background-color: #f1f5f9; padding: 10px; text-align: center; border-radius: 6px; font-size: 0.8rem; color: #64748b; margin: 15px 0; border: 1px dashed #cbd5e1; }}
        .mt-footer {{ text-align: center; margin-top: 40px; color: #64748b; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="mt-header">⚙️ modutools.com</div>
    <div class="container">
        <div class="ad-slot-top">광고 영역: ad-slot-top</div>
        <h2>{tool_name}</h2>
        <p>{tool_name} 웹 도구 템플릿입니다. 세부 계산 논리를 장착해 주세요.</p>
        <input type="number" id="val1" placeholder="값 1 입력" />
        <input type="number" id="val2" placeholder="값 2 입력" />
        <button onclick="calculate()">계산하기</button>
        <div class="result" id="resText">결과 대기 중...</div>
        <div class="ad-slot-bottom">광고 영역: ad-slot-bottom</div>
    </div>
    <div class="mt-footer">© PublishFlow AI. All rights reserved.</div>
    <script>
        function calculate() {{
            const v1 = parseFloat(document.getElementById('val1').value || 0);
            const v2 = parseFloat(document.getElementById('val2').value || 0);
            const res = v1 * (v2 / 100);
            document.getElementById('resText').innerText = "계산 결과: " + res;
        }}
    </script>
</body>
</html>"""

    # clean markup fences if returned by LLM
    if html_code.startswith("```html"):
        html_code = html_code[7:]
    if html_code.endswith("```"):
        html_code = html_code[:-3]
    html_code = html_code.strip()

    safe_name = tool_name.replace(" ", "_").replace("/", "_")
    output_path = os.path.join(out_dir, f"tool-{safe_name}.html")

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_code)
        _log(f"도구 빌드 및 스캐폴딩 완료! 저장 위치: {output_path}", "ok")
    except Exception as e:
        _log(f"파일 쓰기 오류: {e}", "err")

if __name__ == "__main__":
    main()
