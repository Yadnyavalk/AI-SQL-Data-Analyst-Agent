# 🤖 AI SQL Data Analyst Agent

An AI-powered SQL Data Analyst that allows users to ask questions about MySQL databases using natural language.

The application converts natural-language questions into SQL queries using an LLM, executes the generated SQL against the selected MySQL database, displays the results, and automatically attempts to repair SQL queries when database execution errors occur.

---

## 🚀 Features

- 🗣️ Ask database questions using natural language
- 🤖 AI-powered SQL generation
- 🗄️ MySQL database integration
- 📊 Display query results in a tabular format
- 💬 Conversational memory for follow-up questions
- 🔄 Automatic SQL error correction
- 📚 Dynamic database schema loading
- 🔀 Multiple database/project selection
- 🔐 Environment-variable based API and database credentials
- 🎈 Interactive Streamlit interface

---

## 🏗️ Project Architecture

The application follows a modular architecture:

```text
User
  ↓
Streamlit UI
  ↓
Project Selection
  ↓
SQLAgent
  ├── Load Database Schema
  ├── Conversation Memory
  ├── Prompt Construction
  └── LLM
        ↓
    Generated SQL
        ↓
    MySQL Query Executor
        ↓
   ┌────┴────┐
   ↓         ↓
Success    Error
   ↓         ↓
Results   SQL Auto Repair
             ↓
          Corrected SQL
             ↓
       Execute Again
             ↓
          Results



🛠️ Tech Stack
Python
Streamlit
MySQL
LangChain
LangChain Core
LangChain Groq
Groq LLM
Pandas
python-dotenv
mysql-connector-python
📂 Project Structure
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
├── .env
└── README.md

.env is intentionally excluded from GitHub because it contains secret credentials.

📌 Supported Projects

The application currently supports multiple MySQL databases through project selection.

🏦 Bank Churn Analysis

Database:

bank_data
🍕

Pizza Sales Analysis

Database:

pizzahut

Projects are configured through app/projects.py.

⚙️ How It Works
1. Select a Project

The user selects a project from the Streamlit interface.

The selected project determines which MySQL database will be used.

2. Load Database Schema

The application dynamically reads the selected database schema.

It retrieves:

Tables
Columns
Sample distinct values

This schema is provided to the LLM so that SQL queries are generated using the available database structure.

3. Generate SQL

The user's natural-language question is sent to the SQL Agent.

The agent provides the LLM with:

System prompt
Database name
Database schema
Conversation history
Current user question

The LLM generates the SQL query.

4. Execute SQL

The generated SQL query is executed against the selected MySQL database.

If successful, the query results are returned and displayed in Streamlit.

5. Automatic SQL Repair

If the generated SQL produces a database error, the application sends the following information to the LLM:

Original SQL
Database error
Database schema

The LLM generates corrected SQL and the application executes it again.

6. Display Results

Successful query results are converted into a Pandas DataFrame and displayed in the Streamlit interface.

🧠 Conversation Memory

The SQL Agent maintains conversation history so that follow-up questions can use previous context.

For example:

User:
Show customers from Germany.

User:
How many of them have exited?

The second question can use the context from the previous conversation.

The application also limits stored conversation history to prevent it from growing indefinitely.

🔐 Environment Variables

API keys and database credentials are not stored directly in the source code.

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password

Never upload the .env file to GitHub.

The repository contains a .gitignore rule to prevent environment variables from being committed.

📦 Installation

Clone the repository:

git clone https://github.com/Yadnyavalk/AI-SQL-Data-Analyst-Agent.git

Navigate into the project:

cd AI-SQL-Data-Analyst-Agent

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
🗄️ MySQL Setup

Make sure MySQL Server is installed and running.

Create the required databases and import the corresponding datasets.

The application currently expects the configured project databases:

bank_data
pizzahut

Make sure the MySQL credentials in .env have permission to access these databases.

▶️ Run the Application

Start the Streamlit application:

streamlit run streamlit_app.py

Streamlit will provide a local URL where the application can be accessed.

💡 Example Questions
Bank Churn Analysis
Show the top 10 customers with the highest balance.
How many customers have exited?
Show the number of exited customers by geography.
Pizza Sales Analysis
What are the top 10 pizzas by revenue?
Show total sales by pizza category.
🔄 SQL Auto-Repair

One of the key features of this project is automatic SQL error correction.

Natural Language Question
        ↓
LLM
        ↓
Generated SQL
        ↓
MySQL
        ↓
   SQL Error?
     ↙     ↘
   No       Yes
   ↓         ↓
Results   Error Prompt
             ↓
            LLM
             ↓
        Corrected SQL
             ↓
           MySQL

This allows the application to retry failed SQL queries instead of immediately returning an error to the user.

📁 Main Components
File	Responsibility
streamlit_app.py	Streamlit user interface
sql_agent.py	Central SQL Agent and workflow
llm.py	LLM initialization
mysql_schema.py	Dynamic MySQL schema extraction
mysql_database.py	MySQL connection and query execution
projects.py	Project-to-database configuration
prompts.py	Main SQL generation prompt
error_prompt.py	SQL error correction prompt
🔒 Security

Sensitive credentials are stored using environment variables.

The following information should never be committed to GitHub:

.env
API keys
Database passwords
Private credentials

The .gitignore file is configured to exclude .env and the Python virtual environment.

👨‍💻 Author

Yadnyavalk Deshmukh

Data Analyst | AI & Data Science

Pune, India

📌 Project Status

Completed — Deployment Preparation

The project has been developed incrementally through multiple development sprints, including:

Project setup
LLM integration
SQL generation
MySQL migration
Multi-project database support
Dynamic schema loading
Conversational memory
SQL error correction
Streamlit UI improvements
Deployment preparation