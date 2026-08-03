from app.llm import get_llm
from app.prompts import SYSTEM_PROMPT
from app.database import run_query

from langchain_core.messages import SystemMessage,HumanMessage




llm = get_llm()

messages = [SystemMessage(content  = SYSTEM_PROMPT),
            HumanMessage(content = "Show all employees from pune")]

response = llm.invoke(messages)

sql_query = response.content[0]["text"]
print(sql_query)


results = run_query(sql_query)
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