# 서울 날씨 AI 비서

서울의 일평균 기온 시계열 데이터를 Firestore에 저장하고, 사용자가 자연어로 데이터에 대해 질문할 수 있도록 구현한 AI 데이터 분석 비서입니다.

FastAPI 기반 백엔드에서 시계열 데이터를 관리하고 분석하며, Gemini API를 활용하여 저장된 실제 데이터를 기반으로 사용자 질문에 답변합니다.

## 1. 프로젝트 개요

본 프로젝트의 목표는 사용자의 시계열 데이터를 저장하고 분석한 뒤, AI가 해당 데이터를 이해하여 자연어 질문에 답변할 수 있는 서비스를 구현하는 것입니다.

서울의 일평균 기온 데이터를 활용하였으며 다음과 같은 흐름으로 동작합니다.

```text
서울 기온 데이터
      ↓
Firebase Firestore 저장
      ↓
FastAPI 데이터 조회 및 분석
      ↓
데이터 요약 + 날짜별 데이터
      ↓
Gemini API
      ↓
자연어 데이터 질의응답
```

프론트엔드에서는 데이터 요약, AI 채팅, 데이터 관리, 대화 기록 기능을 사용할 수 있습니다.

---

## 2. 주요 기능

### 2.1 시계열 데이터 분석

Firestore에 저장된 서울 일평균 기온 데이터를 분석하여 다음 정보를 제공합니다.

- 데이터 기간
- 전체 데이터 개수
- 전체 평균 기온
- 최고 기온
- 최저 기온
- 표준편차
- 최근 데이터
- 최근 기온 추세

현재 저장된 데이터의 기본 정보는 다음과 같습니다.

| 항목 | 값 |
|---|---|
| 데이터 기간 | 2022-01-01 ~ 2024-01-01 |
| 데이터 개수 | 731개 |
| 전체 평균 기온 | 13.69°C |
| 최고 기온 | 31.1°C |
| 최저 기온 | -13.7°C |
| 표준편차 | 10.72°C |

최근 추세는 최근 7일 평균과 이전 7일 평균을 비교하여 상승, 하락 또는 유지 상태로 계산합니다.

### 2.2 AI 데이터 질의

사용자는 저장된 기온 데이터에 대해 자연어로 질문할 수 있습니다.

예시:

```text
2023년 6월 13일 평균기온 알려줘
2023년 6월 평균기온 알려줘
2023년 1월 중 가장 추운 날은 언제야?
2022년과 2023년 평균기온을 비교해줘
2023년 여름 평균기온을 알려줘
최근 기온 추세를 설명해줘
```

FastAPI 서버가 Firestore에서 데이터를 불러온 뒤 전체 데이터 요약과 날짜별 실제 데이터를 Gemini에 전달합니다.

AI는 제공된 실제 데이터를 근거로 답변하며, 저장된 데이터에서 확인할 수 없는 값은 임의로 생성하지 않도록 구성했습니다.

### 2.3 데이터 CRUD

사용자는 웹 화면에서 기온 데이터를 직접 관리할 수 있습니다.

지원 기능:

- 데이터 추가
- 데이터 조회
- 데이터 수정
- 데이터 삭제

각 데이터는 기본적으로 다음 정보를 포함합니다.

```text
날짜 (date)
기온 (value)
메모 (memo)
```

데이터를 추가, 수정 또는 삭제하면 데이터 목록과 데이터 요약 정보가 다시 갱신됩니다.

### 2.4 대화 기록

AI와의 대화 내용은 Firestore에 저장됩니다.

지원 기능:

- AI 대화 자동 저장
- 저장된 대화 목록 조회
- 이전 대화 불러오기
- 대화 이어서 진행
- 저장된 대화 삭제

---

## 3. 사용 데이터

서울 날씨 시계열 데이터를 사용했습니다.

- 기간: 2022-01-01 ~ 2024-01-01
- 데이터 개수: 731개
- 주요 분석 값: 일평균 기온
- 데이터베이스: Firebase Firestore

원본 데이터에서 날짜와 일평균 기온을 중심으로 서비스에 필요한 형태로 저장하여 사용했습니다.

---

## 4. 기술 스택

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- Firebase Admin SDK
- Google Gemini API
- python-dotenv

### Database

- Firebase Firestore

### Frontend

- HTML
- CSS
- Vanilla JavaScript

### Deployment

- Backend: Render
- Frontend: Vercel

### AI

- Google Gemini API
- `google-genai`

---

## 5. 프로젝트 구조

```text
seoul-weather-ai-assistant/
├── backend/
│   ├── routers/
│   │   ├── data.py
│   │   ├── conversations.py
│   │   └── chat.py
│   ├── services/
│   │   ├── summary.py
│   │   └── ai.py
│   ├── main.py
│   ├── firebase.py
│   ├── config.py
│   ├── schemas.py
│   ├── seed_data.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   ├── config.js
│   └── build.sh
│
├── data/
│   └── seoul_weather_data.csv
│
├── requirements.txt
├── vercel.json
├── .gitignore
└── README.md
```

---

## 6. 시스템 구조

서비스는 다음과 같은 구조로 구성되어 있습니다.

```text
사용자
  ↓
Vercel Frontend
(HTML / CSS / JavaScript)
  ↓
FastAPI REST API
(Render)
  ↓
Firebase Firestore
  ↓
데이터 조회 및 분석
  ↓
Gemini API
  ↓
데이터 기반 자연어 답변
```

프론트엔드와 백엔드를 분리하여 구현하였으며 CORS 설정을 통해 Vercel에 배포된 프론트엔드에서 Render의 FastAPI 서버에 접근할 수 있도록 구성했습니다.

---

## 7. API

FastAPI를 사용하여 REST API를 구현했습니다.

### Data API

| Method | Endpoint | 기능 |
|---|---|---|
| GET | `/api/data` | 전체 데이터 조회 |
| POST | `/api/data` | 데이터 추가 |
| PUT | `/api/data/{id}` | 데이터 수정 |
| DELETE | `/api/data/{id}` | 데이터 삭제 |
| GET | `/api/data/summary` | 시계열 데이터 요약 |

### Chat API

| Method | Endpoint | 기능 |
|---|---|---|
| POST | `/api/chat` | 데이터 기반 AI 질문 |

### Conversation API

| Method | Endpoint | 기능 |
|---|---|---|
| GET | `/api/conversations` | 대화 목록 조회 |
| GET | `/api/conversations/{id}` | 특정 대화 조회 |
| POST | `/api/conversations` | 대화 저장 |
| DELETE | `/api/conversations/{id}` | 대화 삭제 |

FastAPI Swagger UI에서도 각 API를 확인하고 테스트할 수 있습니다.

---

## 8. 로컬 실행 방법

### 8.1 저장소 복제

```bash
git clone https://github.com/choalbin010201/seoul-weather-ai-assistant.git
cd seoul-weather-ai-assistant
```

### 8.2 Python 가상환경 생성

```bash
python -m venv .venv
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 8.3 패키지 설치

```bash
pip install -r requirements.txt
```

### 8.4 환경변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 필요한 환경변수를 설정합니다.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=YOUR_GEMINI_MODEL

FIREBASE_SERVICE_ACCOUNT_JSON=YOUR_FIREBASE_SERVICE_ACCOUNT_JSON

ALLOWED_ORIGINS=http://localhost:5500
```

실제 API Key와 Firebase Service Account 정보는 GitHub에 업로드하지 않습니다.

### 8.5 FastAPI 실행

프로젝트 루트에서 다음 명령을 실행합니다.

```bash
python -m uvicorn backend.main:app --reload
```

실행 후:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### 8.6 Frontend 실행

새 터미널에서:

```bash
cd frontend
python3 -m http.server 5500
```

브라우저에서 다음 주소로 접속합니다.

```text
http://localhost:5500
```

---

## 9. 환경변수

| 변수 | 설명 |
|---|---|
| `GEMINI_API_KEY` | Gemini API 인증 키 |
| `GEMINI_MODEL` | 사용할 Gemini 모델 |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | Firebase Admin SDK 인증 정보 |
| `ALLOWED_ORIGINS` | FastAPI CORS 허용 Origin |
| `API_BASE_URL` | 프론트엔드에서 사용할 백엔드 API 주소 |

보안을 위해 실제 API Key와 Firebase 인증 정보는 Git 저장소에 포함하지 않습니다.

---

## 10. 배포

### Frontend

Vercel

https://seoul-weather-ai-assistant-frontend.vercel.app

### Backend

Render

https://seoul-weather-ai-assistant.onrender.com

### Swagger API Documentation

https://seoul-weather-ai-assistant.onrender.com/docs

### GitHub Repository

https://github.com/choalbin010201/seoul-weather-ai-assistant

Render 무료 인스턴스 특성상 일정 시간 요청이 없으면 서버가 일시 중지될 수 있으며, 첫 요청 시 응답까지 시간이 걸릴 수 있습니다.

---

## 11. 구현 흐름

### 데이터 분석

Firestore에서 데이터를 불러와 날짜순으로 정렬하고 평균, 최고, 최저, 표준편차 및 최근 추세 등의 요약 정보를 계산합니다.

### AI 질의

사용자의 질문과 함께 저장된 데이터의 요약 정보 및 날짜별 데이터를 Gemini API에 전달합니다.

Gemini는 제공된 데이터를 기반으로 특정 날짜, 월, 연도 또는 기간에 대한 질문에 답변합니다.

### 데이터 관리

FastAPI의 REST API와 Firestore CRUD 기능을 연결하여 웹에서 데이터를 추가, 조회, 수정 및 삭제할 수 있도록 구현했습니다.

### 대화 관리

AI 질문과 답변을 Firestore의 대화 데이터로 저장하여 이전 대화를 다시 불러오거나 삭제할 수 있도록 구현했습니다.

---

## 12. 주요 구현 결과

본 프로젝트를 통해 다음과 같은 전체 데이터 서비스 흐름을 구현했습니다.

```text
시계열 데이터
→ Firestore 저장
→ FastAPI 조회
→ 데이터 분석 및 요약
→ Gemini 데이터 컨텍스트 제공
→ 자연어 질의응답
→ 대화 기록 저장
```

단순히 AI에게 일반적인 질문을 전달하는 방식이 아니라, 사용자가 저장한 실제 시계열 데이터를 AI의 컨텍스트로 제공하여 데이터에 기반한 답변을 생성하도록 구현한 것이 핵심입니다.
