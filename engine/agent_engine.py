import json

from engine.state_manager import get_state, update_state
from engine.planner import generate_plan
from engine.scope_guard import is_crud_issue, reject_reason
from engine.label_manager import sync_labels_with_state
from engine.pr_guard import has_existing_pr

from adapters.github_adapter import (
    add_label,
    comment_on_issue,
    get_issue_labels,
    get_issue_comments
)

from adapters.github_pr import (
    create_branch,
    create_file,
    create_pull_request
)


def check_approval(issue_number, repo):
    comments = get_issue_comments(issue_number, repo)

    if not comments:
        return None

    last_comment = comments[-1]["body"].lower()

    if "approve plan" in last_comment:
        return "approved"

    if "reject plan" in last_comment:
        return "rejected"

    return None


def process_issue(issue):

    repo = issue["repo"]
    issue_number = issue["number"]

    print("\n----- AGENT ENGINE -----")

    # =========================
    # 1. VALIDATE INPUT
    # =========================
    if not repo or not issue_number:
        raise Exception("Invalid issue payload")

    # =========================
    # 2. PR DUPLICATE GUARD
    # =========================
    if has_existing_pr(repo, issue_number):
        print("⚠️ PR já existe para essa issue. Abortando execução.")
        return

    # =========================
    # 3. LOAD STATE + LABELS
    # =========================
    labels = get_issue_labels(issue_number, repo)
    state = get_state(repo, issue_number)

    print(f"State inicial: {state['status']}")

    if "rejected" in labels:
        print("⚠️ Issue já foi rejeitada. Ignorando.")
        return

    if state.get("status") in ["DONE", "REJECTED"]:
        print(f"⚠️ Issue já finalizada ({state['status']}). Ignorando.")
        return

    # =========================
    # 4. STATE INIT
    # =========================
    if state["status"] == "NEW":
        print("🚀 Inicializando planejamento")

        update_state(repo, issue_number, status="PLANNING")

        comment_on_issue(
            issue_number,
            repo,
            "🤖 Agent started - generating development plan..."
        )

    # reload state
    state = get_state(repo, issue_number)

    # =========================
    # 5. SCOPE VALIDATION
    # =========================
    if not is_crud_issue(issue["title"], issue.get("body", "")):
        comment_on_issue(issue_number, repo, reject_reason())
        add_label(issue_number, repo, "rejected")
        update_state(repo, issue_number, status="REJECTED")

        print("❌ Issue fora do escopo")
        return

    # =========================
    # 6. PLAN GENERATION
    # =========================
    if not state.get("steps", {}).get("plan_generated"):
        print("🧠 Gerando plano...")

        plan = generate_plan(issue["title"], issue.get("body", ""))

        if isinstance(plan, dict) and "steps" in plan:
            plan["steps"] = sorted(plan["steps"], key=lambda x: x.get("id", 0))

        # ⚠️ sem markdown com ``` pra não quebrar string
        comment_body = (
            "## 🤖 AI Development Plan\n\n"
            "JSON Plan:\n\n"
            f"{json.dumps(plan, indent=2)}\n\n"
            "---\n\n"
            "### ⏳ Awaiting approval\n\n"
            "Reply with:\n"
            "- approve plan\n"
            "- reject plan\n"
        )

        comment_on_issue(issue_number, repo, comment_body)

        update_state(
            repo,
            issue_number,
            status="WAITING_APPROVAL",
            steps={"plan_generated": True}
        )

        return  # ⛔ PARA AQUI

    # reload state
    state = get_state(repo, issue_number)

    # =========================
    # 7. APPROVAL STEP
    # =========================
    if state["status"] == "WAITING_APPROVAL":
        print("⏳ Aguardando aprovação do plano...")

        decision = check_approval(issue_number, repo)

        if decision == "approved":
            print("✅ Plano aprovado")

            update_state(repo, issue_number, status="APPROVED")

            comment_on_issue(
                issue_number,
                repo,
                "✅ Plan approved. Starting execution..."
            )

        elif decision == "rejected":
            print("❌ Plano rejeitado")

            update_state(repo, issue_number, status="REJECTED")

            comment_on_issue(
                issue_number,
                repo,
                "❌ Plan rejected by user."
            )

        return

    # =========================
    # 8. EXECUTION (PR FLOW)
    # =========================
    if state["status"] == "APPROVED":
        print("🚀 Executando plano e criando PR...")

        branch_name = f"feature/issue-{issue_number}"

        create_branch(repo, branch_name)

        # por enquanto só salva o plano (próximo passo = gerar código)
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
    # 9. SYNC LABELS
    # =========================
    state = get_state(repo, issue_number)

    labels = get_issue_labels(issue_number, repo)
    sync_labels_with_state(repo, issue_number, state, labels)

    print(f"Estado final: {state}")