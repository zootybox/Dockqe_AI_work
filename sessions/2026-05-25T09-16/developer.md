# 💻 코다리 — Researcher와 Business 에이전트의 분석 결과 및 요구사항을 반영하여, 최신 인기 키워드 분석 프로그램 개발 계획을 수립하고, 주요 기능(키워드 수집, 분석, 시각화 등)에 대한 기술 스택과 아키텍처를 설계하십시오.

💻 코다리: 작업 시작합니다.

Researcher와 Business 에이전트의 분석 결과와 요구사항을 면밀히 검토했습니다. 애드센스 수익 극대화를 위한 최신 인기 키워드 분석 프로그램 개발 계획을 수립하고, 주요 기능에 대한 기술 스택과 아키텍처를 설계하겠습니다.

---

### **최신 인기 키워드 분석 프로그램 개발 계획 및 아키텍처 설계**

#### **1. 목표**
고수익 키워드 발굴 및 효율적인 관리를 통해 워드프레스 자동 포스팅 시스템의 애드센스 수익을 극대화하는 것을 목표로 합니다. Researcher의 키워드 발굴 방법론과 Business 에이전트의 수익성 평가 기준을 프로그램에 내재화하여, 자동으로 최적의 키워드를 제안하고 그 성과를 시각화할 수 있는 시스템을 구축합니다.

#### **2. 주요 기능 및 요구사항 요약**

*   **키워드 수집:**
    *   Google Keyword Planner, Ahrefs/SEMrush, Google Trends, 네이버 데이터랩 등 다양한 소스에서 키워드 데이터 수집.
    *   월별 검색량, 예상 입찰가, 경쟁률, 트렌드 데이터 포함.
*   **키워드 분석:**
    *   수집된 키워드 데이터 기반으로 수익성 평가 (월별 검색량 1,000 이상, 예상 입찰가 1,000원 이상).
    *   키워드 난이도/경쟁률 분석 (낮거나 중간 수준 우선).
    *   예상 CTR 및 RPM 계산 로직 포함.
*   **시각화 및 관리:**
    *   수익성 높은 키워드 목록 시각화 (테이블, 차트).
    *   키워드 그룹핑, 필터링, 정렬 기능.
    *   키워드별 성과 추이 모니터링 대시보드.
*   **자동화:**
    *   정기적인 키워드 데이터 업데이트 및 재분석.
    *   새로운 고수익 키워드 발견 시 알림 기능.
*   **워드프레스 연동:**
    *   분석된 키워드를 워드프레스 자동 포스팅 시스템에 전달.

#### **3. 기술 스택 (Technology Stack)**

*   **백엔드 (Backend):**
    *   **언어:** Python (강력한 데이터 처리 라이브러리, 웹 스크래핑 용이, Google API 연동 친화적)
    *   **프레임워크:** FastAPI (높은 성능, 비동기 지원, 자동 API 문서화)
    *   **데이터베이스:** PostgreSQL (안정적이고 확장성 높은 관계형 데이터베이스, JSONB 지원으로 유연한 데이터 저장 가능)
    *   **OR/M:** SQLAlchemy (객체-관계 매핑)
    *   **스케줄러:** APScheduler (정기적인 키워드 수집 및 분석 작업 자동화)
    *   **웹 스크래핑/API 클라이언트:** `requests`, `BeautifulSoup4` (웹 스크래핑), Google Ads API Client Library, Ahrefs/SEMrush API Client Libraries (필요시)
*   **프론트엔드 (Frontend):**
    *   **프레임워크:** React.js (재사용 가능한 컴포넌트 기반 UI, 강력한 생태계)
    *   **상태 관리:** React Query (서버 상태 관리 최적화)
    *   **차트 라이브러리:** Recharts 또는 Chart.js (데이터 시각화)
    *   **UI 라이브러리:** Chakra UI 또는 Ant Design (빠른 UI 개발 및 일관된 디자인)
*   **배포 (Deployment):**
    *   **백엔드:** Docker (컨테이너화), Google Cloud Run (서버리스 컨테이너 배포, 자동 스케일링) 또는 AWS ECS Fargate
    *   **프론트엔드:** Cloudflare Pages (빠른 정적 사이트 호스팅, CDN), Vercel 또는 Netlify
    *   **CI/CD:** GitHub Actions (자동화된 테스트 및 배포)
*   **기타:**
    *   **인증:** JWT (JSON Web Tokens) 또는 OAuth 2.0 (Google API 연동 시)

#### **4. 아키텍처 설계**

```mermaid
graph TD
    User[사용자] -- 키워드 분석 요청 --> Frontend(React.js)
    Frontend -- API 호출 --> Backend(FastAPI)
    Backend -- 데이터 조회/저장 --> Database(PostgreSQL)

    subgraph Data Sources
        GoogleKeywordPlanner[Google Keyword Planner API]
        AhrefsAPI[Ahrefs/SEMrush API]
        GoogleTrends[Google Trends (스크래핑/API)]
        NaverDatalab[네이버 데이터랩 (스크래핑/API)]
    end

    Backend -- API/스크래핑 --> DataSources
    Scheduler(APScheduler) -- 정기적 실행 --> Backend

    subgraph Backend Services
        KeywordCollector[키워드 수집 모듈]
        KeywordAnalyzer[키워드 분석 모듈]
        ReportGenerator[리포트 생성 모듈]
    end

    Backend -- 모듈 호출 --> KeywordCollector
    KeywordCollector -- 데이터 저장 --> Database
    Backend -- 모듈 호출 --> KeywordAnalyzer
    KeywordAnalyzer -- 분석 결과 저장 --> Database
    Backend -- 모듈 호출 --> ReportGenerator
    ReportGenerator -- 데이터 조회 --> Database

    Frontend -- 데이터 시각화 --> User
    Backend -- 워드프레스 연동 --> WordPressRESTAPI[워드프레스 REST API]
```

#### **5. 개발 단계별 계획**

1.  **환경 설정:**
    *   Python 가상 환경 설정 및 FastAPI 프로젝트 초기화.
    *   PostgreSQL 데이터베이스 설정 및 ORM (SQLAlchemy) 연동.
    *   React.js 프로젝트 초기화.
2.  **데이터 모델 설계:**
    *   키워드, 분석 결과, 소스별 데이터 등을 저장할 데이터베이스 스키마 설계.
3.  **키워드 수집 모듈 개발:**
    *   Google Keyword Planner API 연동 (최우선).
    *   Google Trends 데이터 수집 로직 구현.
    *   (추후) Ahrefs/SEMrush, 네이버 데이터랩 연동.
4.  **키워드 분석 모듈 개발:**
    *   Researcher 및 Business 에이전트의 기준에 따른 수익성 평가 로직 구현.
    *   월별 검색량, 예상 입찰가, 경쟁률, 예상 CTR, 예상 RPM 계산.
    *   분석 결과 데이터베이스 저장.
5.  **API 엔드포인트 개발 (FastAPI):**
    *   키워드 목록 조회, 상세 정보 조회, 분석 결과 조회 등.
    *   키워드 수집/분석 작업 트리거 API.
6.  **프론트엔드 개발 (React.js):**
    *   키워드 검색 및 목록 표시 UI.
    *   분석 결과 시각화 (테이블, 차트).
    *   필터링, 정렬, 그룹핑 기능 UI.
    *   대시보드 구현.
7.  **스케줄러 구현:**
    *   APScheduler를 이용한 정기적인 키워드 수집 및 분석 작업 자동화.
8.  **워드프레스 연동 모듈:**
    *   분석된 키워드를 워드프레스 자동 포스팅 시스템에 전달하는 API 개발.
9.  **배포 자동화 (CI/CD):**
    *   GitHub Actions를 이용한 테스트 및 Cloud Run/Cloudflare Pages 배포 자동화.

#### **6. 다음 단계**
FastAPI 프로젝트 초기화를 진행하고, 첫 번째 기능인 Google Keyword Planner API 연동을 위한 환경 설정 및 데이터 모델 설계를 시작하겠습니다. Google Ads API 인증 정보를 확보해야 합니다.

📊 평가: 진행중 — 키워드 분석 프로그램의 전체 개발 계획과 아키텍처를 설계했습니다.
📝 다음 단계: FastAPI 프로젝트 초기화 및 Google Keyword Planner API 연동을 위한 환경 설정과 데이터 모델 설계를 진행하겠습니다.
