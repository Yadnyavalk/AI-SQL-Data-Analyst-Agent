from app.llm import get_llm
from app.prompts import SYSTEM_PROMPT
from app.mysql_database import run_query
from app.mysql_schema import get_database_schema



from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)


class SQLAgent:

    def __init__(self,database_name):
        # Create the LLM once
        self.llm = get_llm()

        # store selected databse,so agent remembers which database it using if asked different que,
        # storing here becoz passing database name like 
        # agent.process_question("bank_data",question)  becomes messy 
           
        self.database_name = database_name

        # Load the database schema once
        self.schema = get_database_schema(self.database_name)

    def ask(self, user_question):
        """
        Converts the user's English question into SQL using the LLM.
        """

        messages = [
            SystemMessage(
                content=SYSTEM_PROMPT.format(

                    database_name=self.database_name,
                    schema=self.schema
                
                )
            ),
            HumanMessage(
                content=user_question
            )
        ]

        response = self.llm.invoke(messages)

        ai_response = response.content

        # Remove markdown if the model returns ```sql ... ```
        ai_response = (
            ai_response
            .replace("```sql", "")
            .replace("```", "")
            .strip()
        )

        return ai_response

    def execute_query(self, sql_query):
        """
        Executes the generated SQL query on SQLite.
        """

        results, headers = run_query(self.database_name,sql_query)

        return results, headers

    def process_question(self, user_question):
        """
        Main workflow of the AI SQL Agent.
        """

        # Step 1: Generate SQL (or AI response)
        ai_response = self.ask(user_question)

        # Step 2: If AI generated SQL
        if ai_response.upper().startswith("SELECT"):

            results, headers = self.execute_query(ai_response)

            return {
                "type": "sql",
                "query": ai_response,
                "results": results,
                "headers": headers
            }

        # Step 3: Otherwise return normal AI response
        return {
            "type": "chat",
            "message": ai_response
        }

        """
# What did we just do?
# We created a class called:
# SQLAgent

# Think of it as your own AI employee.
# Earlier, main.py itself had to:
# - create the LLM
# - load the schema
# - remember everything

# Now the agent will remember those things itself.
# When we create it:
# agent = SQLAgent()

# Python automatically runs __init__() and stores:
# self.llm
# self.schema
# inside the object.

# So instead of repeatedly writing:
# llm = get_llm()
# schema = get_database_schema()
# we write them once when the agent is created.
"""

"""
ai_response = (
    ai_response
    .replace("```sql", "")
    .replace("```", "")
    .strip()
)

# This is not AI logic. It's just cleaning text.
# Imagine Groq returns this:
# ```sql
# SELECT * FROM employees;
# ```

# Notice those extra symbols?
# ```sql
# and
# ```

# These are called Markdown code fences.
# AI models sometimes return SQL like this because they're formatted for humans.
# But our database only understands SQL.
# SQLite wants:
# SELECT * FROM employees;

# It doesn't want:
# ```sql
# SELECT * FROM employees;
# ```

# So we remove the extra formatting.
# First line:
# .replace("```sql", "")

# Suppose:
# ai_response = "```sql\nSELECT * FROM employees;"

# After this:
# ai_response = ai_response.replace("```sql", "")

# Result:
# SELECT * FROM employees;

# The starting ```sql is removed.
"""