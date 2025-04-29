import streamlit as st

from openai import OpenAI
from utils.llmclient import LLMClient
from utils.chatutils import stream_response

# Get an API Key before continuing
if not st.secrets.llm.api_key or not st.secrets.llm.base_url:   
    st.error("Enter an API Key / Base Url to continue")
    st.stop()

st.title("Streamlit AI Chatbot")

##
client = LLMClient(
    api_key=st.secrets.llm.api_key,
    base_url=st.secrets.llm.base_url
)

# sets up sidebar nav widgets
with st.sidebar:
    st.subheader("LLM Settings")
    model = st.selectbox('What model would you like to use?', client.list_models())
    max_history = st.number_input("Max History", min_value=1, max_value=10, value=2, step=1)
    context_size = st.number_input("Context Size", min_value=1024, max_value=16384, value=8192, step=1024)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("What would you like to ask?"):
    # Display user prompt in chat message widget
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # adds user's prompt to session state
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("ai"):
        # Display a placeholder for the response
        response_placeholder = st.empty()
        with st.spinner('Generating response...'):
            # retrieves response from model
            system_prompt = f"""You are an AI chatbot having a conversation with a human."""
            llm_stream = client.generate_response(
                system_prompt=system_prompt, 
                user_prompt=user_prompt, 
                model=model,
                stream=True)

            # streams the response back to the screen
            stream_output = st.write_stream(stream_response(llm_stream))

        # appends response to the message list
        st.session_state.messages.append({"role": "assistant", "content": stream_output})

