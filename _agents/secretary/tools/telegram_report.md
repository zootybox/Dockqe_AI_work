<!-- version: telegram_report_v1 -->
# 📱 telegram_report 스킬

이 도구는 비서(Secretary) 에이전트가 사장님(성재님)의 텔레그램 채팅방으로 1인 기업 활동 내역, 수익 일일 브리핑, 특이사항 등의 알림을 직접 발송해 주는 자동화 도구입니다.

## 📋 사전 준비 사항
- Python 3 설치 환경
- `requests` 패키지 설치 (`pip install requests`)
- `telegram_report.json` 설정 파일에 봇 토큰 및 챗 아이디 기입

## ⚙️ 설정값 구성 (`telegram_report.json`)
- `BOT_TOKEN` — 텔레그램 봇 토큰 정보 (기본값: `8941848388:AAF5FcCEFPh0bwijALUxfYqa_cO5WfQoHzg`)
- `CHAT_ID` — 메시지를 수신할 사장님 텔레그램 계정 또는 채널 ID (기본값: `7113075354`)

## 🖥️ 실행 방식
```bash
python3 telegram_report.py
```
전송할 텍스트 내용을 인자로 지정하여 직접 발송하거나, 인자가 없으면 디폴트 일일 점검 완료 카드를 전송합니다.
