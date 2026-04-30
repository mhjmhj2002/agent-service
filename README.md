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
│   ├── event_runner.py
│   └── webhook_server.py
│
├── prompts/
│   └── planning/
│
├── schemas/
│
├── state/
│
├── .env
├── .env.example
└── requirements.txt
```

---

## 🔁 Workflow (Atual)

1. GitHub dispara evento
2. Webhook recebe evento
3. Filtro por tipo (`issues`, `issue_comment`)
4. Agent engine processa:

    * valida estado
    * valida escopo (CRUD)
    * gera plano com IA
5. Aguarda aprovação humana
6. Dev responde:

    * `approve plan`
    * `reject plan`
7. Agent continua fluxo

---

## 🌐 Webhook Setup (GitHub + ngrok)

> ⚠️ ESSENCIAL para funcionamento real (sem simulação)

---

### 1. Subir servidor webhook

```bash
python3 -m entrypoints.webhook_server
```

Servidor roda em:

```
http://localhost:5000/webhook
```

---

### 2. Expor com ngrok

Instalar:

```bash
sudo snap install ngrok
```

Criar conta:
https://dashboard.ngrok.com/signup

Configurar token:

```bash
ngrok config add-authtoken SEU_TOKEN
```

Subir túnel:

```bash
ngrok http 5000
```

Você vai receber algo como:

```
https://xxxxx.ngrok-free.dev
```

---

### 3. Configurar webhook no GitHub

No repositório:

```
Settings → Webhooks → Add webhook
```

Configurar:

* **Payload URL**

```
https://SEU-NGROK/webhook
```

* **Content type**

```
application/json
```

* **Events**
  Selecionar:
* Issues
* Issue comments

Salvar.

---

## 🔥 Importante (evitar bugs)

### ✅ Filtros implementados

O sistema evita problemas comuns de webhook:

* execução duplicada
* loop infinito (bot chamando ele mesmo)
* eventos irrelevantes

### 🧠 Regras

* Só processa:

    * `issues.opened`
    * `issue_comment.created`
* Ignora:

    * comentários do próprio bot
    * comentários sem comando (`approve plan`, `reject plan`)

---

## 🧪 Fluxo Real (End-to-End)

1. Criar issue no GitHub:

```
Criar endpoint POST /clientes
```

---

2. Sistema responde automaticamente:

* adiciona comentário
* gera plano com IA

---

3. Dev aprova:

```
approve plan
```

---

4. Sistema:

* detecta aprovação
* continua execução

---

## ⚙️ Setup & Configuration

### 1. Clone

```bash
git clone https://github.com/your-user/agent-service.git
cd agent-service
```

---

### 2. Virtual env

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Instalar deps

```bash
pip install -r requirements.txt
```

---

### 4. .env

```bash
cp .env.example .env
```

Editar:

```env
GITHUB_TOKEN=your_github_token
GITHUB_OWNER=your_username

OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
```

---

## ▶️ Execução

### 🔹 Modo simulado

```bash
python3 -m entrypoints.event_runner
```

---

### 🔹 Modo real

```bash
python3 -m entrypoints.webhook_server
```

* ngrok ativo

---

## 🧪 Expected Behavior

* Issue criada → plano gerado automaticamente
* Comentário `approve plan` → continua fluxo
* Sem duplicação
* Sem loops

---

## 🚫 Scope Limitation (v1)

### ✅ Suportado

* CRUD APIs
* Controllers / Services / Repositories

### ❌ Não suportado

* Integrações externas
* Mensageria
* Workflows complexos

---

## 🧠 Design Principles

* Idempotência
* Event-driven
* State-driven execution
* Guard rails
* AI com validação de schema

---

## 🚧 Next Steps

* Atualizar `pom.xml` automaticamente
* Gerar código Spring Boot
* Criar PR automático
* Testes automatizados
* Multi-agent orchestration

---

## ⚠️ Important

* Nunca versionar `.env`
* Tokens são sensíveis
* ngrok URL muda a cada execução (free)

---

## 👨‍💻 Author

Study project focused on:

* Agentic AI
* Backend architecture
* Dev automation
* Autonomous systems
