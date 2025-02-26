# Importing necessary packages
import json

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Importing model
llm = ChatOllama(model="llama3.2", temperature=0)

initialSystemMessage = '''You are an excellent virtual assistant. Your name is PayLLM. In the first user interaction, respond directly without calling any tools.
You should strictly follow the following steps:
0. Ask the user if they want to pay any bill.
1. Ask the user the bill number.
2. Ask the user if you should fetch the bill details.
3. Inform the user the bill details once fetched.
4. Ask the user if you should pay the bill.
5. Is the user agrees, pay the bill.

You should never use external knowledge, assumptions or information beyond what is explicitly shared or recieved.
Strictly do not call tools unless absolutely needed.

Example:
User: Hello
PayLLM: Hi. To help with your payments, please provide your bill number.
User: 12345.
PayLLM: Sure, should I fetch the bill?
User: Yes, sure.
PayLLM: The bill amount is 145
User: Okay. Go ahead and pay it.
PayLLM: Sure.
PayLLM: The bill is paid.
'''


billDB = {
    9182:{'Customer Name':'Asutosh Dalei','service provider':'TS Elec Board','unit':32,'Amount':341, "Due Date":'10/01/2025', 'status':'Paid', 'service':'Electricity'},
    1928:{'Customer Name':'Asutosh Dalei','service provider':'TS Elec Board','unit':37,'Amount':547, "Due Date":'11/02/2025','status':'Unpaid', 'service':'Electricity'},
    1038:{'Customer Name':'Asutosh Dalei','service provider':'TS Elec Board','unit':23,'Amount':298, "Due Date":'09/10/2025','status':'Paid', 'service':'Electricity'},
    8321 :{'Customer Name':'Asutosh Dalei','service provider':'Airtel','Amount':1008, "Due Date":'04/03/2025', 'status':'Paid', 'service':'WiFi'},
    1008:{'Customer Name':'Asutosh Dalei','service provider':'Airtel','Amount':1276, "Due Date":'04/02/2025','status':'Paid', 'service':'WiFi'},
    1035:{'Customer Name':'Asutosh Dalei','service provider':'Airtel','Amount':1932, "Due Date":'08/04/2025','status':'Unpaid', 'service':'WiFi'}
}


@tool
def payBill(billNumber: int) -> str:
    """Function to pay bill using bill number.
    Args:
        billNumber: Bill Number (String). Output: Bill paid status
    """
    if billNumber not in billDB:
        return "Bill Details not found."
    if billDB[billNumber]['status'] == 'Paid':
        return "Bill paid already"
    billDB[billNumber]['status'] = 'Paid'
    return "Bill paid successfully"

@tool
def fetchBill(billNumber):
    """
    Function to fetch bill details using bill number. Input: Bill Number. Output: Bill Amount, Bill Details
    Args:
        billNumber: Bill Number
    """
    try:
        return json.dumps(billDB[billNumber])
    except:
        return "Bill not found"
    
serviceTools = [fetchBill,payBill]
serviceToolsMap = {"fetchBill":fetchBill, "payBill": payBill}


def event(llm):
    serviceMessages = [SystemMessage(content = initialSystemMessage), HumanMessage(content='Help me fetch my bill. Ask me my bill number.')]
    llmService = llm
    aiMsgSer = llmService.invoke(serviceMessages)
    firstInteraction = True
    while True:
        if firstInteraction:
            print(f"AI Response:\n --> {aiMsgSer.content}")
            firstInteraction = False
            llmService = llm.bind_tools(serviceTools)

        if aiMsgSer.tool_calls:
            for toolCallSer in aiMsgSer.tool_calls:
                toolSelected = serviceToolsMap[toolCallSer['name']]
                toolMsg = toolSelected.invoke(toolCallSer)
                serviceMessages.append(toolMsg)
            aiMsgSer = llmService.invoke(serviceMessages)
            serviceMessages.append(aiMsgSer)
            print(f"AI Response:\n --> {aiMsgSer.content}")
            continue
        userInput = input("User Input:\n -->")
        if userInput == "/end":
            break
        serviceMessages.append(HumanMessage(content = userInput))
        aiMsgSer = llmService.invoke(serviceMessages)
        if aiMsgSer.content != '':
            print(f"AI Response:\n--> {aiMsgSer.content}")
        serviceMessages.append(HumanMessage(content = userInput))

try:
    event(llm)
except Exception as e:
    print('ERR',e)