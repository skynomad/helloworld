import nest_asyncio
import streamlit as st
from bs4 import BeautifulSoup
from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage

nest_asyncio.apply()

search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="duckduckgo-search",
        func=search.run,
        description="This tool receives search keywords from users and searches the web for the latest information. ",
    )
]

# Configuring Chat Models
chat = ChatOpenAI(
    api_key=st.secrets.llm.api_key,
    base_url=st.secrets.llm.base_url,
    model="llama3.2:3b-instruct-fp16",
    temperature=0,
    max_tokens=1000,
)

# Agent Configuration
agent = create_react_agent(chat, tools, prompt=hub.pull("hwchase17/react"))
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

# Configuring the Streamlit Application
st.title("Bedrock ReAct Agent Chat")
messages = [SystemMessage(content="You always answer questions in Japanese. ")]

# User Input Processing
prompt = st.chat_input("Ask me anything. ")
if prompt:
    messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # call an agent
        result = agent_executor.invoke({"input": prompt})
        st.write(result["output"])