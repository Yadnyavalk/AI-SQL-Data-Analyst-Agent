from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq

load_dotenv()


def get_llm():

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    return llm