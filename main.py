from app.sql_agent import SQLAgent
from tabulate import tabulate

# Create SQL Agent
agent = SQLAgent("bank_data")

print("Welcome to AI SQL Data Analyst 🚀")
print("-" * 50)

while True:

    # Take user input
    user_question = input("\nAsk your question (or type 'exit'): ")

    # Exit condition
    if user_question.lower() == "exit":
        print("\nGoodbye! 👋")
        break

    # Process user question
    response = agent.process_question(user_question)

    # If LLM generated SQL
    if response["type"] == "sql":

        print("\nGenerated SQL:")
        print(response["query"])

        print("\nQuery Results")
        print("=" * 50)

        # Database execution failed
        if response["results"] is None:
            print("Unable to execute query.")
            continue

        # No rows returned
        if len(response["results"]) == 0:
            print("No records found.")
        else:
            print(
                tabulate(
                    response["results"],
                    headers=response["headers"],
                    tablefmt="grid"
                )
            )

    # Normal AI response (not SQL)
    else:
        print("\nAI:")
        print(response["message"])