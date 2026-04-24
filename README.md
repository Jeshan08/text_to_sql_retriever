# ⚓ TALK2DB AI: Secure Text-to-SQL Business Intelligence

This is an intelligent agentic system that allows users to query MySQL databases using natural language. Built with a focus on security,acts as a bridge between non-technical users and complex data structures, ensuring that all queries are analyzed for safety before execution.

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
| **Frontend** | Next.js 16, React 19, Tailwind CSS v4, TypeScript |
| **Backend** | FastAPI, Python 3.11 |
| **AI Orchestration** | LangChain, OpenAI GPT-4o |
| **Database** | MySQL, SQLAlchemy |

---

## 📁 Project Structure

```
SQL-ai/
├── .gitignore
├── backend/
│   ├── api    
│   │    └── query_routes.py                
│   ├── services
│   |   ├── langchain_agent.py   # The llm and sql chain code
│   │   └── security.py          # Forbidden command check 
│   ├── main.py                   # FastAPI app & API routes
│   ├── requirements.txt
│   ├── database.py               # SQLAlchemy engine
│   └── .env                      # Environment variables (never committed)
└── frontend/
    ├── app/
    │   ├── (dashboard)/
    │   │   └── page.tsx          # Main chat page — serves route "/"
    │   ├── layout.tsx            # Root layout (wraps all pages)
    │   └── globals.css           # Global styles (Tailwind v4)
    ├── components/
    │   └── dashboard/
    │       └── chatAgent.tsx     # Chat UI — input, messages, API calls
    ├── public/                   # Static assets
    ├── next.config.ts            # Next.js config
    ├── postcss.config.mjs        # PostCSS + Tailwind v4
    ├── eslint.config.mjs         # ESLint config
    ├── tsconfig.json             # TypeScript config
    └── package.json              # Dependencies
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
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the `backend/` folder:

```env
OPENAI_API_KEY=sk-...

DB_HOST=localhost
DB_PORT=3306
DB_USER=ai_readonly
DB_PASSWORD=your_password
DB_NAME=your_database
```

### 4. Create a MySQL read-only user

```sql
CREATE USER 'sql_readonly'@'localhost' IDENTIFIED BY 'your_password';
GRANT SELECT ON your_database.* TO 'sql_readonly'@'localhost';
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
Defines a `scan_sql()` function that uses regex to detect blocked SQL keywords before any query is executed. Keywords include `DROP`, `DELETE`, `UPDATE`, `INSERT`, `TRUNCATE`, `ALTER`, `CREATE`, `GRANT`, `REVOKE`, `EXEC` and more. Raises `UnsafeSQLError` on a match.

#### `agent.py`
Builds the LangChain SQL agent using `ChatOpenAI` (GPT-4o) and `SQLDatabaseToolkit`. The default query runner is replaced with a secure custom tool that calls `scan_sql()` before hitting the database. Exposes a single `run_query(question)` function for the API layer.

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

#### `package.json`
Key dependencies:

| Package | Version | Purpose |
| :--- | :--- | :--- |
| `next` | 16.2.4 | React framework |
| `react` | 19.2.4 | UI library |
| `react-markdown` | ^10.1.0 | Renders AI responses as Markdown |
| `tailwindcss` | ^4 | Utility-first CSS |
| `typescript` | ^5 | Type safety |

#### `next.config.ts`
Next.js configuration file. Currently using default settings — extend this to add environment variables, image domains, or custom webpack config.

#### `tsconfig.json`
TypeScript config with strict mode enabled. Uses `@/*` path alias mapped to the project root so you can import like `import X from "@/components/X"` from anywhere.

#### `postcss.config.mjs`
Configures PostCSS with `@tailwindcss/postcss` plugin for Tailwind v4 — which no longer requires a separate `tailwind.config.ts` file.

#### `eslint.config.mjs`
ESLint flat config using `eslint-config-next` for Next.js-specific linting rules.

#### `app/layout.tsx`
Root layout that wraps every page in the app. Sets the HTML metadata, loads fonts, and applies base className to the `<body>`. Anything placed here (navbar, footer) appears on every route.

#### `app/globals.css`
Global stylesheet using Tailwind v4 `@import "tailwindcss"` syntax. Add custom CSS variables or base styles here.

#### `app/(dashboard)/page.tsx`
The main page served at `http://localhost:3000/`. This is a **Next.js Server Component** — it handles the initial render on the server. The `(dashboard)` folder is a **route group**, meaning the folder name is ignored in the URL but keeps the project organised. This page renders the `ChatAgent` component.

#### `components/dashboard/chatAgent.tsx`
The core client-side chat component. Handles all user interaction including message state, loading state, sending questions to the FastAPI backend, and rendering the conversation. Uses `react-markdown` to display AI responses with full Markdown support including tables and code blocks.

---

## 🛡️ Security Design

SQL AI implements a **Defence-in-Depth** strategy with three independent layers:

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
3. **Contextual Rejection** — if a blocked query is attempted, SQL AI returns a human-readable explanation instead of an error trace.

---

## 📡 API Reference

### `POST /query`

**Request**
```json
{
  "question": "Who are our top 5 customers by revenue?"
}
```

**Response**
```json
{
  "answer": "The top 5 customers by total revenue are: ..."
}
```



---

## 📝 Author

Developed by **Jeshan Chhabra** — Software Engineer & AI Student.