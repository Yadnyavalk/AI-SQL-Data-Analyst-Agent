from app.sql_agent import SQLAgent

# Create the AI agent
agent = SQLAgent()

# Ask a question
question = "Show all employees"

print("=" * 60)
print("Question:")
print(question)
print("=" * 60)

# Get the response
result = agent.process_question(question)

print("\nComplete Result Dictionary:")
print(result)

print("\n" + "=" * 60)
print("Accessing Individual Values")
print("=" * 60)

print("\nType:")
print(result["type"])

if result["type"] == "sql":

    print("\nGenerated SQL:")
    print(result["query"])

    print("\nHeaders:")
    print(result["headers"])

    print("\nResults:")
    print(result["results"])

else:

    print("\nAI Message:")
    print(result["message"])