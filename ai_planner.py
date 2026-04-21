import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_plan(title, body):
    prompt = f"""
You are a senior backend engineer.

Given this GitHub issue, break it into a step-by-step implementation plan.

Issue:
Title: {title}
Body: {body}

Context:
- Java Spring Boot project
- Layers: controller, service, dto
- Keep steps technical and objective

Output format:
- Step 1: ...
- Step 2: ...
- Step 3: ...
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content