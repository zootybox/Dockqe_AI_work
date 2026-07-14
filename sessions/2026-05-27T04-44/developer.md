# 💻 코다리 — WordPress REST API를 활용한 자동 글 작성 프로그램의 핵심 기능(인증, 포스팅, 미디어 업로드) 개발 계획 수립 및 Cloudflare Pages를 통한 배포 방안 구상. Google Apps Script 연동을 통한 자동화 워크플로우 아이디어 제시.

💻 코다리: WordPress REST API를 활용한 자동 글 작성 프로그램 개발 계획 수립 및 Cloudflare Pages 배포, Google Apps Script 연동 자동화 워크플로우 아이디어 제시 요청 확인했습니다. 시니어 엔지니어로서, 이 프로젝트의 핵심 기능을 꼼꼼하게 설계하고, 안정적인 운영 방안까지 고려하여 구체적인 계획을 제시하겠습니다. [근거: 개인 목표]

---

### **1. WordPress REST API 자동 글 작성 프로그램 핵심 기능 개발 계획**

WordPress REST API를 이용한 자동 글 작성 프로그램은 크게 세 가지 핵심 기능으로 구성됩니다.

#### **1.1. 인증 (Authentication)**

*   **목표:** WordPress API에 안전하게 접근하여 글을 작성할 수 있는 권한 확보.
*   **방법:**
    *   **Application Passwords (추천):** WordPress 5.6부터 도입된 `Application Passwords`를 사용하여 특정 애플리케이션에 대한 API 접근 권한을 부여합니다. 이는 사용자 계정 비밀번호 노출 없이 안전하게 API를 사용할 수 있는 방법입니다. [근거: 추측]
        *   **구현:** WordPress 관리자 페이지에서 `사용자 > 프로필`로 이동하여 `새 애플리케이션 비밀번호 추가`를 통해 생성합니다. 생성된 비밀번호는 프로그램 내 환경 변수나 보안 설정 파일에 저장하여 사용합니다.
        *   **인증 헤더:** `Authorization: Basic <base64_encoded(username:application_password)>` 형태로 HTTP 요청 헤더에 포함합니다.
    *   **OAuth 1.0a (대안):** 좀 더 복잡하지만, 사용자 인증 흐름이 필요한 경우 고려할 수 있습니다. 하지만 자동 글 작성에는 Application Passwords가 더 적합합니다. [근거: 추측]
*   **보안 고려사항:**
    *   생성된 Application Password는 외부에 노출되지 않도록 철저히 관리해야 합니다. 환경 변수(`.env` 파일 등)를 사용하고 `.gitignore`에 추가하여 버전 관리 시스템에 포함되지 않도록 합니다.

#### **1.2. 포스팅 (Posting)**

*   **목표:** 제목, 내용, 카테고리, 태그, 상태(초안/공개) 등을 포함하여 WordPress에 새 글을 생성합니다.
*   **WordPress REST API 엔드포인트:** `/wp/v2/posts`
*   **구현:**
    *   **HTTP 메서드:** `POST`
    *   **요청 본문 (JSON):**
        ```json
        {
          "title": "자동 생성된 글 제목",
          "content": "여기에 글 내용이 들어갑니다. HTML 태그 사용 가능합니다.",
          "status": "publish", // 또는 "draft"
          "categories": [1, 2], // 카테고리 ID 배열
          "tags": [3, 4], // 태그 ID 배열
          "featured_media": 5, // 대표 이미지 ID (선택 사항)
          "excerpt": "글 요약 부분입니다.",
          "comment_status": "open"
        }
        ```
    *   **라이브러리:** Python의 `requests` 라이브러리 또는 JavaScript의 `fetch` API를 사용하여 HTTP 요청을 보냅니다.
*   **에러 처리:** API 응답 코드를 확인하여 성공/실패 여부를 판단하고, 실패 시 적절한 로깅 및 재시도 로직을 구현합니다.

#### **1.3. 미디어 업로드 (Media Upload)**

*   **목표:** 글에 필요한 이미지나 기타 미디어 파일을 WordPress 미디어 라이브러리에 업로드하고, 업로드된 미디어의 ID를 포스팅 시 활용합니다.
*   **WordPress REST API 엔드포인트:** `/wp/v2/media`
*   **구현:**
    *   **HTTP 메서드:** `POST`
    *   **요청 헤더:** `Content-Type: multipart/form-data`
    *   **요청 본문:** 파일을 `multipart/form-data` 형식으로 전송합니다.
    *   **예시 (Python `requests`):**
        ```python
        import requests

        wordpress_url = "https://yourdomain.com/wp-json"
        username = "your_username"
        app_password = "your_application_password"

        # 인증 헤더 생성
        auth_header = requests.auth.HTTPBasicAuth(username, app_password)

        # 이미지 파일 열기
        with open("image.jpg", "rb") as f:
            files = {'file': f}
            headers = {'Content-Disposition': 'attachment; filename="image.jpg"'} # 파일 이름 명시

            response = requests.post(
                f"{wordpress_url}/wp/v2/media",
                auth=auth_header,
                headers=headers,
                files=files
            )

        if response.status_code == 201:
            media_id = response.json()['id']
            print(f"미디어 업로드 성공. ID: {media_id}")
        else:
            print(f"미디어 업로드 실패: {response.text}")
        ```
*   **미디어 ID 활용:** 업로드 성공 시 반환되는 미디어 ID를 포스팅 요청 시 `featured_media` 필드나 글 내용(`content`) 내 `<img>` 태그의 `src` 속성에 활용할 수 있습니다.

---

### **2. Cloudflare Pages를 통한 배포 방안**

Cloudflare Pages는 정적 웹사이트 및 프론트엔드 애플리케이션을 빠르고 안정적으로 배포할 수 있는 플랫폼입니다. 자동 글 작성 프로그램의 "프론트엔드" 또는 "제어판" 역할을 하는 웹 인터페이스가 있다면 Cloudflare Pages를 활용할 수 있습니다. 만약 백엔드 스크립트만 있다면 Cloudflare Workers나 자체 서버 호스팅을 고려해야 합니다. 여기서는 웹 인터페이스가 있는 경우를 상정합니다.

*   **장점:**
    *   **글로벌 CDN:** 빠른 콘텐츠 전송 속도.
    *   **무료:** 기본적인 사용은 무료.
    *   **Git 연동:** GitHub, GitLab, Bitbucket 등 Git 저장소와 연동하여 코드 푸시 시 자동 배포.
    *   **커스텀 도메인:** 쉽게 커스텀 도메인을 연결할 수 있습니다.
*   **배포 과정:**
    1.  **프로젝트 생성:** Cloudflare 대시보드에서 `Pages > 프로젝트 생성`을 선택합니다.
    2.  **Git 연동:** 프로그램 코드가 있는 Git 저장소를 연결합니다.
    3.  **빌드 설정:** 빌드 명령어 (예: `npm run build`, `yarn build`)와 빌드 출력 디렉토리 (예: `build`, `dist`)를 설정합니다.
    4.  **환경 변수 설정:** WordPress API 키와 같은 민감한 정보는 Cloudflare Pages의 환경 변수 기능을 사용하여 안전하게 관리합니다. (Build settings > Environment variables)
    5.  **자동 배포:** Git 저장소에 코드를 푸시할 때마다 Cloudflare Pages가 자동으로 빌드하고 배포합니다.
*   **백엔드 스크립트 처리:** 만약 자동 글 작성 로직이 순수 백엔드 스크립트(예: Python 스크립트)라면, Cloudflare Pages는 직접 실행할 수 없습니다. 이 경우, Cloudflare Workers를 사용하여 API 엔드포인트를 만들거나, 서버리스 함수(AWS Lambda, Google Cloud Functions) 또는 자체 서버에 배포해야 합니다.

---

### **3. Google Apps Script 연동을 통한 자동화 워크플로우 아이디어**

Google Apps Script (GAS)는 Google Workspace 서비스(Google Sheets, Docs, Calendar 등)를 확장하고 자동화할 수 있는 강력한 서버리스 플랫폼입니다. 이를 활용하여 WordPress 자동 글 작성 워크플로우를 더욱 효율적으로 만들 수 있습니다.

#### **3.1. 아이디어 1: Google Sheets 기반 콘텐츠 관리 및 예약 발행**

*   **워크플로우:**
    1.  **콘텐츠 작성:** Google Sheets에 글 제목, 내용, 카테고리, 태그, 발행일시 등을 정리합니다. 각 행이 하나의 WordPress 포스트가 됩니다. [근거: 추측]
    2.  **GAS 스크립트 개발:**
        *   GAS 스크립트가 Google Sheets의 데이터를 읽어옵니다.
        *   각 행의 데이터를 기반으로 WordPress REST API를 호출하여 글을 작성합니다.
        *   이미지 URL이 있다면, GAS에서 이미지를 다운로드하여 WordPress 미디어 라이브러리에 업로드하고, 반환된 미디어 ID를 글 내용에 삽입합니다.
        *   글 작성 후, Sheets에 발행 상태(성공/실패, 발행 URL)를 업데이트합니다.
    3.  **트리거 설정:** GAS의 시간 기반 트리거를 설정하여 특정 시간(예: 매일 자정, 매주 월요일 오전)에 스크립트를 자동으로 실행합니다. 이를 통해 예약 발행 기능을 구현할 수 있습니다.
*   **장점:**
    *   콘텐츠 관리의 용이성 (스프레드시트 친숙도).
    *   별도의 서버 없이 Google 인프라에서 실행.
    *   예약 발행 기능 구현 용이.
*   **보안:** WordPress API 인증 정보(Application Password)는 GAS의 `Script Properties`에 저장하여 코드에 직접 노출되지 않도록 합니다.

#### **3.2. 아이디어 2: Google Forms를 이용한 간편 포스팅 인터페이스**

*   **워크플로우:**
    1.  **폼 생성:** Google Forms를 사용하여 글 제목, 내용, 카테고리 선택 등을 입력받는 폼을 만듭니다.
    2.  **응답 시 GAS 실행:** Google Forms 응답이 제출될 때마다 GAS 스크립트가 자동으로 실행되도록 트리거를 설정합니다.
    3.  **WordPress 포스팅:** GAS 스크립트가 폼 응답 데이터를 받아 WordPress REST API를 호출하여 글을 작성합니다.
*   **장점:**
    *   간단한 인터페이스로 누구나 쉽게 글을 작성하고 발행할 수 있습니다.
    *   모바일에서도 접근 가능.

#### **3.3. 아이디어 3: Gmail 연동을 통한 이메일 기반 포스팅**

*   **워크플로우:**
    1.  **이메일 수신:** 특정 이메일 주소(예: `post@yourdomain.com`)로 이메일을 보내면, GAS 스크립트가 해당 이메일을 감지하고 내용을 파싱합니다.
    2.  **내용 파싱:** 이메일 제목을 글 제목으로, 본문을 글 내용으로 사용합니다. 첨부파일은 미디어로 업로드합니다.
    3.  **WordPress 포스팅:** 파싱된 데이터를 WordPress REST API로 전송하여 글을 작성합니다.
*   **장점:**
    *   이메일 클라이언트만 있으면 어디서든 글을 발행할 수 있습니다.

---

**결론:**

WordPress REST API를 활용한 자동 글 작성 프로그램은 Application Passwords를 통한 안전한 인증, `/wp/v2/posts` 및 `/wp/v2/media` 엔드포인트를 활용한 포스팅 및 미디어 업로드가 핵심입니다. Cloudflare Pages는 이 프로그램의 웹 인터페이스를 배포하는 데 적합하며, 백엔드 로직은 Cloudflare Workers나 GAS를 활용할 수 있습니다. 특히 Google Apps Script는 Google Sheets 연동을 통해 콘텐츠 관리 및 예약 발행 자동화를 강력하게 지원할 수 있습니다.

이 계획을 바탕으로 개발을 진행하며, 각 단계에서 발생할 수 있는 문제점들을 철저히 검토하고 최적의 솔루션을 찾아나가겠습니다. ⚙️💻

📊 평가: 진행중 — WordPress REST API, Cloudflare Pages, Google Apps Script 연동에 대한 개발 계획 및 아이디어를 구체적으로 제시했습니다.
📝 다음 단계: 제시된 계획을 바탕으로 개발 환경을 설정하고, 각 핵심 기능별 프로토타입 구현을 시작합니다.
자가검증: 사실 3개 / 추측 3개
