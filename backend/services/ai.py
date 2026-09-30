from google import genai
from google.genai import types

from ..config import GEMINI_API_KEY, GEMINI_MODEL
from .summary import build_summary


def answer_question(question: str, rows: list[dict]) -> str:
    """
    Firestore에서 가져온 서울 일평균 기온 데이터를
    전체 요약 + 날짜별 원본 데이터 형태로 Gemini에게 전달한다.

    이를 통해 특정 날짜, 월별/연도별 평균, 기간 비교,
    최고/최저 기온 등의 질문에 답할 수 있다.
    """

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY가 설정되지 않았습니다."
        )

    if not rows:
        raise RuntimeError(
            "분석할 기온 데이터가 없습니다."
        )

    # 날짜순 정렬
    sorted_rows = sorted(
        rows,
        key=lambda row: row["date"]
    )

    # 전체 데이터 요약
    summary = build_summary(sorted_rows)

    # Gemini에게 전달할 날짜별 원본 데이터 생성
    #
    # 예:
    # 2022-01-01: -4.3°C
    # 2022-01-02: -1.3°C
    # ...
    data_lines = []

    for row in sorted_rows:
        date = row.get("date")
        value = row.get("value")
        memo = row.get("memo", "")

        line = f"{date}: {value}°C"

        if memo:
            line += f" / 메모: {memo}"

        data_lines.append(line)

    raw_data_text = "\n".join(data_lines)

    system_prompt = f"""
당신은 사용자가 Firestore에 저장한 서울 일평균 기온 데이터를
분석하고 설명하는 AI 데이터 분석 비서입니다.

반드시 아래에 제공된 실제 저장 데이터를 근거로 답변하세요.

==================================================
[전체 데이터 요약]
==================================================

데이터 기간:
{summary["period"]}

전체 데이터 개수:
{summary["count"]}개

전체 평균 기온:
{summary["metrics"]["average"]}°C

전체 최고 기온:
{summary["metrics"]["max"]}°C
날짜:
{summary["metrics"]["max_date"]}

전체 최저 기온:
{summary["metrics"]["min"]}°C
날짜:
{summary["metrics"]["min_date"]}

표준편차:
{summary["metrics"]["std"]}°C

최근 추세:
{summary["trend"]}

가장 최근 데이터:
날짜: {summary["latest"]["date"]}
기온: {summary["latest"]["value"]}°C


==================================================
[날짜별 실제 저장 데이터]
==================================================

{raw_data_text}


==================================================
[데이터 해석 규칙]
==================================================

1. 위 데이터의 각 값은 해당 날짜의 서울 일평균 기온이다.

2. 특정 날짜를 질문하면 반드시 날짜별 실제 저장 데이터에서
   해당 날짜를 찾아 답변한다.

3. 특정 월의 평균기온을 질문하면 해당 월에 포함되는
   실제 데이터들의 산술평균을 계산한다.

4. 특정 연도의 평균기온을 질문하면 해당 연도의
   실제 데이터들의 산술평균을 계산한다.

5. 특정 기간의 최고 또는 최저 기온을 질문하면
   그 기간에 포함되는 데이터만 비교한다.

6. 두 기간을 비교해달라는 질문에는 각각의 값을
   실제 데이터로 계산한 후 비교한다.

7. '여름'은 6월, 7월, 8월로 해석한다.
   '겨울'은 12월, 1월, 2월로 해석한다.
   '봄'은 3월, 4월, 5월로 해석한다.
   '가을'은 9월, 10월, 11월로 해석한다.

8. 데이터에 존재하지 않는 날짜나 기간에 대해서는
   값을 임의로 만들어내지 않는다.

9. 계산 결과가 필요한 경우 제공된 실제 데이터만 사용한다.

10. 데이터에 없는 정보를 일반적인 날씨 지식이나
    추측으로 채우지 않는다.

11. 질문에 필요한 데이터가 없으면
    "저장된 데이터에서 확인할 수 없습니다."라고 설명한다.

12. 가능한 경우 계산 결과와 함께 사용한 기간을 명확하게 표시한다.

13. 자연스러운 한국어로 답변한다.

14. 답변은 간결하고 이해하기 쉽게 작성한다.
""".strip()

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=700,
            temperature=0.1,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini에서 응답을 생성하지 못했습니다."
        )

    return response.text.strip()