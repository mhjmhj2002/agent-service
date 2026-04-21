import json

from engine.state_manager import get_state, update_state
from engine.planner import generate_plan
from engine.scope_guard import is_crud_issue, reject_reason
from engine.label_manager import sync_labels_with_state
from engine.pr_guard import has_existing_pr

from adapters.github_adapter import (
    add_label,
    comment_on_issue,
    get_issue_labels
)

from adapters.github_pr import (
    create_branch,
    create_file,
    create_pull_request
)


def process_issue(issue):

    repo = issue["repo"]
    issue_number = issue["number"]

    print("\n----- AGENT ENGINE -----")

    # 🔥 PR DUPLICATE GUARD (antes de tudo)
    if has_existing_pr(repo, issue_number):
        print("⚠️ PR já existe para essa issue. Abortando execução.")
        return

    # =========================
    # 1. VALIDATE INPUT
    # =========================
    if not repo or not issue_number:
        raise Exception("Invalid issue payload")

    # =========================
    # 2. GUARDS (GitHub + State)
    # =========================
    labels = get_issue_labels(issue_number, repo)
    state = get_state(repo, issue_number)

    print(f"State inicial: {state['status']}")

    if "in-progress" in labels:
        print("⚠️ Issue já está em progresso. Abortando execução.")
        return

    if "rejected" in labels:
        print("⚠️ Issue já foi rejeitada. Ignorando.")
        return

    if state.get("status") in ["DONE", "REJECTED"]:
        print(f"⚠️ Issue já finalizada ({state['status']}). Ignorando.")
        return

    # =========================
    # 3. STATE INIT
    # =========================
    if state["status"] == "NEW":
        update_state(repo, issue_number, status="IN_PROGRESS")

        add_label(issue_number, repo, "in-progress")
        comment_on_issue(issue_number, repo, "Agent started")

        update_state(
            repo,
            issue_number,
            steps={"label_applied": True, "comment_added": True}
        )

    # reload state
    state = get_state(repo, issue_number)

    # =========================
    # 4. SCOPE VALIDATION
    # =========================
    if not is_crud_issue(issue["title"], issue.get("body", "")):
        comment_on_issue(issue_number, repo, reject_reason())
        add_label(issue_number, repo, "rejected")
        update_state(repo, issue_number, status="REJECTED")

        print("❌ Issue fora do escopo")
        return

    # =========================
    # 5. PLAN (IA)
    # =========================
    if not state["steps"]["plan_generated"]:
        print("Gerando plano...")

        plan = generate_plan(issue["title"], issue.get("body", ""))
        plan["steps"] = sorted(plan["steps"], key=lambda x: x["id"])

        comment_on_issue(
            issue_number,
            repo,
            f"🧠 PLAN:\n\n```json\n{json.dumps(plan, indent=2)}\n```"
        )

        update_state(repo, issue_number, steps={"plan_generated": True})
        update_state(repo, issue_number, status="PLANNED")

    # reload state
    state = get_state(repo, issue_number)

    # =========================
    # 6. EXECUTE (PR FLOW)
    # =========================
    if state["status"] == "PLANNED":
        print("🚀 Criando PR...")

        branch_name = f"feature/issue-{issue_number}"

        create_branch(repo, branch_name)

        plan = generate_plan(issue["title"], issue.get("body", ""))

        create_file(
            repo,
            f"plans/issue-{issue_number}.json",
            json.dumps(plan, indent=2),
            f"Add plan for issue #{issue_number}",
            branch_name
        )

        pr = create_pull_request(
            repo,
            title=f"Feature: Issue #{issue_number}",
            body="Auto-generated PR by Agent",
            head=branch_name
        )

        print(f"✅ PR criado: {pr['html_url']}")

        update_state(repo, issue_number, status="DONE")

    # =========================
    # 7. SYNC
    # =========================
    state = get_state(repo, issue_number)

    labels = get_issue_labels(issue_number, repo)
    sync_labels_with_state(repo, issue_number, state, labels)

    print(f"Estado final: {state}")