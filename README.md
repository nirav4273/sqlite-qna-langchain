# SQLite Q&A with LangChain

A command-line agent that answers natural-language questions about a SQLite
todo list. It uses LangChain's SQL toolkit to inspect the database schema and
run read-only queries, with conversational memory across turns.

## How it works

- On startup, `main.py` ensures a `todos` table exists in `todo.db`
  (`id`, `title`, `date`, `status`).
- A LangChain agent is built with `SQLDatabaseToolkit`, giving it tools to
  list tables, inspect schema, and run SQL queries against the database.
- A system prompt constrains the agent to read-only-style behavior (no
  `DROP`/schema changes) and instructs it to answer based only on actual
  query results.
- Conversation history is kept in memory (`InMemorySaver`) so follow-up
  questions retain context within a session.

## Requirements

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/) for dependency management
- An API key for at least one supported LLM provider:
  - Groq (`GROQ_API_KEY`)
  - OpenAI (`OPENAI_API_KEY`)

## Setup

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root:

   ```env
   MODEL_PROVIDER=openai   # "openai" or "groq"

   GROQ_API_KEY=your_groq_key
   GROQ_MODEL=llama-3.1-8b-instant

   OPENAI_API_KEY=your_openai_key
   OPENAI_MODEL=gpt-4o-mini
   ```

3. Run the app:

   ```bash
   uv run main.py
   ```

4. Ask questions at the prompt, e.g. `What todos are still pending?`. Type
   `break` to exit.

## Notes

- `.env` is gitignored — never commit real API keys.
- The agent is instructed to avoid destructive SQL, but the model can still
  make mistakes; review its queries if you're working with data you care
  about.
