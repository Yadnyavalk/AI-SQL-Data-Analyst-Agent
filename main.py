from app.llm import get_llm
from app.prompts import SYSTEM_PROMPT

from langchain_core.messages import SystemMessage,HumanMessage




llm = get_llm()

messages = [SystemMessage(content  = SYSTEM_PROMPT),
            HumanMessage(content = "Show all employees from pune")]

response = llm.invoke(messages)

print(response.content)

