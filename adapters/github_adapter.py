from github_client import (
    get_issue_by_number,
    comment_on_issue,
    add_label,
    get_issue_labels,
    update_issue_body
)

import requests
import os


# =========================
# 💬 COMMENTS (AGENT RULES)
# =========================

def agent_already_commented(issue_number, repo):
    issue = get_issue_by_number(issue_number, repo)

    comments = issue.get("comments", 0)
    return comments > 0

def get_issue_comments(issue_number, repo):
    """
    Aceita repo como string ou dict
    """

    if isinstance(repo, str):
        owner = os.getenv("GITHUB_OWNER")
        name = repo
    else:
        owner = repo["owner"]
        name = repo["name"]

    token = os.getenv("GITHUB_TOKEN")

    url = f"https://api.github.com/repos/{owner}/{name}/issues/{issue_number}/comments"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    print(f"[REQUEST] GET {url}")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Erro ao buscar comentários: {response.status_code}")
        print(response.text)
        return []

    comments = response.json()

    print(f"[COMMENTS LOADED] {len(comments)} comentários encontrados")

    return comments

# =========================
# 🏷 LABEL RULES
# =========================

def has_label(issue_number, repo, label):
    labels = get_issue_labels(issue_number, repo)
    return label in labels


# =========================
# 🧠 STATE PERSISTENCE
# =========================

STATE_MARKER = "### 🤖 Agent State"


def extract_state(body):
    if not body or STATE_MARKER not in body:
        return {
            "status": "NEW",
            "steps": {
                "label_applied": False,
                "comment_added": False,
                "plan_generated": False
            }
        }

    return {
        "status": "UNKNOWN",
        "steps": {
            "label_applied": "label_applied: true" in body,
            "comment_added": "comment_added: true" in body,
            "plan_generated": "plan_generated: true" in body
        }
    }


def build_state_block(state):
    return f"""
{STATE_MARKER}
status: {state['status']}

steps:
- label_applied: {str(state['steps']['label_applied']).lower()}
- comment_added: {str(state['steps']['comment_added']).lower()}
- plan_generated: {str(state['steps']['plan_generated']).lower()}
""".strip()


def save_state(issue, state):
    body = issue.get("body", "")
    new_body = body + "\n\n" + build_state_block(state)

    update_issue_body(issue["number"], issue["repo"], new_body)


# =========================
# 💬 ACTION HELPERS (AGENTE)
# =========================

def send_comment(issue_number, repo, text):
    return comment_on_issue(issue_number, repo, text)


def apply_label(issue_number, repo, label):
    return add_label(issue_number, repo, label)