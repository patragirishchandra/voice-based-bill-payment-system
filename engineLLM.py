# Importing necessary packages
import json

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Importing model
llm = ChatOllama(model="llama3.2", temperature=0)



# Creating Tools
@tool
def fetchUserDetails() -> str:
    """
    Function contains the information about the user. Returns information such as user name, account holder status, amazon id.
    """
    userDetails = '''User Name: Girish Chandra Patra, Account Status: Active, Amazon ID: 12345'''
    userDetails = {'user_name':"Girish Chandra Patra", "account_status":"Active", "amazon_id": 12345}

    return json.dumps(userDetails)

@tool
def fetchServiceList() -> str:
    """
    Function contains information of all available services using this platform.
    """
    serviceList = {'electricity':"Pay electricity bill", 'gas':"Pay the gas bill", 'water':"Pay the water bill", 'wifi':"Pay the wifi bill"}
    return json.dumps(serviceList)

@tool
def payElectricityBill():
    """
    Tool to handle all electricity bill related payments.
    """
    print("entered here")
    # elecBillPay.event()
    return "electricity bill paid: 572 rupees."


tools = [fetchUserDetails, fetchServiceList, payElectricityBill]
toolsMap = {'fetchUserDetails':fetchUserDetails, "fetchServiceList":fetchServiceList, "payElectricityBill":payElectricityBill}

llm = llm.bind_tools(tools)

# Central session messages
global messages
# messages = [SystemMessage(content = "You are a helpful bill payment assistant for a user. Start by greeting the user.")]
messages = [SystemMessage(content = "You are a helpful bill payment assistant for a user. Restrict your response to just this task, nothing else. Strictly start by asking the user about the bill number. Followed by asking if you should fetch the bill or not. Followed by asking if you shoud pay the bill or not.")]


aiMsg = llm.invoke(messages)
messages.append(aiMsg)

while True:
    if aiMsg.tool_calls:
        for toolCall in aiMsg.tool_calls:
            toolSelected = toolsMap[toolCall['name']]
            toolMsg = toolSelected.invoke(toolCall)
            messages.append(toolMsg)
        aiMsg = llm.invoke(messages)
        messages.append(aiMsg)
        print(f"AI Response:\n--> {aiMsg.content}")
        continue
    
    # Text/Voice
    userInput = input("User Input:\n -->")

    if userInput == '/end':
        break
    if userInput == '/clear':
        messages = [SystemMessage(content = "You are a helpful bill payment assistant for a user. Do not hallucinate. Restrict yourself to information that you know of for sure onlt. Start by greeting the user.")]
        aiMsg = llm.invoke(messages)
        messages.append(aiMsg)
        continue

    messages.append(HumanMessage(content=userInput))
    aiMsg = llm.invoke(messages)
    if aiMsg.content != '':
        print(f"AI Response:\n--> {aiMsg.content}")
    messages.append(aiMsg)

    # print(messages)