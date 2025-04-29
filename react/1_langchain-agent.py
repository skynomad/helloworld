import nest_asyncio
import streamlit as st

from bs4 import BeautifulSoup
from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_xml_agent
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage

nest_asyncio.apply()

# Function to read the contents of a web page
def web_page_reader(url: str) -> str:
    loader = WebBaseLoader(url)
    content = loader.load()[0].page_content
    return content

# Configuring Search and Web Page Readers
search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="duckduckgo-search",
        func=search.run,
        description="This tool receives search keywords from users and searches the web for the latest information. ",
    ),
    Tool(
        name="WebBaseLoader",
        func=web_page_reader,
        description="This tool returns the content text if the user passes the URL. Accepts URL strings only. ",
    ),
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
agent = create_xml_agent(chat, tools, prompt=hub.pull("hwchase17/xml-agent-convo"))
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

# Configuring the Streamlit Application
st.title("AI Agent Chat")
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