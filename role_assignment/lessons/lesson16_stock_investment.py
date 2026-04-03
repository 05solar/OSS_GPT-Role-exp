import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# 수업 포인트:
# - 동일한 질문("주식투자를 성공적으로 하는 방법")에 역할만 바꿔서
#   응답의 톤, 관점, 깊이가 얼마나 달라지는지 비교한다.
# - 역할: 없음 / 금융 전문가 / 회의적 경제학자 / 초등학생 선생님


def setup():
    """.env에서 API 키와 모델명을 읽고 클라이언트를 만든다."""
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(env_path)

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("OPENAI_API_KEY is not set in .env", file=sys.stderr)
        raise SystemExit(1)

    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    return OpenAI(api_key=api_key), model


def ask(client, model, prompt, role_text=None):
    """role_text가 있으면 instructions로 전달하고, 없으면 일반 호출한다."""
    payload = {"model": model, "input": prompt}
    if role_text:
        payload["instructions"] = role_text

    try:
        response = client.responses.create(**payload)
    except Exception as exc:
        print(f"API request failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    return (response.output_text or "").strip()


def main():
    client, model = setup()

    prompt = "주식투자를 성공적으로 하는 방법을 설명해줘."

    # 1) 역할 없음
    no_role = ask(client, model, prompt)

    # 2) 금융 전문가
    financial_analyst = ask(
        client,
        model,
        prompt,
        (
            "You are a seasoned financial analyst with 20 years of experience "
            "in equity markets. Provide practical, data-driven advice using "
            "professional terminology. Answer in Korean."
        ),
    )

    # 3) 회의적인 경제학자
    skeptical_economist = ask(
        client,
        model,
        prompt,
        (
            "You are a skeptical economist who questions conventional investment wisdom. "
            "Highlight risks, market inefficiencies, and behavioral biases that cause "
            "most retail investors to fail. Be critical and evidence-based. Answer in Korean."
        ),
    )

    # 4) 초등학생 선생님
    elementary_teacher = ask(
        client,
        model,
        prompt,
        (
            "You are a kind elementary school teacher explaining a complex topic "
            "to 10-year-old students. Use very simple words, fun analogies, and "
            "short sentences. Avoid jargon entirely. Answer in Korean."
        ),
    )

    print("\n" + "=" * 60)
    print("Lesson 16 - 주식투자 설명: 역할에 따른 응답 비교")
    print("=" * 60)

    print("\n--- [역할 없음] ---")
    print(no_role)

    print("\n--- [금융 전문가 (Financial Analyst)] ---")
    print(financial_analyst)

    print("\n--- [회의적인 경제학자 (Skeptical Economist)] ---")
    print(skeptical_economist)

    print("\n--- [초등학생 선생님 (Elementary Teacher)] ---")
    print(elementary_teacher)


if __name__ == "__main__":
    main()
