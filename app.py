from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
import os

st.title("StuFlo AI")

os.environ["GOOGLE_API_KEY"] = 'AIzaSyAhMpPQ2UBCtdZBacgCM2S6XqFDudYU8pI'

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that provides hints to any student.",
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | llm

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = chain.invoke(
        {
            "input": prompt,
        }
    )

    with st.chat_message("assistant"):
        st.markdown(response.content)
    
    st.session_state.messages.append({"role": "assistant", "content": response.content})