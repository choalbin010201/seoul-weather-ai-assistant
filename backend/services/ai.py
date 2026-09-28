from google import genai
from google.genai import types

from ..config import GEMINI_API_KEY, GEMINI_MODEL
from .summary import build_summary


def answer_question(question: str, rows: list[dict]) -> str:
    """
    Firestore에서 가져온 시계열 데이터(rows)를 요약한 뒤,
    그 요약 정보를 Gemini에게 전달하여 답변을 생성한다.
    """

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY가 설정되지 않았습니다."
        )

    # Firestore 원본 데이터 -> 시계열 요약
    summary = build_summary(rows)

    system_prompt = f"""
당신은 사용자의 서울 일평균 기온 데이터를 이해하고 설명하는
AI 데이터 분석 비서입니다.

아래 정보는 사용자가 Firestore에 저장한 실제 시계열 데이터를
분석하여 계산한 요약 정보입니다.

[저장된 데이터 요약]

데이터 기간:
{summary["period"]}

전체 데이터 개수:
{summary["count"]}개

평균 기온:
{summary["metrics"]["average"]}°C

최고 기온:
{summary["metrics"]["max"]}°C
날짜: {summary["metrics"]["max_date"]}

최저 기온:
{summary["metrics"]["min"]}°C
날짜: {summary["metrics"]["min_date"]}

표준편차:
{summary["metrics"]["std"]}°C

최근 추세:
{summary["trend"]}

가장 최근 데이터:
날짜: {summary["latest"]["date"]}
기온: {summary["latest"]["value"]}°C

[답변 규칙]

1. 사용자의 데이터에 관한 질문에는 위 요약 정보를 우선 근거로 사용하세요.
2. 가능한 경우 구체적인 날짜와 수치를 포함하세요.
3. 위 요약 정보만으로 알 수 없는 내용은 임의로 만들어내지 마세요.
4. 확인할 수 없는 정보는 저장된 데이터 요약만으로 확인할 수 없다고 설명하세요.
5. 자연스러운 한국어로 답변하세요.
6. 답변은 간결하고 이해하기 쉽게 작성하세요.
""".strip()

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=500,
            temperature=0.3,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini에서 응답을 생성하지 못했습니다."
        )

    return response.text.strip()