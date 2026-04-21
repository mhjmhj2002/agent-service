import json

from engine.state_manager import get_state, update_state
from engine.planner import generate_plan
from adapters.github_adapter import (
    add_label,
    comment_on_issue
)


def process_issue(issue):
    repo = issue["repo"]
    issue_number = issue["number"]

    state = get_state(repo, issue_number)

    print("\n----- AGENT ENGINE -----")
    print(f"State inicial: {state['status']}")

    # 🟡 IN_PROGRESS
    if state["status"] == "NEW":
        update_state(repo, issue_number, status="IN_PROGRESS")

        add_label(issue_number, repo, "in-progress")
        comment_on_issue(issue_number, repo, "Agent started")

        update_state(
            repo,
            issue_number,
            steps={"label_applied": True, "comment_added": True}
        )

    # 🔄 RELOAD STATE
    state = get_state(repo, issue_number)

    # 🧠 PLANO
    if not state["steps"]["plan_generated"]:
        print("Gerando plano...")

        plan = generate_plan(issue["title"], issue.get("body", ""))

        # 🔥 ordena steps
        plan["steps"] = sorted(plan["steps"], key=lambda x: x["id"])

        comment_on_issue(
            issue_number,
            repo,
            f"🧠 PLAN:\n\n```json\n{json.dumps(plan, indent=2)}\n```"
        )

        update_state(repo, issue_number, steps={"plan_generated": True})
        update_state(repo, issue_number, status="PLANNED")

    # 🔄 RELOAD STATE
    state = get_state(repo, issue_number)

    # 🟢 FINAL
    if state["steps"]["plan_generated"]:
        update_state(repo, issue_number, status="DONE")

    print(f"Estado final: {get_state(repo, issue_number)}")