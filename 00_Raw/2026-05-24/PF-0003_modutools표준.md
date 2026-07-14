---
id: PF-2026-0003
title: "modutools.com 도구 개발 표준"
type: "UI/UX Standard"
category: "10_Wiki/💡 Topics/PublishFlow"
author: "PublishFlow AI"
tags: [modutools, cloudflare, design-system, css]
created: "2026-05-24"
---

# 🛠 modutools.com 도구 개발 표준

## 📌 한 줄 통찰 (Agent Directive)
> modutools에 새로운 웹 도구를 배포할 때는 반드시 규정된 공통 헤더/푸터 및 Pretendard 폰트 기반 둥근 카드 UI 디자인 시스템을 적용해야 한다.

## 🎨 UI/UX 디자인 시스템

### 1. 기본 스타일
- **폰트:** Pretendard, sans-serif
- **테마:** 라이트 테마 기반 (부드러운 흰색 배경 및 연회색 테두리)
- **카드 스타일:** `border-radius: 12px` / `box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1)` 적용

### 2. 레이아웃 컴포넌트
- **mt-header:** 상단 로고 및 네비게이션바 영역
- **mt-footer:** 하단 카피라이트, 사이트맵 및 AdSense 광고 하단 슬롯
- **tool- 접두사:** 모든 개별 도구의 CSS 클래스 및 고유 컴포넌트 파일명에는 `tool-` 접두사를 붙여 명칭 충돌 방지 (예: `.tool-calculator`, `tool-image-cropper.js`)

## 📂 카테고리 구성 (총 40개 도구)
- **계산기 (9개):** 이자 계산기, 대출 계산기, 퍼센트 계산기 등
- **이미지 (7개):** 이미지 크롭퍼, 리사이저, 포맷 변환기 등
- **텍스트 (5개):** 글자수 세기, 대소문자 변환기 등
- **변환기 (10개):** 단위 변환기, 진수 변환기 등
- **생성기 (4개):** 비밀번호 생성기, UUID 생성기 등
- **생활 (4개):** 디데이 계산기, 칼로리 계산기 등
- **운동 (1개):** BMI 계산기 등
