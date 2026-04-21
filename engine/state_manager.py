import json
import os

STATE_FILE = "state/agent_state.json"


def _load_state():
    if not os.path.exists(STATE_FILE):
        return {}

    with open(STATE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_state(repo, issue_number):
    state = _load_state()

    repo_state = state.get(repo, {})
    issue_state = repo_state.get(str(issue_number))

    if not issue_state:
        return {
            "repo": repo,
            "issue_number": issue_number,
            "status": "NEW",
            "steps": {
                "label_applied": False,
                "comment_added": False,
                "plan_generated": False
            }
        }

    return issue_state


def update_state(repo, issue_number, status=None, steps=None):
    state = _load_state()

    if repo not in state:
        state[repo] = {}

    if str(issue_number) not in state[repo]:
        state[repo][str(issue_number)] = get_state(repo, issue_number)

    issue_state = state[repo][str(issue_number)]

    if status:
        issue_state["status"] = status

    if steps:
        issue_state["steps"].update(steps)

    state[repo][str(issue_number)] = issue_state

    _save_state(state)

    return issue_state