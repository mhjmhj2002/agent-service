# engine/scope_guard.py

CRUD_KEYWORDS = ["create", "update", "delete", "get", "list", "crud"]

def is_crud_issue(title, body):
    text = f"{title} {body}".lower()

    return any(keyword in text for keyword in CRUD_KEYWORDS)


def reject_reason():
    return (
        "🚫 This agent currently supports only CRUD-based API tasks.\n\n"
        "Examples supported:\n"
        "- Create endpoint\n"
        "- List resources\n"
        "- Update entity\n\n"
        "Please refine your issue."
    )