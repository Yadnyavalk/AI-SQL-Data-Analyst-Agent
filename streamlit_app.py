import streamlit as st
import pandas as pd

from app.sql_agent import SQLAgent
from app.projects import PROJECTS


if "history" not in st.session_state:
    st.session_state.history = []


st.title("🤖 AI SQL Data Analyst")

st.sidebar.title("📌 About")
st.sidebar.markdown("---")

st.subheader("📂 PROJECT")

selected_project = st.selectbox(
    "",
    list(PROJECTS.keys()),
    label_visibility="collapsed"
)

database_name = PROJECTS[selected_project]["database"]

agent = SQLAgent(database_name)

st.sidebar.write(
    """
AI-powered SQL Data Analyst

Built with:
- Groq
- LangChain
- MySQL
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
            {
                "question": question,
                "result": result
            }
        )


for chat in st.session_state.history:

    st.markdown("---")

    st.write("👤 You:")
    st.write(chat["question"])

    result = chat["result"]

    if result["type"] == "sql":

        st.write("🤖 Generated SQL")
        st.code(result["query"], language="sql")

        if result["error"]:
            st.error(result["error"])

        else:
            df = pd.DataFrame(
                result["results"],
                columns=result["headers"]
            )

            st.dataframe(df)

    else:

        st.write("🤖 AI")
        st.write(result["message"])