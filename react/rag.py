import os
import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import OpenAI

os.environ['OPENAI_API_KEY'] = "Enter Your API Key"

# A data set of a vertical is read as sample data. (Change to any csv, etc.)
df = pd.read_csv(
    "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv"
)

# launch an agent
agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)

# Ask questions and get answers
rep = agent.invoke("Tell me the average age of each gender in Japanese")
print(rep["output"])