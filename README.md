# 🤖 Agentic Issue Processor

An experimental agent-based system that processes GitHub issues and generates structured implementation plans using AI.

---

## 🚀 Overview

This project simulates an autonomous software agent capable of:

* Reading GitHub issues
* Deciding execution flow
* Generating structured implementation plans via AI
* Posting results back to GitHub
* Managing execution state to avoid duplication

---

## 🧠 Architecture

```
agent_service/
├── engine/
│   ├── agent_engine.py      # Core orchestration logic
│   ├── planner.py           # AI integration (OpenAI)
│   ├── state_manager.py     # Execution state control
│   ├── schema_validator.py  # JSON validation
│   ├── plan_normalizer.py   # AI output normalization
│   └── prompt_loader.py     # External prompt loader
│
├── adapters/
│   └── github_adapter.py    # GitHub API integration
│
├── entrypoints/
│   └── event_runner.py      # Local event simulation
│
├── prompts/
│   └── planning/
│       ├── system.txt       # System prompt (AI behavior)
│       └── user.txt         # User prompt template
│
├── schemas/
│   └── plan_schema.json     # Output contract
│
└── .env                     # Environment variables
```

---

## 🔁 Workflow

1. Load GitHub issue
2. Check execution state
3. Apply label (`in-progress`)
4. Post initial comment
5. Generate plan using AI
6. Normalize and validate output
7. Post structured JSON plan
8. Update execution state

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

* Deterministic execution
* Idempotent operations
* AI output validation (schema-based)
* Separation of concerns
* Prompt externalization
* Fail-fast error handling

---

## 🧪 Current Capabilities

* GitHub issue ingestion
* AI-based plan generation
* JSON schema validation
* Output normalization
* State management
* Local event simulation

---

## 🚧 Next Steps

* Execute plan steps automatically
* Generate code artifacts (Java/Spring Boot)
* Introduce retry strategies for AI failures
* Add multi-agent coordination
* Integrate with CI/CD pipelines

---

## ⚠️ Disclaimer

This project is experimental and intended for learning and architectural exploration of agent-based systems.

---

## 👨‍💻 Author

Study project focused on autonomous agents, AI orchestration, and backend architecture.

## ⚙️ Setup & Configuration

### 1. Clone the repository

```bash
git clone https://github.com/your-user/agent-service.git
cd agent-service
```

---

### 2. Create your environment file

This project uses environment variables for configuration.

A template file is provided:

```bash
cp .env.example .env
```

---

### 3. Configure your `.env`

Open the `.env` file and fill in your credentials:

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

### ⚠️ Important

* The `.env` file is **NOT committed** to the repository
* Never expose your tokens or API keys
* The `.env.example` file is only a template

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Run the project

```bash
python3 -m entrypoints.event_runner
```

---

### 🧪 Expected Behavior

When running, the agent will:

* Load a GitHub issue
* Apply the `in-progress` label
* Post a start comment
* Generate an implementation plan using AI
* Post the plan as structured JSON

---

### 🔍 Debug Tips

If something fails:

* Check if `.env` is properly filled
* Verify your GitHub token permissions
* Ensure `OPENAI_API_KEY` is valid
* Enable debug logs (`DEBUG=true`)

---
