import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def select_repository_with_ai(title, body):
    prompt = f"""
You are an assistant that decides which repository should handle a task.

Available repositories:
- web-api
- ms-user
- ms-order

Issue:
Title: {title}
Body: {body}

Rules:
- If it's about users → ms-user
- If it's about orders → ms-order
- If it's about gateway/orchestration → web-api

Answer ONLY with one of:
web-api, ms-user, ms-order
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip().lower()
    return result