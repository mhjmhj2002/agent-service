# engine/scope_guard.py

CRUD_KEYWORDS = [
    # inglês
    "create", "update", "delete", "get", "list", "crud", "endpoint", "api", "post", "put",
    # português
    "criar", "atualizar", "deletar", "remover", "buscar", "listar", "endpoint"
]


def is_crud_issue(title, body):
    text = f"{title} {body}".lower()

    # regra 1: palavra-chave direta
    if any(keyword in text for keyword in CRUD_KEYWORDS):
        return True

    # regra 2: padrão REST (ex: POST /users)
    if any(method in text for method in ["post", "get", "put", "delete"]):
        if "/" in text:
            return True

    return False


def reject_reason():
    return (
        "🚫 This agent currently supports only CRUD-based API tasks.\n\n"
        "Supported examples:\n"
        "- Create endpoint (POST /resource)\n"
        "- List resources (GET /resource)\n"
        "- Update entity (PUT /resource/{id})\n"
        "- Delete entity (DELETE /resource/{id})\n\n"
        "Portuguese examples:\n"
        "- Criar endpoint\n"
        "- Listar recursos\n"
        "- Atualizar entidade\n\n"
        "Please refine your issue."
    )