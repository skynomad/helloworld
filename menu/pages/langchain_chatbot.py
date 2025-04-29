import streamlit as st

from openai import OpenAI
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from utils.chatclient import ChatClient
from utils.llmclient import LLMClient
from utils.chatutils import stream_response

# Get an API Key before continuing
if not st.secrets.llm.api_key or not st.secrets.llm.base_url:   
    st.error("Enter an API Key / Base Url to continue")
    st.stop()

st.title("My AI Chatbot")

##
client = LLMClient(
    api_key=st.secrets.llm.api_key,
    base_url=st.secrets.llm.base_url,
)

# sets up sidebar nav widgets
with st.sidebar:
    st.subheader("LLM Settings")
    model = st.selectbox('What model would you like to use?', client.list_models())
    max_history = st.number_input("Max History", min_value=1, max_value=10, value=2, step=1)
    context_size = st.number_input("Context Size", min_value=1024, max_value=16384, value=8192, step=1024)

##
chatclient = ChatClient(
    api_key=st.secrets.llm.api_key,
    base_url=st.secrets.llm.base_url,
    model=model
)

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

# Set up the LangChain, passing in Message History
# You are a useful assistant. Answer all questions with {language}.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI chatbot having a conversation with a human."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | chatclient.chat_client
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="question",
    history_messages_key="history",
)

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    msgs.add_user_message(prompt)
    
# If last message is not from the AI, generate a new response
if st.session_state.langchain_messages[-1].type != "ai":
    with st.chat_message("ai"):
        #st.write(st.session_state.langchain_messages[-1].content)
        with st.spinner("Thinking..."):
            response = chatclient.get_llm_response(chain_with_history=chain_with_history, prompt=st.session_state.langchain_messages[-1].content)
        
        st.write(response)