import os
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

env_path = ".env"
load_dotenv(env_path)

api_key = os.getenv("OPENAI_API_KEY", "").strip()
client = OpenAI(api_key=api_key)



class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    text_format=CalendarEvent,
)

output = response.output_parsed

# print(output.name)
# print(output.date)
# print(output.participants)


response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "system", "content": "맛집을 유저의 우선순위에 맞춰서 정렬해주되, 양식 종류는 무조건 포함해야해. 출력은 전문가적인 분석 스타일의 형태로 해줘"},
        {
            "role": "user",
            "content": "전주 지역의 맛집을 검색해서 찾아줘. 나는 중식 종류를 좀 더 선호하고, 한식도 좋아하긴 해",
        },
    ],)

print(response.output_text)