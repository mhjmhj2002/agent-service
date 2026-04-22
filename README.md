# 🤖 Agentic Issue Processor

An experimental agent-based system that processes GitHub issues and generates structured implementation plans using AI.

---

## 🚀 Overview

This project simulates an autonomous software agent capable of:

- Reading GitHub issues
- Deciding execution flow
- Generating structured implementation plans via AI
- Posting results back to GitHub
- Managing execution state to avoid duplication

---

## 🧠 Architecture

```
agent_service/
├── engine/
│   ├── agent_engine.py
│   ├── planner.py
│   ├── state_manager.py
│   ├── schema_validator.py
│   ├── plan_normalizer.py
│   ├── prompt_loader.py
│   ├── scope_guard.py
│   ├── label_manager.py
│   └── pr_guard.py
│
├── adapters/
│   ├── github_adapter.py
│   └── github_pr.py
│
├── entrypoints/
│   └── event_runner.py
│
├── prompts/
│   └── planning/
│       ├── system.txt
│       └── user.txt
│
├── schemas/
│   └── plan_schema.json
│
├── state/
│   └── *.json
│
├── .env
├── .env.example
└── requirements.txt
```

---

## 🔁 Workflow

1. Load GitHub issue
2. Validate execution state
3. Apply guards:
   - Scope (CRUD only)
   - Concurrency (labels)
   - PR duplication
4. Move to `in-progress`
5. Generate plan via AI
6. Validate JSON output (schema)
7. Post plan as comment
8. Create branch + PR (future step)
9. Update state (`DONE`, `REJECTED`)
10. Sync labels with GitHub

---

## 📦 Example Output

```json
{
  "steps": [
    {
      "id": 1,
      "type": "controller",
      "name": "UserController",
      "description": "Create GET /users endpoint"
    }
  ]
}
```

---

## 🔐 Design Principles

- Deterministic execution
- Idempotent operations
- Schema validation for AI output
- Separation of concerns
- Externalized prompts
- Fail-fast error handling

---

## 🧪 Current Capabilities

- GitHub issue ingestion
- Scope validation (CRUD-only)
- AI-based plan generation
- JSON schema validation
- Output normalization
- State persistence (JSON)
- Label synchronization
- Duplicate PR prevention
- Local event simulation

---

## ⚙️ Setup & Configuration

### 1. Clone the repository

```bash
git clone https://github.com/your-user/agent-service.git
cd agent-service
```

---

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create your environment file

```bash
cp .env.example .env
```

---

### 5. Configure your `.env`

Edit the `.env` file:

```env
GITHUB_TOKEN=your_github_token
GITHUB_OWNER=your_username
GITHUB_REPOS=agentic-ia-web-api,agentic-ia-ms-user,agentic-ia-ms-order

OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini

DEBUG=true
DRY_RUN=false
ENVIRONMENT=dev
```

---

### 6. Run the project

```bash
python3 -m entrypoints.event_runner
```

---

## 🔄 Updating Dependencies (IMPORTANT)

If you install new libraries during development, update the dependency list:

```bash
pip freeze > requirements.txt
```

This ensures the project runs correctly on any machine.

---

## 🧪 Expected Behavior

When running, the agent will:

- Load a GitHub issue
- Apply the `in-progress` label
- Post a start comment
- Generate an implementation plan using AI
- Post the plan as structured JSON

---

## 🔍 Debug Tips

If something fails:

- Check if `.env` is properly configured
- Verify GitHub token permissions
- Ensure `OPENAI_API_KEY` is valid
- Activate virtual environment (`source venv/bin/activate`)
- Reinstall dependencies if needed:

```bash
pip install -r requirements.txt --upgrade
```
---

## ⚠️ Important

- `.env` is NOT versioned
- Never commit tokens or API keys
- `.env.example` is only a template

---

## ▶️ Running the Project

```bash
python3 -m entrypoints.event_runner
```

---

## 🧪 Expected Behavior

When executed, the agent will:

- Read a GitHub issue
- Validate scope (CRUD only)
- Apply `in-progress` label
- Generate an AI plan
- Post structured JSON
- Update execution state
- Prevent duplicate runs

---

## 🚫 Scope Limitation (v1)

This version only supports CRUD-based issues:

### ✅ Supported

- Create endpoint
- List resources
- Update entity
- Delete entity

### ❌ Not Supported

- AWS integrations (SQS, SNS, etc.)
- Messaging systems
- Complex workflows
- External APIs

Out-of-scope issues are automatically rejected.

---

## 🔍 Debug Tips

If something fails:

- Check `.env` configuration
- Validate GitHub token permissions
- Ensure OpenAI API key is valid
- Enable debug logs (`DEBUG=true`)

---

## 🚧 Next Steps

- Code generation (Spring Boot / Java)
- Automatic branch creation
- Pull request generation
- Test generation
- CI/CD integration
- Multi-agent orchestration

---

## ⚠️ Disclaimer

This project is experimental and intended for learning and architectural exploration of agent-based systems.

---

## 👨‍💻 Author

Study project focused on:

- Agentic AI
- Backend architecture
- Autonomous systems
- Dev automation