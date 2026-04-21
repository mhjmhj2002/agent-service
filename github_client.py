import os
import requests

BASE_URL = "https://api.github.com"


# =========================
# 🔐 HELPERS COM DEBUG
# =========================

def get_headers():
    token = os.getenv("GITHUB_TOKEN")
    owner = os.getenv("GITHUB_OWNER")

    # 🔥 DEBUG REAL (onde o problema está)
    print("\n[DEBUG GITHUB CLIENT]")
    print("TOKEN EXISTS:", bool(token))
    print("TOKEN PREVIEW:", (token[:6] + "...") if token else None)
    print("OWNER:", owner)

    if not token:
        raise Exception("GITHUB_TOKEN não encontrado no ambiente")

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }


def get_owner():
    owner = os.getenv("GITHUB_OWNER")

    if not owner:
        raise Exception("GITHUB_OWNER não encontrado no ambiente")

    return owner


# =========================
# 🔍 ISSUES
# =========================

def get_issue_by_number(issue_number, repo):
    url = f"{BASE_URL}/repos/{get_owner()}/{repo}/issues/{issue_number}"

    print(f"\n[REQUEST] GET {url}")

    response = requests.get(url, headers=get_headers())

    print("[RESPONSE STATUS]", response.status_code)

    response.raise_for_status()
    return response.json()


def get_all_issues(repo):
    url = f"{BASE_URL}/repos/{get_owner()}/{repo}/issues"

    print(f"\n[REQUEST] GET {url}")

    response = requests.get(url, headers=get_headers())

    print("[RESPONSE STATUS]", response.status_code)

    response.raise_for_status()
    return response.json()


# =========================
# 💬 COMMENTS
# =========================

def comment_on_issue(issue_number, repo, comment):
    url = f"{BASE_URL}/repos/{get_owner()}/{repo}/issues/{issue_number}/comments"

    print(f"\n[COMMENT] {url}")
    print("[BODY]", comment)

    response = requests.post(
        url,
        headers=get_headers(),
        json={"body": comment}
    )

    print("[RESPONSE STATUS]", response.status_code)

    response.raise_for_status()
    return response.json()


# =========================
# 🏷 LABELS
# =========================

def add_label(issue_number, repo, label):
    url = f"{BASE_URL}/repos/{get_owner()}/{repo}/issues/{issue_number}/labels"

    print(f"\n[LABEL] {label}")
    print("[REQUEST]", url)

    response = requests.post(
        url,
        headers=get_headers(),
        json={"labels": [label]}
    )

    print("[RESPONSE STATUS]", response.status_code)

    response.raise_for_status()
    return response.json()


# =========================
# ✏️ UPDATE BODY
# =========================

def update_issue_body(issue_number, repo, new_body):
    url = f"{BASE_URL}/repos/{get_owner()}/{repo}/issues/{issue_number}"

    print(f"\n[UPDATE ISSUE BODY] {url}")

    response = requests.patch(
        url,
        headers=get_headers(),
        json={"body": new_body}
    )

    print("[RESPONSE STATUS]", response.status_code)

    response.raise_for_status()
    return response.json()
    
def get_issue_labels(issue_number, repo):
    issue = get_issue_by_number(issue_number, repo)
    return [l["name"] for l in issue.get("labels", [])]    