def select_repository(issue_title, issue_body):
    text = f"{issue_title} {issue_body}".lower()

    if "user" in text:
        return "ms-user"

    if "order" in text:
        return "ms-order"

    if "gateway" in text or "web-api" in text:
        return "web-api"

    return "unknown"