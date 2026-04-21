def select_best_issue(issues):
    def score(issue):
        labels = [l["name"] for l in issue.get("labels", [])]

        s = 0

        if "high-priority" in labels:
            s += 50
        if "bug" in labels:
            s += 30
        if "enhancement" in labels:
            s += 20

        if "in-progress" in labels:
            s -= 100

        body = issue.get("body") or ""
        s += max(0, 20 - len(body) // 50)

        return s

    return sorted(issues, key=score, reverse=True)[0]