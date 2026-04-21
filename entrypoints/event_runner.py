import os
from dotenv import load_dotenv

from github_client import get_issue_by_number
from engine.agent_engine import process_issue


# =========================
# 🚀 BOOTSTRAP DO SISTEMA
# =========================

# 🔥 força carregar .env mesmo se já existir variável no sistema
load_dotenv(override=True)


def validate_env():
    required = ["GITHUB_TOKEN", "GITHUB_OWNER"]

    missing = [v for v in required if not os.getenv(v)]

    if missing:
        raise Exception(f"❌ Missing environment variables: {missing}")

    # 🔎 debug controlado (não polui muito)
    token = os.getenv("GITHUB_TOKEN")
    owner = os.getenv("GITHUB_OWNER")

    print("\n[ENV CHECK]")
    print("OWNER:", owner)
    print("TOKEN OK:", bool(token))
    print("TOKEN PREVIEW:", token[:6] + "..." if token else None)


def run_event(issue_number, repo):
    print("\n================ EVENT =================")

    validate_env()

    print(f"\n[INPUT]")
    print(f"Repo: {repo}")
    print(f"Issue: {issue_number}")

    issue = get_issue_by_number(issue_number, repo)

    # 🔥 injeta repo no objeto
    issue["repo"] = repo

    print("\n[ISSUE LOADED]")
    print(f"Title: {issue.get('title')}")
    print(f"State: {issue.get('state')}")

    process_issue(issue)


# =========================
# 🧪 TESTE MANUAL
# =========================

if __name__ == "__main__":
    run_event(2, "agentic-ia-ms-user")