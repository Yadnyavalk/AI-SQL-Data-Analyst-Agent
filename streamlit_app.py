import streamlit as st
import pandas as pd
from app.sql_agent import SQLAgent


if "history" not in st.session_state:
    st.session_state.history=[]

st.title("🤖 AI SQL Data Analyst")

st.sidebar.title("📌 About")

st.sidebar.markdown("---")

st.subheader("📂 PROJECT")

selected_project = st.selectbox(
    "",
    [
        "🏦 Bank Churn Analysis",
        "🍕 Pizza Sales Analysis"
    ]
)
if selected_project == "🏦 Bank Churn Analysis":
    database_name = "bank_data"

else:
    database_name = "pizzahut"

agent = SQLAgent(database_name)


st.sidebar.write(
    """
    AI-powered SQL Data Analyst

    Built with:
    - Groq
    - LangChain
    - MYSQL
    - Streamlit
    """
)

if st.button("🗑 Clear Chat"):

    st.session_state.history = []

    st.rerun()

question = st.text_input("Ask your question")

if st.button("Ask"):

    if question.strip() == "":

        st.warning("Please enter the question")

    else:

        with st.spinner("Thinking..."):

            result = agent.process_question(question)

        st.session_state.history.append(
                 
                 {"question": question,
                 "result": result})         

for chat in st.session_state.history:

    st.markdown("---")

    st.write("👤 You:")
    st.write(chat["question"])

    result = chat["result"]

    if result["type"] == "sql":

        st.write("🤖 Generated SQL")

        st.code(result["query"], language="sql")

        df = pd.DataFrame(
            result["results"],
            columns=result["headers"]
        )

        st.dataframe(df)

    else:

        st.write("🤖 AI")

        st.write(result["message"])