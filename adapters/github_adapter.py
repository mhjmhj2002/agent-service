from github_client import (
    get_issue_by_number,
    comment_on_issue,
    add_label,
    get_issue_labels,
    update_issue_body
)


# =========================
# 💬 COMMENTS (AGENT RULES)
# =========================

def agent_already_commented(issue_number, repo):
    issue = get_issue_by_number(issue_number, repo)

    comments = issue.get("comments", 0)
    return comments > 0


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