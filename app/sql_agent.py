from app.llm import get_llm
from app.prompts import SYSTEM_PROMPT
from app.error_prompt import ERROR_PROMPT
from app.mysql_database import run_query
from app.mysql_schema import get_database_schema

from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)


class SQLAgent:

    def __init__(self, database_name):

        # Create the LLM once
        self.llm = get_llm()

        # Store selected database
        self.database_name = database_name

        # Load database schema once
        self.schema = get_database_schema(self.database_name)

        self.chat_history = []

    def ask(self, user_question):
        """
        Converts user's English question into SQL using LLM.
        """

        messages = [
            SystemMessage(
                content=SYSTEM_PROMPT.format(
                    database_name=self.database_name,
                    schema=self.schema
                )
            )]
        messages.extend(self.chat_history)

        messages.append(
            HumanMessage(
                content=user_question
            ))
        

        response = self.llm.invoke(messages)

        self.chat_history.append(HumanMessage(content=user_question))

        self.chat_history.append(response)

        # Keep only the last 10 messages (5 user + 5 AI)
        self.chat_history = self.chat_history[-10:]

        ai_response = response.content

        # Remove markdown formatting
        ai_response = (
            ai_response
            .replace("```sql", "")
            .replace("```", "")
            .strip()
        )

        return ai_response

    def fix_sql(self, sql_query, error_message):
        """
        Fixes SQL query when database returns an error.
        """
        print("\n========== SQL AUTO FIX ==========")
        print("Original SQL:")
        print(sql_query)
        print("\nDatabase Error:")
        print(error_message)
        messages = [
            SystemMessage(
                content=ERROR_PROMPT.format(
                    database_name=self.database_name,
                    schema=self.schema,
                    sql_query=sql_query,
                    error=error_message
                )
            ),
            HumanMessage(
                content="Fix the SQL query."
            )
        ]

        response = self.llm.invoke(messages)

        corrected_sql = (
            response.content
            .replace("```sql", "")
            .replace("```", "")
            .strip()
        )

        print("\nCorrected SQL:")
        print(corrected_sql)
        print("=================================\n")
        
        return corrected_sql

    def execute_query(self, sql_query):
        """
        Executes SQL query on MySQL database.
        """

        results, headers, error = run_query(
            self.database_name,
            sql_query
        )

        return results, headers, error

    def process_question(self, user_question):
        """
        Main workflow of AI SQL Agent.
        """

        # Step 1: Generate SQL
        ai_response = self.ask(user_question)

        # Step 2: If AI generated SQL
        if ai_response.upper().startswith("SELECT"):

            results, headers, error = self.execute_query(ai_response)

            if error is None:
                return {
                    "type": "sql",
                    "query": ai_response,
                    "results": results,
                    "headers": headers,
                    "error": None
                }

            corrected_sql = self.fix_sql(
                ai_response,
                error
            )

            results, headers, error = self.execute_query(
                corrected_sql
            )

            if error is None:
                return {
                    "type": "sql",
                    "query": corrected_sql,
                    "results": results,
                    "headers": headers,
                    "error": None
                }

            return {
                "type": "chat",
                "message": "I couldn't generate a valid SQL query after attempting to correct it."
            }

        # Step 3: Normal AI response
        return {
            "type": "chat",
            "message": ai_response
        }