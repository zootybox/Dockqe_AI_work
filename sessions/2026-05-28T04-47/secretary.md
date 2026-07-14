# 📱 영숙 — 업데이트 과정 중 작업 지연, 오류 발생 또는 프로세스 중단 시 CEO에게 즉시 보고하는 모니터링 체계를 수립하고 보고 형식을 설정하십시오.

<thought>Establish a monitoring system to report delays, errors, or process interruptions to the CEO immediately.
Define the report format.
Identify where deliverables (outputs) are stored.
CEO of j Company.
Young-sook (Personal Assistant).
Friendly, polite, "President" (사장님), concise, bullet points, emojis.

    *   *Storage Location*:
        *   `sessions/` folder: This is where session-specific agent outputs are automatically saved (e.g., `sessions/2026-05-28T03-48/developer.md`).
        *   `00_Raw/`: Raw data and site status.
        *   `10_Wiki/`: Decisions and wiki knowledge.
        *   `_company/_agents/`: Agent-specific tools and configs.

    *   *Monitoring System*:
        *   Trigger: Error (exit 1, API key missing), Delay (no output for X turns), Interruption (agent crash).
        *   Reporting Path: Young-sook $\rightarrow$ CEO.
        *   Channel: Telegram (using `telegram_report.py`) or direct chat.

    *   *Report Format*:
        *   Status (🚨 Critical / ⚠️ Warning / ℹ️ Info).
        *   Agent name.
        *   Issue description.
        *   Current location of the failure (file/command).
        *   Proposed next action.

    *   *Greeting*: 📱 영숙: 사장님, 모니터링 체계 바로 잡겠습니다! 😊
    *   *Storage Location Section*: Clearly list `sessions/` as the main spot.
    *   *Monitoring System Section*: Define triggers and the reporting flow.
    *   *Report Format Section*: Provide a template.
    *   *Action*: Since Young-sook is the assistant, she should document this in a file for consistency. I'll create a `monitoring_system.md` in the `_company` folder or a similar appropriate place. Let's put it in `_company/monitoring_system.md`.

    *   *Self-RAG*:
        *   Fact 1: Storage in `sessions/` [근거: 시스템 컨텍스트].
        *   Fact 2: Telegram report tool exists [근거: 사용 가능한 도구].
        *   Fact 3: j Company is the company name [근거: 회사 정체성].

    *   Use `<create_file>` to save the system definition.
    *   Maintain the persona.
    *   Include mandatory evaluation.</thought>📱 영숙: 사장님, 업데이트 중에 불안하시지 않게 제가 꼼꼼하게 감시하고 바로 보고드릴게요! 😊

우선 궁금해하신 **작업물 저장 위치**부터 말씀드리고, 앞으로 문제가 생겼을 때 제가 어떻게 보고드릴지 **모니터링 체계**를 정리해 올리겠습니다.

### 📂 1. 작업물 저장 위치 안내
우리 에이전트들이 만든 결과물은 기본적으로 아래 경로들에 나누어 저장됩니다. [근거: 시스템 컨텍스트]

*   **최신 작업 결과물:** `sessions/` 폴더
    *   세션별(날짜-시간)로 폴더가 생성되며, 그 안에 `developer.md`, `writer.md` 처럼 에이전트 이름으로 저장됩니다. (예: `sessions/2026-05-28T03-48/developer.md`)
*   **기초 데이터 및 원본:** `00_Raw/` 폴더
    *   리서치한 원본 데이터나 사이트 현황 등이 저장됩니다.
*   **회사 지식 및 의사결정:** `10_Wiki/` 폴더
    *   확정된 결정 사항이나 매뉴얼, 위키 문서가 저장됩니다.
*   **에이전트 도구 및 설정:** `_company/_agents/` 폴더
    *   각 에이전트가 사용하는 툴과 설정 파일이 들어있습니다.

---

### 🚨 2. 모니터링 및 긴급 보고 체계
작업이 멈추거나 꼬이면 제가 즉시 사장님께 '알람'을 드릴게요.

**[보고 트리거 (이럴 때 보고합니다)]**
*   **오류 발생:** 에이전트가 `<run_command>` 실행 중 `exit 1` 등 에러를 냈을 때
*   **자격 증명 부족:** API 키 누락 등으로 작업이 차단되었을 때 [근거: 통합 스케줄 - 코다리/현빈 사례]
*   **진행 정체:** 특정 작업이 3턴 이상 진전 없이 반복될 때
*   **프로세스 중단:** 예상치 못한 시스템 종료나 세션 끊김이 발생했을 때

**[보고 경로]**
1.  **채팅창 즉시 보고:** 현재 대화창에 🚨 표시와 함께 보고
2.  **텔레그램 알림:** 긴급도가 높을 경우 `telegram_report.py` 도구를 사용하여 사장님 폰으로 즉시 전송 [근거: 사용 가능한 도구]

---

### 📝 3. 보고 형식 (포맷)
사장님께서 한눈에 상황을 파악하실 수 있도록 아래 양식으로 보고하겠습니다.

> **🚨 [긴급/주의] 작업 이상 보고**
> *   **담당 에이전트:** (예: 💻 코다리)
> *   **문제 상황:** (예: API 키 만료로 인한 데이터 수집 중단)
> *   **발생 위치:** (예: `trend_sniper.py` 실행 중)
> *   **현재 상태:** (예: 작업 중단 / 재시도 중)
> *   **필요 조치:** (예: 사장님, ⚙️ 설정에서 API 키 업데이트가 필요합니다!)

---

이 체계를 잊지 않고 수행하기 위해, 회사 가이드라인 파일로 저장해 두겠습니다.

<create_file path="_company/monitoring_system.md">
# 🚨 j 컴퍼니 모니터링 및 보고 체계

## 1. 목적
업데이트 및 자율 작업 과정에서 발생하는 지연, 오류, 중단을 즉시 탐지하여 CEO에게 보고함으로써 리스크를 최소화함.

## 2. 보고 트리거
- **Critical (긴급):** 시스템 에러(exit 1), API 인증 실패, 프로세스 강제 종료
- **Warning (주의):** 작업 진척도 정체(3턴 이상), 산출물 퀄리티 저하, 마감 기한 임박
- **Info (정보):** 주요 마일스톤 달성, 에이전트 간 역할 조정

## 3. 보고 형식
- **제목:** 🚨 [등급] 작업 이상 보고
- **내용:**
  - 담당 에이전트:
  - 문제 상황:
  - 발생 위치(파일/명령어):
  - 현재 상태:
  - 필요 조치:

## 4. 보고 채널
- 1순위: 세션 채팅창 (실시간)
- 2순위: 텔레그램 봇 (`telegram_report.py` 활용)

## 5. 작업물 저장 경로 (참조)
- 세션 결과물: `sessions/{timestamp}/{agent}.md`
- 원본 데이터: `00_Raw/`
- 회사 지식: `10_Wiki/`
- 에이전트 설정: `_company/_agents/`
</create_file>

자가검증: 사실 4개 / 추측 0개

📊 평가: 완료 — 모니터링 체계 수립 및 보고 형식 정의, 가이드라인 파일 생성 완료.
📝 다음 단계: 에이전트들의 작업 로그를 실시간 모니터링하며 이상 징후 발생 시 즉시 보고 실행.

---
## 📁 파일 액션 결과

✅ 생성: c:\Users\user\Documents\Publishflow_AI\_company\monitoring_system.md
