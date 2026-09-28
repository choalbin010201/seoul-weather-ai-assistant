# 서울 날씨 데이터 기반 AI 비서

서울 일평균 기온 시계열 데이터를 Firestore에 저장하고, 요약 정보를 GPT 시스템 컨텍스트에 주입하여 맞춤형 답변을 제공하는 과제 제출용 웹 서비스입니다.

## 데이터
- 기간: **2022-01-01 ~ 2024-01-01**
- 데이터 포인트: **731개**
- `value`: 서울 일평균 기온(°C)
- 파일: `data/seoul_weather_data.csv`

## 구조
```text
backend/  FastAPI, Firestore, OpenAI
frontend/ HTML, CSS, JavaScript
data/     제출용 시계열 CSV
screenshots/ 제출 스크린샷
README.md
requirements.txt
vercel.json
```

## 로컬 실행 1: 환경 만들기
프로젝트 루트에서 실행합니다.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp backend/.env.example .env
```
`.env`에 실제 값을 넣습니다. 서비스 계정 JSON 파일 자체는 GitHub에 올리지 않습니다.
```text
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.6-luna
FIREBASE_SERVICE_ACCOUNT_JSON={...서비스 계정 JSON 전체...}
ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
```

## 로컬 실행 2: Firestore 초기 데이터 넣기
Firebase에서 Firestore Database를 만든 후:
```bash
python -m backend.seed_data
```
731개 데이터를 `data` 컬렉션에 저장합니다. 날짜를 문서 ID로 사용해 재실행 시 같은 날짜가 중복되지 않습니다.

## 로컬 실행 3: 백엔드
```bash
uvicorn backend.main:app --reload
```
- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

## 로컬 실행 4: 프론트
새 터미널에서:
```bash
cd frontend
python3 -m http.server 5500
```
브라우저에서 `http://localhost:5500` 접속.

## 필수 API
| 기능 | Method | Endpoint |
|---|---|---|
| 데이터 추가 | POST | `/api/data` |
| 데이터 조회 | GET | `/api/data` |
| 데이터 수정 | PUT | `/api/data/{id}` |
| 데이터 삭제 | DELETE | `/api/data/{id}` |
| 데이터 요약 | GET | `/api/data/summary` |
| 대화 저장 | POST | `/api/conversations` |
| 대화 목록 | GET | `/api/conversations` |
| 대화 불러오기 | GET | `/api/conversations/{id}` |
| 대화 삭제 | DELETE | `/api/conversations/{id}` |
| AI 채팅 | POST | `/api/chat` |

## 컨텍스트 주입
```text
질문 → Firestore data 조회 → 기간/개수/평균/최대/최소/표준편차/최근 추세 계산
→ 시스템 프롬프트 주입 → OpenAI Responses API → 답변 → conversations 자동 저장
```

## Render 배포
GitHub 저장소를 Render Web Service에 연결합니다.
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- 환경변수: `OPENAI_API_KEY`, `OPENAI_MODEL`, `FIREBASE_SERVICE_ACCOUNT_JSON`, `ALLOWED_ORIGINS`
Vercel 배포 후 `ALLOWED_ORIGINS=https://YOUR-PROJECT.vercel.app`로 설정합니다.

## Vercel 배포
GitHub 저장소를 연결하고 환경변수 `API_BASE_URL=https://YOUR-RENDER-SERVICE.onrender.com`을 설정합니다. `vercel.json`과 `frontend/build.sh`가 빌드 시 이 값을 `config.js`에 주입합니다.

## 배포 URL (배포 후 수정)
- Frontend: `https://...`
- Backend API: `https://...`
- Swagger: `https://.../docs`

## 제출 스크린샷
1. 데이터 요약 + 질문/답변이 보이는 채팅 화면
2. 데이터 추가 또는 삭제가 보이는 데이터 관리 화면
3. 이전 대화를 불러온 대화 기록 화면

## 제출 전 체크
- [ ] Firestore 연결 및 731개 seed
- [ ] Swagger에서 CRUD/summary 확인
- [ ] GPT 답변 확인
- [ ] 대화 자동 저장/불러오기 확인
- [ ] Render `/docs` 확인
- [ ] Vercel 확인
- [ ] 실제 배포 URL과 스크린샷 README에 추가
- [ ] `.env`와 Firebase 키가 GitHub에 없는지 확인
