from app.sql_agent import SQLAgent
from tabulate import tabulate

agent = SQLAgent()

print("Welcome to AI SQL Data Analyst 🚀")
print("-" * 50)

while True:

    user_question = input("\nAsk your question (or type 'exit'): ")

    if user_question.lower() == "exit":
        print("\nGoodbye! 👋")
        break

    ai_response = agent.process_question(user_question)

    
    # Debug (remove later)
    print("\nDEBUG:")
    print(type(ai_response))
    print(ai_response)

    # Check if AI generated SQL
    if ai_response.upper().startswith("SELECT"):

        sql_query = ai_response

        print("\nGenerated SQL:")
        print(sql_query)

        # CHANGED
        results, headers = agent.execute_query(sql_query)

        if results is None:
            print("\nUnable to execute query.")
            continue

        print("\nQuery Results")
        print("=" * 50)

        if len(results) == 0:

            print("No records found.")

        else:

            print(
                tabulate(
                    results,
                    headers=headers,
                    tablefmt="grid"
                )
            )

    else:

        print("\nAI:")
        print(ai_response)