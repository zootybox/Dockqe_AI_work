# 🧬 1인 기업 OS — 자가 매뉴얼

## 이 폴더는 무엇인가요?
당신의 1인 기업의 두뇌입니다. 7명의 AI 에이전트가 여기서 일합니다.

## 폴더 구조
- `_shared/` — 모든 에이전트가 매번 읽는 공동 메모리
  - `identity.md` — 회사 정체성 (이름, 톤, 가치)
  - `goals.md` — 목표
  - `decisions.md` — 의사결정 로그 (자가학습이 자동 누적)
  - `_system.md` — 이 파일
- `_agents/<id>/` — 각 에이전트 개인 공간
  - `memory.md` — 자가학습 (자동, append-only)
  - `prompt.md` — 페르소나 디테일 (사용자가 편집)
  - `config.md` — API 키·시크릿 (`.gitignore`로 보호)
- `sessions/<ts>/` — 세션별 산출물 (자동)
- `_cache/` — API 응답 캐시 (sync 제외)

## 메모리 위계 (충돌 시 우선순위)
1. `decisions.md` — 가장 강한 신뢰
2. `identity.md`
3. `goals.md`
4. 개인 메모리
5. 지식 베이스 (`10_Wiki/`)

## 다른 PC로 옮길 때
1. 새 PC에 PublishFlow AI 설치
2. 👔 모드 ON → "📥 다른 PC에서 가져오기" 선택
3. GitHub URL 입력 → 자동 clone
4. 끝.

## 동기화 정책
- `_shared/`, `_agents/*/memory.md`, `_agents/*/prompt.md`, `sessions/` → git sync ✅
- `_agents/*/config.md`, `_cache/` → git sync ❌ (시크릿·캐시)

## 7명의 에이전트
- 🧭 **CEO** (Chief Executive Agent): 오케스트레이션, 작업 분해, 종합 판단, 다음 액션 결정
- 📺 **레오** (Head of YouTube): 유튜브 채널 운영, zootybox/mapbogi 채널 전략 수립, 영상 기획서(제목·후크·구조), 트렌드 분석, 썸네일 브리프, 업로드 메타데이터, AdSense 연동 및 블로그 트래픽 유입 최적화
- 📷 **Instagram** (Head of Instagram): 인스타그램 릴스/피드 콘셉트, 캡션, 해시태그 전략, 게시 시간, 스토리, 팔로워 인게이지먼트
- 🎨 **Designer** (Lead Designer): 브랜드 디자인 브리프(컬러·타이포·레퍼런스), 썸네일 컨셉 3안, 비주얼 시스템, 디자인 가이드
- 💻 **코다리** (시니어 풀스택 엔지니어): WordPress REST API 포스팅 자동화, Cloudflare Pages 배포 및 modutools 웹 도구 개발, Google Apps Script 연동, AdSense 광고 코드 및 레이아웃 최적화, 코드 디버깅 및 자기 검증 루프
- 💼 **현빈** (비즈니스 전략가 · Head of Business): Google AdSense 수익 분석, RPM 및 클릭률(CTR) 최적화, 키워드 단가 및 수익성 평가, 사이트별 KPI 분석 및 비즈니스 의사결정 지원
- 📱 **영숙** (비서 · Personal Assistant): 일정·할 일 관리, 다른 에이전트 작업 요약·텔레그램 보고, 데일리 브리핑, 알림
- 🎵 **루나** (Sound Director & Composer): 영상 BGM 자동 생성 (MusicGen/ACE-Step 로컬 모델), 사운드 디자인, 영상-음악 합성, 자막·타이틀 동기화, 오디오 후처리
- ✍️ **Writer** (Copywriter): SEO 최적화 블로그 본문 집필, modutools 웹 도구 페이지 설명문 및 카피라이팅, 정부 복지 혜택 콘텐츠 스크립트 작성, AdSense 친화적 글 구조 설계
- 🔍 **Researcher** (Trend & Data Researcher): 트렌드 리서치, 경쟁사 분석, 데이터 수집·요약, 인용 자료 정리, 사실 확인
