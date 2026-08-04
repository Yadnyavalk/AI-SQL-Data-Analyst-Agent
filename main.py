from app.llm import get_llm
from app.prompts import SYSTEM_PROMPT
from app.database import run_query
from tabulate import tabulate


from langchain_core.messages import SystemMessage, HumanMessage


llm = get_llm()

print("Welcome to AI SQL Data Analyst 🚀")
print("-" * 50)

while True:



    user_question = input("\nAsk your question (or type 'exit'): ")

    if user_question.lower() == "exit":
        print("\nGoodbye! 👋")
        break

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_question)
    ]

    response = llm.invoke(messages)

    ai_response = response.content[0]["text"]

    response = llm.invoke(messages)

    ai_response = response.content[0]["text"]

    # Check whether Gemini generated SQL
    if ai_response.strip().upper().startswith("SELECT"):

        sql_query = ai_response

        print("\nGenerated SQL:")
        print(sql_query)

        results, headers = run_query(sql_query)

        if results is None:
            print("\nUnable to execute query.")
            continue

        print("\nQuery Results")
        print("=" * 50)

        if len(results) == 0:
            print("No records found.")

        else:
         
            print(tabulate(results,headers = headers,tablefmt="grid"))
                      

    else:
        print("\nAI:")
        print(ai_response)