# 💻 코다리 — '블로그 자동 포스팅' 기능을 위한 프론트엔드 아키텍처를 설계하고, 사용자가 최소한의 데이터 입력으로 포스팅을 자동화할 수 있도록 UI 컴포넌트 구성을 제안하세요. 기존 modutools.com의 디자인 표준 종속성을 제거하고, 독립적인 개발 및 배포가 가능한 구조를 고려해야 합니다. [근거: 사용자 명령]

💻 코다리: CEO님의 지시 잘 받았습니다. 기존 `modutools.com`의 디자인 표준에서 벗어나 '블로그 자동 포스팅' 기능에 특화된 프론트엔드 아키텍처를 설계하고, 최소한의 데이터 입력으로 포스팅을 자동화할 수 있는 UI 컴포넌트 구성을 제안하겠습니다. 독립적인 개발 및 배포가 가능한 구조를 최우선으로 고려하겠습니다. [근거: 사용자 명령]

먼저, 독립적인 개발 및 배포를 위해 프레임워크 선택이 중요합니다. React, Vue, Svelte 중 하나를 선택하여 컴포넌트 기반 개발을 진행할 수 있습니다. 여기서는 React를 기반으로 아키텍처를 제안하겠습니다. [추측]

---

### 블로그 자동 포스팅 프론트엔드 아키텍처 설계 및 UI 컴포넌트 구성 제안

**1. 아키텍처 개요**

*   **프레임워크:** React (또는 Next.js for SSR/SSG) [추측]
    *   **선택 이유:** 컴포넌트 기반 개발, 광범위한 생태계, 뛰어난 개발자 경험. Next.js를 선택할 경우 SEO 최적화 및 초기 로딩 성능 향상에 유리합니다. [추측]
*   **상태 관리:** React Context API 또는 Recoil (필요시 Redux Toolkit) [추측]
    *   **선택 이유:** 소규모 프로젝트에는 Context API로 충분하며, 복잡도가 증가하면 Recoil과 같은 경량 상태 관리 라이브러리를 고려합니다. [추측]
*   **스타일링:** Tailwind CSS 또는 Styled-components [추측]
    *   **선택 이유:** Tailwind CSS는 유틸리티 기반으로 빠른 개발이 가능하며, Styled-components는 컴포넌트 레벨 스타일링으로 충돌을 최소화합니다. 독립적인 개발을 위해 기존 `modutools.com`의 CSS 프레임워크와는 별도로 구성합니다. [근거: 사용자 명령]
*   **API 통신:** Axios 또는 Fetch API [추측]
    *   **선택 이유:** 표준 Fetch API를 기본으로 사용하고, 인터셉터 등 추가 기능이 필요하면 Axios를 고려합니다. [추측]
*   **배포:** Cloudflare Pages [근거: 지난 의사결정 로그]
    *   **선택 이유:** 빠르고 안정적인 배포, CDN 기본 제공, 서버리스 함수 연동 용이. [추측]

**2. UI 컴포넌트 구성 (컨셉 1: Step-by-Step 가이드 기반)**

Designer 에이전트가 제안한 'Step-by-Step 가이드' 컨셉을 기반으로 UI 컴포넌트를 구성하겠습니다. 각 단계는 독립적인 컴포넌트로 분리되어 재사용성 및 유지보수성을 높입니다. [근거: 동료 에이전트 산출물]

```typescript
// src/App.tsx
import React, { useState } from 'react';
import StepProgressBar from './components/StepProgressBar';
import PostTitleStep from './components/PostTitleStep';
import PostContentStep from './components/PostContentStep';
import PostMediaStep from './components/PostMediaStep';
import PostSettingsStep from './components/PostSettingsStep';
import PostReviewStep from './components/PostReviewStep';
import PostSuccessStep from './components/PostSuccessStep';
import { PostData } from './types'; // 타입 정의 파일

const initialPostData: PostData = {
  title: '',
  content: '',
  media: [],
  categories: [],
  tags: [],
  publishDate: new Date(),
  status: 'publish',
};

function App() {
  const [currentStep, setCurrentStep] = useState(0);
  const [postData, setPostData] = useState<PostData>(initialPostData);

  const handleNext = (data: Partial<PostData>) => {
    setPostData(prev => ({ ...prev, ...data }));
    setCurrentStep(prev => prev + 1);
  };

  const handlePrev = () => {
    setCurrentStep(prev => prev - 1);
  };

  const steps = [
    { name: '제목 입력', component: <PostTitleStep onNext={handleNext} initialData={postData} /> },
    { name: '내용 작성', component: <PostContentStep onNext={handleNext} onPrev={handlePrev} initialData={postData} /> },
    { name: '미디어 추가', component: <PostMediaStep onNext={handleNext} onPrev={handlePrev} initialData={postData} /> },
    { name: '설정 및 태그', component: <PostSettingsStep onNext={handleNext} onPrev={handlePrev} initialData={postData} /> },
    { name: '최종 검토', component: <PostReviewStep onNext={handleNext} onPrev={handlePrev} initialData={postData} /> },
    { name: '포스팅 완료', component: <PostSuccessStep /> },
  ];

  return (
    <div className="container mx-auto p-4 flex">
      <div className="w-1/4 pr-4">
        <StepProgressBar currentStep={currentStep} steps={steps.map(s => s.name)} />
      </div>
      <div className="w-3/4 pl-4">
        {steps[currentStep].component}
      </div>
    </div>
  );
}

export default App;
```
[추측]

**주요 컴포넌트 목록:**

*   **`App.tsx`**: 애플리케이션의 최상위 컴포넌트. 상태 관리(현재 단계, 포스팅 데이터) 및 라우팅/단계 전환 로직을 담당합니다. [추측]
*   **`StepProgressBar.tsx`**: 현재 진행 단계를 시각적으로 표시하는 컴포넌트. `Designer` 에이전트의 제안에 따라 좌측에 배치됩니다. [근거: 동료 에이전트 산출물]
    *   **Props:** `currentStep: number`, `steps: string[]` [추측]
*   **`PostTitleStep.tsx`**: 포스팅 제목을 입력하는 컴포넌트.
    *   **데이터 입력:** 텍스트 필드 (제목) [추측]
    *   **Validation:** 제목 길이 제한, 필수 입력 등 [추측]
    *   **Props:** `onNext: (data: Partial<PostData>) => void`, `initialData: PostData` [추측]
*   **`PostContentStep.tsx`**: 포스팅 내용을 작성하는 컴포넌트.
    *   **데이터 입력:** 리치 텍스트 에디터 (WYSIWYG 또는 Markdown 에디터) [추측]
    *   **Props:** `onNext`, `onPrev`, `initialData` [추측]
*   **`PostMediaStep.tsx`**: 이미지, 동영상 등 미디어를 업로드하고 관리하는 컴포넌트.
    *   **데이터 입력:** 파일 업로드 컴포넌트, 미리보기, 삭제 기능 [추측]
    *   **Props:** `onNext`, `onPrev`, `initialData` [추측]
*   **`PostSettingsStep.tsx`**: 카테고리, 태그, 발행 상태, 발행일시 등을 설정하는 컴포넌트.
    *   **데이터 입력:** 드롭다운 (카테고리), 태그 입력 필드 (자동 완성), 라디오 버튼 (상태), 날짜/시간 선택기 (발행일시) [추측]
    *   **Props:** `onNext`, `onPrev`, `initialData` [추측]
*   **`PostReviewStep.tsx`**: 입력된 모든 내용을 최종적으로 검토하고 수정할 수 있는 컴포넌트.
    *   **데이터 표시:** 읽기 전용으로 모든 입력 데이터 표시 [추측]
    *   **액션:** '수정' 버튼 (해당 단계로 이동), '포스팅' 버튼 [추측]
    *   **Props:** `onNext`, `onPrev`, `initialData` [추측]
*   **`PostSuccessStep.tsx`**: 포스팅 완료 후 성공 메시지 및 다음 작업(예: 게시물 링크 복사, 새 포스팅 시작)을 제공하는 컴포넌트. [추측]

**3. 데이터 흐름 (Google Sheets 연동 고려)**

CEO의 지난 의사결정 로그에서 Google Apps Script 연동을 통한 자동화 워크플로우 아이디어가 제시되었으므로, 프론트엔드는 이와 연동될 수 있도록 설계합니다. [근거: 지난 의사결정 로그]

*   **초기 데이터 로딩:** Google Sheets에서 미리 작성된 포스팅 데이터를 불러와 초기 `postData` 상태를 채울 수 있습니다. [근거: 지난 의사결정 로그]
*   **포스팅 요청:** `PostReviewStep`에서 '포스팅' 버튼 클릭 시, 수집된 `postData`를 백엔드 API (Google Apps Script 또는 별도 서버리스 함수)로 전송하여 WordPress REST API 호출을 트리거합니다. [근거: 지난 의사결정 로그]

**4. 독립적인 개발 및 배포 구조**

*   **모노레포 (Optional):** 만약 향후 다른 독립적인 웹 도구가 추가될 경우, Turborepo나 Nx와 같은 모노레포를 사용하여 백엔드(Google Apps Script), 프론트엔드, 공통 유틸리티 라이브러리를 한 저장소에서 관리할 수 있습니다. [추측]
*   **환경 변수:** WordPress API URL, Application Password 등 민감 정보는 환경 변수를 통해 관리하여 코드에 하드코딩되지 않도록 합니다. Cloudflare Pages는 빌드 시 환경 변수 설정을 지원합니다. [추측]
*   **버전 관리:** Git을 사용하여 소스 코드를 관리하고, Semantic Versioning (예: v1.0.0)을 적용하여 버전 관리를 명확히 합니다. [추측]

이 아키텍처는 `modutools.com`의 기존 디자인 시스템에 종속되지 않고, 블로그 자동 포스팅 기능에 최적화된 독립적인 사용자 경험을 제공하며, Cloudflare Pages를 통한 효율적인 배포를 가능하게 합니다. [근거: 사용자 명령, 지난 의사결정 로그]

---
📊 평가: 진행중 — 프론트엔드 아키텍처 및 UI 컴포넌트 구성의 큰 그림을 제시했습니다.
📝 다음 단계: 각 컴포넌트의 상세 구현 및 스타일링, 백엔드 연동 방안을 구체화해야 합니다.
자가검증: 사실 3개 / 추측 14개
