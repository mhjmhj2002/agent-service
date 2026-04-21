def normalize_plan(plan):
    allowed_types = [
        "controller",
        "service",
        "repository",
        "dto",
        "entity",
        "config"
    ]

    for step in plan["steps"]:
        if step["type"] not in allowed_types:
            step["type"] = "other"

    return plan