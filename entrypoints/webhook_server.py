from flask import Flask, request, jsonify
from engine.agent_engine import process_issue

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    print("\n================ WEBHOOK RECEIVED ================")

    if not data:
        print("❌ Payload vazio")
        return jsonify({"status": "no payload"}), 400

    event = request.headers.get("X-GitHub-Event")
    action = data.get("action")

    print(f"[EVENT] {event} | action={action}")

    # =========================
    # ISSUE OPENED ONLY
    # =========================
    if event == "issues" and action == "opened":
        issue = data.get("issue", {})
        repo_data = data.get("repository", {})

        payload = {
            "repo": repo_data.get("name"),
            "number": issue.get("number"),
            "title": issue.get("title"),
            "body": issue.get("body", "")
        }

        print(f"[ISSUE] #{payload['number']} - {payload['title']}")

        process_issue(payload)

    # =========================
    # COMMENT CREATED ONLY
    # =========================
    elif event == "issue_comment" and action == "created":

        comment_data = data.get("comment", {})
        issue = data.get("issue", {})
        repo_data = data.get("repository", {})
        sender_data = data.get("sender", {})

        comment = comment_data.get("body", "").lower()
        sender = sender_data.get("login", "unknown")
        sender_type = sender_data.get("type", "User")

        print(f"[COMMENT] from={sender} (type={sender_type}): {comment}")

        # 🔥 IGNORA BOT (CORRETO)
        if sender_type == "Bot":
            print("🤖 Ignorando comentário de bot")
            return jsonify({"status": "ignored bot"})

        # 🔥 PROCESSA SÓ COMANDO
        if "approve plan" not in comment and "reject plan" not in comment:
            print("💤 Comentário irrelevante, ignorando")
            return jsonify({"status": "ignored comment"})

        payload = {
            "repo": repo_data.get("name"),
            "number": issue.get("number"),
            "title": issue.get("title"),
            "body": issue.get("body", "")
        }

        print("⚙️ Processando comando do usuário...")

        process_issue(payload)

    else:
        print("💤 Evento ignorado")

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)