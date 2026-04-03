import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parent / ".env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = os.getenv("OPENAI_MODEL", "gpt-4o")

print("GPT 대화 시작 (종료: 'quit' 또는 'exit')")
print("역할 변경: '/role 역할설명' 입력")
print("-" * 40)

role = None
history = []

while True:
    user_input = input("\n나: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ("quit", "exit"):
        print("종료합니다.")
        break
    if user_input.startswith("/role "):
        role = user_input[6:].strip()
        print(f"[역할 변경됨: {role}]")
        history.clear()
        continue

    history.append({"role": "user", "content": user_input})

    payload = {"model": model, "messages": history}
    if role:
        payload["messages"] = [{"role": "system", "content": role}] + history

    response = client.chat.completions.create(**payload)
    reply = response.choices[0].message.content.strip()

    history.append({"role": "assistant", "content": reply})
    print(f"\nGPT: {reply}")
