# Importing necessary packages
import json

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

memory = MemorySaver()
model = ChatOllama(model="llama3.2", temperature=0)

def search(city):
    '''
    Tells the temperature of a input city.
    '''
    if city == 'Hyderabad':
        return 32
    else:
        return "temperature is 43 Celcius"
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}
for step in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in sf")]},
    config,
    stream_mode="values",
):
    step["messages"][-1].pretty_print()

for step in agent_executor.stream({"messages": [HumanMessage(content="whats the weather where I live?")]},config,stream_mode="values"):
    step["messages"][-1].pretty_print()