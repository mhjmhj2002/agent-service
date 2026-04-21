import os
import json
from openai import OpenAI
from engine.prompt_loader import load_prompt
from engine.schema_validator import validate_plan
from engine.plan_normalizer import normalize_plan


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise Exception("❌ OPENAI_API_KEY não encontrada")

    return OpenAI(api_key=api_key)


def generate_plan(title, body):
    client = get_client()

    system_prompt = load_prompt("planning/system.txt")
    user_template = load_prompt("planning/user.txt")

    user_prompt = user_template.format(
        title=title,
        body=body
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    content = response.choices[0].message.content

    # 🔥 1. parse JSON
    try:
        plan_dict = json.loads(content)
    except json.JSONDecodeError:
        raise Exception(f"❌ IA retornou JSON inválido:\n{content}")

    # 🔥 2. normaliza (não quebra pipeline)
    plan_dict = normalize_plan(plan_dict)

    # 🔥 3. valida schema
    try:
        validate_plan(plan_dict)
    except Exception as e:
        raise Exception(f"❌ Plano inválido após normalização:\n{plan_dict}\nErro: {str(e)}")

    return plan_dict