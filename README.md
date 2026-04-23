# ⚓ SQl AI: Secure Text-to-SQL Business Intelligence

This is an intelligent agentic system that allows users to query MySQL databases using natural language. Built with a focus on security, Vela acts as a bridge between non-technical users and complex data structures, ensuring that all queries are analyzed for safety before execution.

---

## ✨ Key Features

- **Natural Language Processing:** Ask questions like "Who are our top 3 customers?" and get instant answers.
- **Logic-Based Security Guardrails:** Custom middleware scans every generated SQL query to block destructive commands (`DROP`, `DELETE`, `UPDATE`, `TRUNCATE`).
- **Modern Next.js UI:** A clean, responsive dashboard with real-time feedback and Markdown-formatted responses.
- **Agentic Architecture:** Uses LangChain to handle the "Thought → Action → Observation" loop for accurate data retrieval.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Next.js 15, Tailwind CSS, React Markdown |
| **Backend** | FastAPI, Python 3.11 |
| **AI Orchestration** | LangChain, OpenAI GPT-4o |
| **Database** | MySQL, SQLAlchemy |

---

## 📁 Project Structure

```
SQL-ai/
├── backend/
│   ├── main.py          # FastAPI app & API routes
│   ├── agent.py         # LangChain SQL agent
│   ├── security.py      # SQL keyword scanner
│   ├── database.py      # SQLAlchemy engine
│   └── .env             # Environment variables
└── frontend/
    ├── app/
    │   ├── layout.tsx   # Root layout
    │   ├── page.tsx     # Main chat page
    │   └── globals.css  # Global styles
    ├── components/
    │   ├── ChatWindow.tsx    # Message list + scroll
    │   ├── MessageBubble.tsx # Individual message UI
    │   └── InputBar.tsx      # Text input + send button
    └── lib/
        └── api.ts       # Fetch wrapper for backend
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A running MySQL instance

---

## 🐍 Backend

### 1. Navigate to the backend folder

```bash
cd backend
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn langchain langchain-openai langchain-community sqlalchemy pymysql cryptography python-dotenv
```

### 3. Configure environment variables

Create a `.env` file in the `backend/` folder:

```env
OPENAI_API_KEY=sk-...

DB_HOST=localhost
DB_PORT=3306
DB_USER=Sql_readonly
DB_PASSWORD=your_password
DB_NAME=your_database
```

### 4. Create a MySQL read-only user

```sql
CREATE USER 'SQL_readonly'@'localhost' IDENTIFIED BY 'your_password';
GRANT SELECT ON your_database.* TO 'vela_readonly'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Start the server

```bash
python main.py
```

Backend runs at `http://localhost:8000`

---

### Backend File Explanations

#### `database.py`
Builds the SQLAlchemy engine from environment variables. Includes connection pooling (`pool_pre_ping`, `pool_recycle`) and a `validate_connection()` helper that pings the DB on startup.

#### `security.py`
Defines a `scan_sql()` function that uses regex to detect blocked SQL keywords before any query is executed. Keywords include `DROP`, `DELETE`, `UPDATE`, `INSERT`, `TRUNCATE`, `ALTER`, `CREATE`, `GRANT`, `REVOKE`, `EXEC`, and more. Raises `UnsafeSQLError` on a match.

#### `agent.py`
Builds the LangChain SQL agent using `ChatOpenAI` (GPT-4o) and `SQLDatabaseToolkit`. The default query runner is replaced with a **secure custom tool** that calls `scan_sql()` before hitting the database. Exposes a single `run_query(question)` function for the API layer.

#### `main.py`
FastAPI application with two routes:

| Method | Route | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Liveness probe — checks DB connectivity |
| `POST` | `/query` | Accepts `{ "question": "..." }`, returns `{ "answer": "..." }` |

CORS is configured to allow requests from `http://localhost:3000`.

---

## 🌐 Frontend

### 1. Navigate to the frontend folder

```bash
cd frontend
```

### 2. Install packages

```bash
npm install
```

### 3. Run the development server

```bash
npm run dev
```

Frontend runs at `http://localhost:3000`

---

### Frontend File Explanations

#### `app/page.tsx`
The root page component. Manages the `messages` state array and `loading` flag. Calls `sendQuestion()` from `lib/api.ts` on form submit, then appends both the user message and assistant response to state.

#### `app/layout.tsx`
Sets the HTML `<head>` metadata, loads the Inter and JetBrains Mono fonts from Google Fonts, and wraps all pages in a shared layout shell.

#### `lib/api.ts`
A typed fetch wrapper. `sendQuestion(question)` posts to `POST /query` and returns the answer string. `checkHealth()` hits `GET /health`. The base URL is read from `NEXT_PUBLIC_API_URL` (defaults to `http://localhost:8000`).

#### `components/ChatWindow.tsx`
Renders the scrollable list of messages. Auto-scrolls to the latest message on every update using a `bottomRef`. Shows an animated three-dot typing indicator while `loading` is true. Displays a welcome screen when the conversation is empty.

#### `components/MessageBubble.tsx`
Renders a single message. User messages appear as plain text in a blue bubble (right-aligned). Assistant messages are rendered with `react-markdown` + `remark-gfm` (left-aligned white bubble), supporting **tables**, **code blocks**, and all standard Markdown.

#### `components/InputBar.tsx`
Auto-resizing `<textarea>` that submits on **Enter** (Shift+Enter for newline). Calls `onSubmit()` with the trimmed question and resets itself after sending. The send button is disabled while a response is loading or the input is empty.

---

## 🛡️ Security Design

Vela implements a **Defence-in-Depth** strategy with three independent layers:

```
User Question
      │
      ▼
┌──────────────────────┐
│  FastAPI  /query     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  LangChain Agent     │  ← GPT-4o generates SQL
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  security.scan_sql() │  ← Blocks DROP / DELETE / UPDATE / …
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  MySQL (Read-Only)   │  ← DB-level permission enforcement
└──────────────────────┘
           │
           ▼
  Natural Language Answer
```

1. **Read-Only DB User** — the agent connects with a user that only has `SELECT` privileges.
2. **SQL Scanner** — a pre-execution middleware layer intercepts the LLM output and rejects any destructive keywords.
3. **Contextual Rejection** — if a blocked query is attempted, Vela returns a human-readable explanation instead of an error trace.



## 📝 Author

Developed by **Jeshan Chhabra** — Software Engineer & AI Student.