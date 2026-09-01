# Enterprise AI Assistant

A public reference implementation for an access-aware enterprise AI assistant. It demonstrates the engineering surface that is often missing from a chat-only prototype: retrieval, authorization before generation, grounded citations, audit events, latency and token metadata, and a repeatable evaluation harness.

This project is intentionally separate from Jinwon Lee's internal Samsung work. It uses synthetic documents and contains no company code, prompts, data, or architecture details.

## What it demonstrates

- Role-aware retrieval with SQLite FTS5 and policy filtering before model context is assembled
- A deterministic offline provider for reproducible local runs and tests
- An optional OpenAI provider using the Responses API
- Source citations and explicit handling of insufficient context
- In-memory audit events that record outcomes without logging document content
- Evaluation cases for retrieval hit rate, grounding checks, and access-safety checks
- A static browser demo that works on GitHub Pages without an API key

## Run the API-backed version

```bash
cd projects/enterprise-ai-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8088
```

Open `http://127.0.0.1:8088`.

The default provider is deterministic and makes no external calls. To use OpenAI:

```bash
cp .env.example .env
export OPENAI_API_KEY="your-key"
export ASSISTANT_PROVIDER="openai"
export OPENAI_MODEL="your-approved-model"
uvicorn app.main:app --reload --port 8088
```

The OpenAI integration uses `client.responses.create(...)` and the SDK's `output_text` helper. Access control remains in the application: only authorized documents are sent to the provider.

## Run tests

```bash
cd projects/enterprise-ai-assistant
python3 -m unittest discover -s tests -v
```

## Architecture

```text
Browser / API client
        |
        v
AssistantService -----> AuditLog
        |
        +-----> SQLite FTS5 retrieval
        |               |
        |               v
        |         role policy filter
        |               |
        v               v
Deterministic provider or OpenAI Responses API
        |
        v
Grounded answer + citations + runtime metadata
```

## Deliberate boundaries

- The included documents are synthetic.
- The audit store is in memory; a production deployment would use a durable, access-controlled sink.
- Cost is not invented. The response exposes token counts where the provider supplies them; a deployment can add an approved price table separately.
- This is a reference implementation, not a claim that the public demo is a production service.
