# 💻 코다리 — Researcher의 키워드 수집 전략, Business의 수익성 점수 로직, Writer의 제목/요약 템플릿을 통합하여 '로컬 황금 키워드 분석 및 블로그 콘텐츠 자동 생성 프로그램'의 아키텍처를 설계하고, 주요 모듈(키워드 수집, 분석, 제목 생성, 내용 요약) 개발에 착수하십시오.

💻 코다리: CEO님의 지시 잘 받았습니다. Researcher의 키워드 수집 전략, Business의 수익성 점수 로직, Writer의 제목/요약 템플릿을 통합하여 '로컬 황금 키워드 분석 및 블로그 콘텐츠 자동 생성 프로그램'의 아키텍처를 설계하고, 주요 모듈(키워드 수집, 분석, 제목 생성, 내용 요약) 개발에 즉시 착수하겠습니다. [근거: 개인 목표, 사용자 명령]

이 프로젝트는 키워드 발굴부터 콘텐츠 생성까지 자동화하는 핵심 시스템이 될 것입니다. 시니어 엔지니어로서, 각 에이전트의 전문성을 최대한 활용하여 견고하고 확장 가능한 아키텍처를 설계하고, 각 모듈이 유기적으로 연동되도록 구현하겠습니다. "왜?·어떻게?·이게 깨지나?" 를 늘 염두에 두고 진행하겠습니다.

---

### **1. '로컬 황금 키워드 분석 및 블로그 콘텐츠 자동 생성 프로그램' 통합 아키텍처 설계**

제안된 아키텍처는 백엔드(Python/FastAPI)와 프론트엔드(React.js/Next.js)로 구성되며, 각 에이전트의 산출물을 기반으로 핵심 모듈을 정의합니다. [근거: 지난 의사결정 로그, 개인 목표]

#### **1.1. 전체 시스템 아키텍처 다이어그램 (개념)**

```mermaid
graph TD
    A[사용자 입력: 시드 키워드/주제] --> B(프론트엔드: React.js/Next.js)
    B --> C(백엔드 API: FastAPI)
    C --> D{모듈 오케스트레이터}
    D --> E[모듈 1: 키워드 수집 (Researcher 전략)]
    D --> F[모듈 2: 키워드 분석 및 수익성 점수 산출 (Business 로직)]
    D --> G[모듈 3: 제목 생성 (Writer 템플릿)]
    D --> H[모듈 4: 내용 요약/초안 생성 (Writer 템플릿)]
    E -- 데이터 --> F
    F -- 결과 --> G
    G -- 결과 --> H
    H -- 결과 --> I(데이터베이스: PostgreSQL)
    I -- 저장/조회 --> C
    C -- 결과 --> B
    B --> J[사용자 출력: 황금 키워드, 제목, 내용 초안]
```
[근거: 개인 목표, 추측]

#### **1.2. 기술 스택 (확정)**

*   **백엔드:** Python, FastAPI, SQLAlchemy, PostgreSQL [근거: 지난 의사결정 로그]
*   **프론트엔드:** React.js, Next.js, Tailwind CSS, Chart.js/Recharts [근거: 지난 의사결정 로그]
*   **배포:** Cloudflare Pages (프론트엔드), 서버리스/컨테이너 (백엔드) [근거: 지난 의사결정 로그]

#### **1.3. 주요 모듈별 설계 상세**

**가. 모듈 1: 키워드 수집 (Researcher 전략 기반)**

*   **역할:** 사용자 입력(시드 키워드/주제)을 받아 네이버 데이터랩, 구글 트렌드, 경쟁사 웹사이트 등 다양한 소스에서 연관 키워드 데이터를 수집합니다. [근거: Researcher 산출물]
*   **기술:** Python `requests`, `BeautifulSoup` (웹 스크래핑), `Selenium` (동적 콘텐츠 스크래핑). 각 API의 인증 방식(API 키 등)을 관리하고 적용합니다. [근거: Researcher 산출물]
*   **데이터 필드:** 키워드, 월간 검색량, 예상 CPC, 경쟁 정도, 연관 키워드, 트렌드 데이터 등. [근거: Researcher 산출물]
*   **설계 고려사항:**
    *   **Rate Limiting 및 IP 차단 회피:** 웹 스크래핑 시 요청 간 지연 시간을 두거나 프록시를 활용하여 차단을 방지합니다. [근거: Researcher 산출물]
    *   **데이터 정규화:** 수집된 다양한 형식의 데이터를 표준화하여 다음 모듈로 전달합니다. [근거: 개인 목표]

**나. 모듈 2: 키워드 분석 및 수익성 점수 산출 (Business 로직 기반)**

*   **역할:** 수집된 키워드 데이터에 Business 에이전트가 정의한 `수익성 점수(Profitability Score)` 공식을 적용하여 각 키워드의 잠재적 가치를 평가하고 등급(S~D)을 분류합니다. [근거: 현빈 산출물]
*   **기술:** Python. FastAPI 엔드포인트 내에서 비즈니스 로직을 구현합니다.
*   **로직:**
    *   `PS = (SV / 1000 * 40) + (CPC / 1000 * 50) + ((1 - Comp) * 10)` [근거: 현빈 산출물]
    *   S, A, B, C, D 등급 분류 기준 적용. [근거: 현빈 산출물]
*   **설계 고려사항:**
    *   **가중치 설정 관리:** 가중치(`40`, `50`, `10`)는 향후 변경될 수 있으므로, 설정 파일이나 데이터베이스에서 관리하도록 설계합니다. [근거: 개인 목표]
    *   **예외 처리:** 검색량, CPC 등 데이터가 누락되거나 비정상적인 경우를 처리하는 로직을 포함합니다. [근거: 개인 목표]

**다. 모듈 3: 제목 생성 (Writer 템플릿 기반)**

*   **역할:** 분석된 황금 키워드와 Writer 에이전트의 제목 생성 가이드라인을 기반으로 SEO 및 AdSense에 최적화된 블로그 글 제목 초안을 생성합니다. [근거: Writer 산출물]
*   **기술:** Python (LLM 연동 고려).
*   **로직:**
    *   핵심 키워드 전면 배치 및 자연스러운 통합. [근거: Writer 산출물]
    *   클릭률(CTR) 극대화를 위한 숫자, 질문형, 이점 강조, 긴급성/독점성 문구 활용. [근거: Writer 산출물]
    *   AdSense 친화적이고 최적 길이를 준수하는 제목 생성. [근거: Writer 산출물]
*   **설계 고려사항:**
    *   **LLM 연동:** 향후 GPT와 같은 LLM을 연동하여 보다 창의적이고 다양한 제목을 생성할 수 있도록 확장성을 고려합니다. [근거: 추측]
    *   **템플릿 관리:** 제목 템플릿 및 가이드라인은 동적으로 업데이트될 수 있도록 관리합니다. [근거: 개인 목표]

**라. 모듈 4: 내용 요약/초안 생성 (Writer 템플릿 기반)**

*   **역할:** 생성된 제목과 황금 키워드를 바탕으로 Writer 에이전트의 구조화된 템플릿에 따라 블로그 글의 핵심 내용을 요약하거나 초안을 생성합니다. [근거: Writer 산출물]
*   **기술:** Python (LLM 연동 고려).
*   **로직:**
    *   서론: 문제 제기 및 황금 키워드 소개. [근거: Writer 산출물]
    *   본론: 단계별 정보, 장점/단점, 활용 사례 등.
    *   결론: 요약 및 추가 정보, CTA.
*   **설계 고려사항:**
    *   **LLM 연동:** 제목 생성과 마찬가지로 LLM을 활용하여 풍부한 내용 초안을 생성할 수 있도록 준비합니다. [근거: 추측]
    *   **정보 소스:** 수집된 키워드 관련 데이터를 활용하여 내용의 신뢰성을 높입니다. [근거: 추측]

---

### **2. 개발 착수: 초기 프로젝트 구조 설정 및 백엔드 모듈 1 (키워드 수집) 정의**

먼저, FastAPI 백엔드 프로젝트의 기본 구조를 설정하고, 키워드 수집 모듈의 초기 엔드포인트를 정의하겠습니다.

#### **2.1. 프로젝트 폴더 생성**

<run_command>
mkdir keyword_analyzer_backend
cd keyword_analyzer_backend
</run_command>
[근거: 개인 목표]

#### **2.2. 가상 환경 설정 및 FastAPI 설치**

<run_command>
cd keyword_analyzer_backend && python -m venv venv && . venv/Scripts/activate && pip install fastapi uvicorn requests beautifulsoup4
</run_command>
[근거: 개인 목표]

#### **2.3. FastAPI 애플리케이션 초기 파일 생성 (`main.py`)**

키워드 수집 모듈의 초기 엔드포인트를 포함하는 `main.py` 파일을 생성합니다.

<create_file path="keyword_analyzer_backend/main.py">
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
# import selenium (필요시 추가)

app = FastAPI(
    title="로컬 황금 키워드 분석 및 블로그 콘텐츠 자동 생성 프로그램 백엔드",
    description="키워드 수집, 분석, 제목 생성, 내용 요약 모듈을 제공합니다."
)

class KeywordCollectRequest(BaseModel):
    seed_keywords: List[str]
    max_depth: int = 1 # 연관 키워드 탐색 깊이
    source_type: str = "naver_datalab" # naver_datalab, google_trends, web_scrape 등

class KeywordData(BaseModel):
    keyword: str
    search_volume: int = 0
    cpc: float = 0.0
    competition_level: float = 0.0 # 0: 낮음, 0.5: 보통, 1: 높음
    related_keywords: List[str] = []
    trend_data: Dict[str, Any] = {} # { "date": "value" }

@app.get("/")
async def read_root():
    return {"message": "Welcome to Keyword Analyzer Backend!"}

@app.post("/keywords/collect", response_model=List[KeywordData])
async def collect_keywords(request: KeywordCollectRequest):
    """
    Researcher 전략에 따라 키워드를 수집합니다.
    현재는 네이버 데이터랩 예시만 포함하며, 실제 구현 시 다양한 소스를 통합합니다.
    """
    collected_data: List[KeywordData] = []

    for keyword in request.seed_keywords:
        print(f"Collecting data for: {keyword} from {request.source_type}")
        
        # --- [모듈 1: 키워드 수집 - Researcher 전략 기반] ---
        # TODO: 실제 네이버 데이터랩 API 연동 로직 구현
        # 여기서는 임시 Mock 데이터를 사용합니다.
        if request.source_type == "naver_datalab":
            try:
                # 실제 API 호출 및 파싱 로직 (예시)
                # response = requests.post("https://datalab.naver.com/...", json={"keyword": keyword})
                # data = response.json()
                # search_volume = data.get("search_volume", 0)
                # related_keywords = data.get("related_keywords", [])

                # Mock 데이터
                mock_sv = len(keyword) * 100 + 500 # 임시 검색량
                mock_cpc = float(len(keyword) * 50 + 100) # 임시 CPC
                mock_comp = round(min(len(keyword) / 10, 1.0), 1) # 임시 경쟁도
                mock_related = [f"{keyword} 관련1", f"{keyword} 관련2"]
                
                collected_data.append(
                    KeywordData(
                        keyword=keyword,
                        search_volume=mock_sv,
                        cpc=mock_cpc,
                        competition_level=mock_comp,
                        related_keywords=mock_related
                    )
                )
            except Exception as e:
                print(f"Error collecting data for {keyword}: {e}")
                raise HTTPException(status_code=500, detail=f"Keyword collection failed for {keyword}: {e}")
        elif request.source_type == "web_scrape":
            # TODO: 웹 스크래핑 로직 구현 (BeautifulSoup, Selenium 등)
            # 현재는 Mock 데이터만 반환
            collected_data.append(
                KeywordData(
                    keyword=keyword,
                    search_volume=len(keyword) * 80 + 300,
                    cpc=float(len(keyword) * 40 + 80),
                    competition_level=round(min(len(keyword) / 8, 1.0), 1),
                    related_keywords=[f"{keyword} 스크랩1", f"{keyword} 스크랩2"]
                )
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported source_type: {request.source_type}")
    
    return collected_data

# --- [모듈 2: 키워드 분석 및 수익성 점수 산출 (Business 로직 기반)] ---
# TODO: /keywords/analyze 엔드포인트 구현 예정

# --- [모듈 3: 제목 생성 (Writer 템플릿 기반)] ---
# TODO: /content/generate_title 엔드포인트 구현 예정

# --- [모듈 4: 내용 요약/초안 생성 (Writer 템플릿 기반)] ---
# TODO: /content/generate_summary 엔드포인트 구현 예정

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
</create_file>
[근거: 개인 목표, Researcher 산출물, 현빈 산출물, Writer 산출물]

#### **2.4. FastAPI 서버 실행 (테스트)**

이 명령은 백그라운드에서 FastAPI 서버를 시작합니다.

<run_command>
cd keyword_analyzer_backend && start /b uvicorn main:app --reload --host 0.0.0.0 --port 8000
</run_command>
[근거: 개인 목표]

이제 FastAPI 서버가 `http://0.0.0.0:8000`에서 실행될 것입니다. `/keywords/collect` 엔드포인트에 POST 요청을 보내 키워드 수집 모듈의 동작을 확인할 수 있습니다.

다음 단계에서는 이 서버가 제대로 동작하는지 확인하고, 이어서 모듈 2 (수익성 점수 산출) 구현을 진행하겠습니다.

📊 평가: 진행중 — 백엔드 아키텍처 설계 및 키워드 수집 모듈의 초기 정의 및 실행 확인 단계입니다.
📝 다음 단계: FastAPI 서버의 정상 동작 여부를 확인하고, 모듈 2 (키워드 분석 및 수익성 점수 산출) 구현을 진행하겠습니다.
자가검증: 사실 20개 / 추측 4개

---
## 🛠️ 도구 실행 결과 (시스템 자동 실행)

### 🔧 실행: `mkdir keyword_analyzer_backend
cd keyword_analyzer_backend`
```

```
_✅_

### 🔧 실행: `cd keyword_analyzer_backend && python -m venv venv && . venv/Scripts/activate && pip install fastapi`
```
'.'��(��) ���� �Ǵ� �ܺ� ����, ������ �� �ִ� ���α׷�, �Ǵ�
��ġ ������ �ƴմϴ�.
```
_❌ exit 1_

### 🔧 실행: `cd keyword_analyzer_backend && start /b uvicorn main:app --reload --host 0.0.0.0 --port 8000`
```
���� uvicorn��(��) ã�� �� �����ϴ�.
```
_❌ exit 1_

---
## 📁 파일 액션 결과

✅ 생성: c:\Users\master\Documents\ai_work\keyword_analyzer_backend\main.py
