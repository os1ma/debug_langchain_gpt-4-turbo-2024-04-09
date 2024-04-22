import logging

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

# logging.basicConfig(level=logging.DEBUG)

load_dotenv(override=True)

tools = [TavilySearchResults(max_results=1)]

prompt = hub.pull("hwchase17/openai-tools-agent")
model = "gpt-4-turbo-2024-04-09"
llm = ChatOpenAI(model=model, temperature=0)
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

result = agent_executor.invoke({"input": "What's the weather like in Tokyo?"})

print(result["output"])
