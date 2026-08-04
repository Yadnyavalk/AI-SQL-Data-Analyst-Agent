from app.llm import get_llm
from app.prompts import SYSTEM_PROMPT
from app.database import run_query

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

    sql_query = response.content[0]["text"]

    print("\nGenerated SQL:")
    print(sql_query)

    results = run_query(sql_query)

    if results is None:
        print("\nUnable to execute query.")
        continue

    print("\nQuery Results")
    print("=" * 50)

    if len(results) == 0:
        print("No records found.")

    else:
        for employee in results:
            print(f"Employee ID : {employee[0]}")
            print(f"Name        : {employee[1]}")
            print(f"Department  : {employee[2]}")
            print(f"Salary      : ₹{employee[3]:,}")
            print(f"City        : {employee[4]}")
            print("-" * 50)