STATE_CACHE = {}


def get_state(repo, issue_number):
    key = f"{repo}:{issue_number}"

    if key not in STATE_CACHE:
        STATE_CACHE[key] = {
            "repo": repo,
            "issue_number": issue_number,
            "status": "NEW",
            "steps": {
                "label_applied": False,
                "comment_added": False,
                "plan_generated": False
            }
        }

    return STATE_CACHE[key]


def update_state(repo, issue_number, **updates):
    state = get_state(repo, issue_number)

    if "status" in updates:
        state["status"] = updates["status"]

    if "steps" in updates:
        state["steps"].update(updates["steps"])

    return state