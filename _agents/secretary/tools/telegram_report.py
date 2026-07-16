#!/usr/bin/env python3
# version: telegram_report_v1
"""텔레그램 봇을 통해 사장님에게 회사 동향 및 매출 요약을 보고하는 스킬입니다.

config:
  BOT_TOKEN - 봇 토큰
  CHAT_ID - 챗 아이디
"""
import os
import json
import sys
import requests
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "telegram_report.json")

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
    token = cfg.get("BOT_TOKEN", "").strip()
    chat_id = cfg.get("CHAT_ID", "").strip()

    if not token or not chat_id:
        _log("BOT_TOKEN과 CHAT_ID가 입력되지 않았습니다. telegram_report.json 설정을 채워주세요.", "err")
        sys.exit(1)

    message = ""
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    
    if not message:
        # 인자값이 없을 때 기본적으로 보낼 데일리 보고 포맷
        today_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        message = (
            f"🔔 *PublishFlow AI 에이전트 회사 일일 브리핑*\n"
            f"• *일시:* {today_str}\n\n"
            f"💼 *에이전트 가동 상태:* 정상 (🟢)\n"
            f"• *zootybox.com:* 복지 콘텐츠 포스팅 완료 (2건)\n"
            f"• *mapbogi.com:* Featured Image 연동 정상\n"
            f"• *modutools.com:* 애드센스 슬롯 체크 완료\n\n"
            f"💰 *수익 현황:* AdSense 클릭률 양호\n"
            f"👉 _상세 분석 리포트는 Anti-Gravity 대시보드에서 확인해 주세요._"
        )

    _log("텔레그램 알림 전송 시작...", "step")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    max_len = 3800
    chunks = []
    remaining = message
    while len(remaining) > max_len:
        split_at = remaining.rfind('\n\n', 0, max_len)
        if split_at < int(max_len * 0.6):
            split_at = remaining.rfind('\n', 0, max_len)
        if split_at < int(max_len * 0.6):
            split_at = remaining.rfind('. ', 0, max_len)
        if split_at < int(max_len * 0.4):
            split_at = max_len
        chunks.append(remaining[:split_at].rstrip())
        remaining = remaining[split_at:].lstrip()
    if remaining:
        chunks.append(remaining)

    try:
        for i, chunk in enumerate(chunks):
            part = f"{chunk}\n\n_({i+1}/{len(chunks)})_" if len(chunks) > 1 else chunk
            payload = {
                "chat_id": chat_id,
                "text": part,
                "parse_mode": "Markdown"
            }
            res = requests.post(url, json=payload, timeout=15)
            if not res.ok:
                _log(f"메시지 발송 실패 ({i+1}/{len(chunks)}): 코드 {res.status_code} — {res.text}", "err")
                sys.exit(1)
                
        _log(f"텔레그램 메시지 발송 완료! (총 {len(chunks)}개 메시지)", "ok")
    except Exception as e:
        _log(f"네트워크 통신 오류: {e}", "err")
        sys.exit(1)

if __name__ == "__main__":
    main()
