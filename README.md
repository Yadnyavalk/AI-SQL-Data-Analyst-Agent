# 🤖 AI SQL Data Analyst Agent

An AI-powered SQL Data Analyst that allows users to ask questions about MySQL databases using natural language.

The application converts natural-language questions into SQL queries using an LLM, executes the generated SQL against the selected MySQL database, displays the results, and automatically attempts to repair SQL queries when database execution errors occur.

---

## 🚀 Features

- 🗣️ **Natural Language Queries:** Ask database questions using natural language.
- 🤖 **AI-Powered SQL Generation:** Translates user questions into executable SQL.
- 🗄️ **MySQL Database Integration:** Connects directly with MySQL databases.
- 📊 **Tabular Result Display:** Displays query results in interactive tables.
- 💬 **Conversational Memory:** Remembers previous conversation turns for follow-up questions.
- 🔄 **Automatic SQL Error Correction:** Automatically attempts to repair invalid SQL queries.
- 📚 **Dynamic Schema Loading:** Dynamically loads tables, columns, and sample values.
- 🔀 **Multi-Database / Project Selection:** Allows users to switch between different databases.
- 🔐 **Secure Configuration:** Uses environment variables for API keys and database credentials.
- 🎈 **Interactive Streamlit UI:** Simple and clean user interface built with Streamlit.

---

## 🏗️ Project Architecture

The application follows a modular architecture centered around the `SQLAgent`.

```text
User
  ↓
Streamlit UI
  ↓
Project Selection
  ↓
SQLAgent (Brain)
  │
  ├──────────────┬─────────────────┐
  │              │                 │
  ▼              ▼                 ▼
Schema Loader  Conversation      Prompt
               Memory            Builder
  │              │                 │
  └──────────────┴─────────────────┘
                 │
                 ▼
             LLM Model
                 │
                 ▼
           Generated SQL
                 │
                 ▼
          MySQL Executor
                 │
            SQL Error?
             ┌───┴───┐
            No      Yes
             │        │
             │        ▼
             │   Error Prompt
             │        │
             │        ▼
             │    LLM Model
             │        │
             │        ▼
             │  Corrected SQL
             │        │
             │        ▼
             │   MySQL Executor
             │        │
             └────────┘
                 │
                 ▼
              Results
                 │
                 ▼
           Streamlit UI
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web interface |
| MySQL | Database engine |
| LangChain | LLM application framework |
| LangChain Core | Message and LLM interaction components |
| LangChain Groq | Groq LLM integration |
| Groq | LLM provider |
| Pandas | Query-result tabular display |
| python-dotenv | Environment variable loading |
| mysql-connector-python | MySQL connectivity |

---

## 📂 Project Structure

```text
AI-SQL-Data-Analyst-Agent/
│
├── app/
│   ├── error_prompt.py
│   ├── llm.py
│   ├── mysql_database.py
│   ├── mysql_schema.py
│   ├── projects.py
│   ├── prompts.py
│   └── sql_agent.py
│
├── main.py
├── streamlit_app.py
├── requirements.txt
├── .gitignore
└── README.md
```

The `.env` file is intentionally excluded from GitHub because it contains secret credentials.

---

## 📌 Supported Projects

The application currently supports multiple MySQL databases through project selection.

### 🏦 Bank Churn Analysis

**Database:** `bank_data`

### 🍕

**Pizza Sales Analysis**

**Database:** `pizzahut`

Project-to-database mapping is maintained in:

```text
app/projects.py
```

---

## ⚙️ How the Application Works

### 1. Project Selection

The user selects a project from the Streamlit interface.

The selected project determines which MySQL database will be used.

### 2. Database Schema Loading

`mysql_schema.py` dynamically retrieves the schema of the selected database.

The schema loader obtains:

- Available tables
- Column names
- Sample distinct values where available

This schema information is provided to the LLM so that SQL queries are generated using the available database structure.

### 3. Natural Language → SQL

The user's question is sent to the `SQLAgent`.

The agent provides the LLM with:

- System prompt
- Database name
- Database schema
- Conversation history
- Current user question

The LLM then generates the SQL query.

### 4. SQL Execution

The generated SQL query is executed against the selected MySQL database.

The database executor:

1. Opens a connection to the selected database.
2. Creates a database cursor.
3. Executes the SQL query.
4. Retrieves the result rows.
5. Retrieves the column headers.
6. Returns the results to the SQL Agent.

### 5. SQL Error Detection

If the generated SQL produces a database error, the SQL Agent does not immediately stop.

The application sends the following information to the SQL error-correction prompt:

- Original SQL query
- Database error
- Database schema
- Selected database

### 6. Automatic SQL Correction

The LLM receives the SQL error information and generates corrected SQL.

The corrected query is then executed against MySQL again.

If the corrected SQL succeeds, the results are returned to the Streamlit interface.

If the correction also fails, the application returns a message indicating that it could not generate a valid SQL query after attempting correction.

### 7. Result Display

Successful SQL results are returned with their column headers.

`streamlit_app.py` converts the results into a Pandas DataFrame and displays them using Streamlit.

---

## 🧠 Conversation Memory

The SQL Agent maintains conversation history so that follow-up questions can use previous context.

For example:

**User:**
> Show customers from Germany.

**User:**
> How many of them have exited?

The second question can use the context from the previous conversation.

The agent keeps only the most recent 10 messages, representing up to five user/AI message pairs.

This prevents the conversation history from growing indefinitely.

---

## 🔄 SQL Auto-Correction

One of the main features of the application is automatic SQL error correction.

```text
Natural Language Question
          ↓
         LLM
          ↓
    Generated SQL
          ↓
        MySQL
          ↓
     SQL Error?
      ↙       ↘
    No         Yes
    ↓           ↓
 Results    Error Prompt
                ↓
               LLM
                ↓
         Corrected SQL
                ↓
              MySQL
                ↓
             Results
```

The correction prompt specifically instructs the LLM to:

- Return only corrected SQL
- Preserve the original intent
- Use only tables and columns available in the schema
- Avoid explanations
- Avoid Markdown formatting

This allows the application to retry failed SQL queries instead of immediately returning an error to the user.

---

## 🔐 Environment Variables

Sensitive credentials are loaded through environment variables instead of being stored directly in the source code.

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
```

The `.env` file must **never** be uploaded to GitHub.

The repository's `.gitignore` file excludes `.env`.

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Yadnyavalk/AI-SQL-Data-Analyst-Agent.git
```

### 2. Navigate into the Project

```bash
cd AI-SQL-Data-Analyst-Agent
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment on Windows

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ MySQL Configuration

Make sure MySQL Server is installed and running.

The application currently uses the following configured databases:

- `bank_data`
- `pizzahut`

The corresponding databases and tables must exist in the MySQL instance before using the application.

Configure the MySQL connection details through the `.env` file.

Make sure the MySQL user has permission to access the required databases.

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

Streamlit will provide a local URL where the application can be accessed.

---

## 💡 Example Questions

### 🏦 Bank Churn Analysis

- Show the top 10 customers with the highest balance.
- How many customers have exited?
- Show the number of exited customers by geography.

### 🍕

**Pizza Sales Analysis**

- What are the top 10 pizzas by revenue?
- Show total sales by pizza category.

---

## 📁 Main Components

| File | Responsibility |
|---|---|
| `streamlit_app.py` | Streamlit user interface and interaction flow |
| `app/sql_agent.py` | Central SQL Agent and application workflow |
| `app/llm.py` | LLM initialization |
| `app/mysql_schema.py` | Dynamic MySQL schema extraction |
| `app/mysql_database.py` | MySQL connection and SQL execution |
| `app/projects.py` | Project-to-database configuration |
| `app/prompts.py` | Main SQL-generation prompt |
| `app/error_prompt.py` | SQL error-correction prompt |
| `requirements.txt` | Python dependencies |

---

## 🧩 Design Approach

The project was developed incrementally using separate development sprints.

The implementation evolved from a basic SQL-querying application into a modular AI SQL Agent with:

- LLM-based SQL generation
- MySQL database support
- Dynamic schema loading
- Multiple database/project support
- Conversational memory
- Automatic SQL error correction
- Streamlit interface improvements
- Deployment preparation

The `SQLAgent` acts as the central coordinator between:

- User requests
- LLM
- Database schema
- Conversation history
- SQL generation
- MySQL execution
- SQL error correction

---

## 🛡️ Security

The project keeps sensitive configuration outside the source code.

The following information should **never** be committed to GitHub:

- `.env`
- API keys
- Database passwords
- Private credentials

The `.gitignore` file excludes:

```text
.env
venv/
__pycache__/
*.pyc
*.pyo
.ipynb_checkpoints/
.vscode/
```

---

## 👨‍💻 Author

**Yadnyavalk Deshmukh**

Data Analyst | AI & Data Science

Pune, India

---

## 📌 Project Status

**Completed — Deployment Preparation**

The project was developed incrementally through multiple development sprints covering:

- Project setup
- LLM integration
- SQL generation
- Interactive query execution
- Database error handling
- Conversational interaction
- Dynamic schema handling
- MySQL migration
- Multi-project database support
- SQL error correction
- Conversation memory
- Streamlit UI improvements
- Deployment preparation

---

## ⭐ Future Improvements

Possible future improvements include:

- Cloud deployment
- Remote MySQL database support
- User authentication
- Additional database projects
- Query visualization and analytics
- Improved SQL validation
- Production-level monitoring

---
