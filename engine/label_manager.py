from adapters.github_adapter import add_label


def sync_labels_with_state(repo, issue_number, state, current_labels):
    status = state["status"]

    print(f"[SYNC] Syncing labels for status: {status}")

    status_label_map = {
        "IN_PROGRESS": "in-progress",
        "PLANNED": "planned",
        "DONE": "done",
        "REJECTED": "rejected"
    }

    target_label = status_label_map.get(status)

    if not target_label:
        return

    if target_label not in current_labels:
        add_label(issue_number, repo, target_label)