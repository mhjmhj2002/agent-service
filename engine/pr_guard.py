from adapters.github_pr import get_open_pull_requests


def has_existing_pr(repo, issue_number):
    prs = get_open_pull_requests(repo)

    for pr in prs:
        # heurística simples (melhor depois melhorar com label ou branch name)
        if f"#{issue_number}" in pr.get("title", ""):
            return True

        if f"issue-{issue_number}" in pr.get("head", {}).get("ref", ""):
            return True

    return False