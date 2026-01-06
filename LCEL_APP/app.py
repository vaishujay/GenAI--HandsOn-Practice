## Import necessary libraries

import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough

import langsmith
client = langsmith.Client()
import streamlit as st

load_dotenv()

## Streamlit configurations
st.set_page_config(page_title="LCEL App",
                     page_icon=":robot_face:",
                     layout="centered")

st.write(""" This app answers the questions  strictly based on the context provided.""")

allowed_text = st.text_area("Enter the context here", height=200)

question = st.text_input("Enter your question here")

prompt = PromptTemplate.from_template(
    """
You must answer the questions strictly based on the context provided.
You must not use any prior knowledge.

Context:
{context}

Question:
{question}

If the answer is not contained within the context, respond with:
"I don't know the answer. I can only answer based on the context provided."
"""
)


llm = ChatOpenAI(model = "gpt-3.5-turbo", temperature=0)

## LCEL App Chain
chain = ({"context": RunnablePassthrough(), "question": RunnablePassthrough()}) | prompt | llm | StrOutputParser()

## Execute the chain on user button click
if st.button("Submit"):
    if not allowed_text.strip():
        st.error("Please provide both context ")
    elif not question.strip():
        st.error("Please provide a question")
    else:
        with st.spinner("Generating response..."):
            response = chain.invoke({"contxt": allowed_text, "question": question})

        st.subheader("Answer")
        st.success(response)
    