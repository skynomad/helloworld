import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

st.title("Bedrock Chat")

if "session_id" not in st.session_state:
    st.session_state.session_id = "session_id"
if "history" not in st.session_state:
    st.session_state.history = DynamoDBChatMessageHistory(
        table_name="OpenChatSessionTable", session_id=st.session_state.session_id
    )

if "chain" not in st.session_state:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Your task is to answer the user's questions clearly. "),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="human_message"),
        ]
    )

    chat = ChatOpenAI(
        api_key=st.secrets.llm.api_key,
        base_url=st.secrets.llm.base_url,
        model="llama3.2:3b-instruct-fp16",
        temperature=0,
        max_tokens=1000,
        streaming=True,
    )
    
    chain = prompt | chat
    st.session_state.chain = chain

if st.button("Clear History"):
    st.session_state.history.clear()

for message in st.session_state.history.messages:
    with st.chat_message(message.type):
        st.markdown(message.content)

if prompt := st.chat_input("Please ask me anything."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(
            st.session_state.chain.stream(
                {
                    "messages":st.session_state.history.messages,
                    "human_message":[HumanMessage(content=prompt)] ,
                },
                config={"configurable":{"session_id": st.session_state.session_id}},
            )
        )

    st.session_state.history.add_user_message(prompt)
    st.session_state.history.add_ai_message(response)