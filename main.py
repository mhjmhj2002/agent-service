from github_client import (
    get_all_issues,
    comment_on_issue,
    agent_already_commented,
    add_label,
    has_label,
    plan_already_posted,
    select_best_issue
)

from ai_planner import generate_plan


def main():
    issues = get_all_issues()

    if not issues:
        print("Nenhuma issue encontrada.")
        return

    # 🧠 seleção inteligente (PASSO A)
    issue = select_best_issue(issues)

    issue_number = issue["number"]
    repo_name = issue["repo"]

    print("----- PROCESSANDO ISSUE -----")
    print(f"Repo: {repo_name}")
    print(f"Title: {issue['title']}")
    print(f"Body: {issue.get('body')}")
    print(f"Number: {issue_number}")

    # 🔹 1. LABEL
    if not has_label(issue_number, repo_name, "in-progress"):
        add_label(issue_number, repo_name, "in-progress")
        print("Label 'in-progress' adicionada!")
    else:
        print("Issue já está em progresso.")

    # 🔹 2. comentário inicial
    if not agent_already_commented(issue_number, repo_name):
        comment_on_issue(
            issue_number,
            repo_name,
            "🤖 Agent started processing this issue."
        )
        print("Comentário enviado!")
    else:
        print("Agente já comentou. Pulando...")

    # 🔥 3. PLANO (IA sob demanda)
    if not plan_already_posted(issue_number, repo_name):
        print("Gerando plano com IA...")

        plan = generate_plan(
            issue["title"],
            issue.get("body", "")
        )

        print("----- PLANO GERADO -----")
        print(plan)

        comment_on_issue(
            issue_number,
            repo_name,
            f"🧠 **Generated Plan:**\n\n{plan}"
        )
    else:
        print("Plano já existe. Pulando IA.")


if __name__ == "__main__":
    main()