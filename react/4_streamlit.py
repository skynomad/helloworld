import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

st.title("Bedrock Chat")

chat = ChatOpenAI(
    api_key=st.secrets.llm.api_key,
    base_url=st.secrets.llm.base_url,
    model="llama3.2:3b-instruct-fp16",
    temperature=0,
    max_tokens=1000,
    streaming=True,
)

messages = [
    SystemMessage(content="Your task is to answer your questions clearly. "),
]

if prompt := st.chat_input("Please ask me anything."):
    messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        st.write_stream(chat.stream(messages))

for message in st.session_state.messages:
    if message.type != "system":
        with st.chat_message(message.type):
            st.markdown(message.content)

if prompt := st.chat_input("Please ask me anything."):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = st.write_stream(chat.stream(st.session_state.messages))

    st.session_state.messages.append(AIMessage(content=response))