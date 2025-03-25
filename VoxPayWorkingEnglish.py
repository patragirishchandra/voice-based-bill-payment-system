# Importing necessary packages
import base64
import hashlib
import json

import requests
import speech_recognition as sr  # Uses speech_recognition to capture user voice.
import pyttsx3  # Uses pyttsx3 to convert AI responses into speech.
from langchain.output_parsers import datetime

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech speed

# Initialize Speech Recognizer
recognizer = sr.Recognizer()

# API Configuration
API_BASE_URL = "http://localhost:8080/api/v2"
CLIENT_ID = "08ea8e5ce4a14e8096b0d758c2583c82"
AGENT_ID = "BL01BL02MBBA00000001"
HEADERS = {"Content-Type": "application/json"}


# Function to Speak Text
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to Get Voice Input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"User: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't understand.")
            return ""
        except sr.RequestError:
            print("Speech recognition service unavailable.")
            return ""


# Function to Generate a Sample Signature (Replace with actual logic)
def generate_signature(data):
    hash_object = hashlib.sha256(json.dumps(data).encode('utf-8'))
    signature = base64.b64encode(hash_object.digest()).decode('utf-8')
    return signature


# Function to Get Current Time Greeting
def get_greeting():
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 15:
        return "Good noon"
    elif 15 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


# Importing model
llm = ChatOllama(model="llama3.2", temperature=0)

# Initial System Message for PayLLM
initialSystemMessage = '''You are an excellent virtual assistant. Your name is PayLLM. In the first user interaction, respond directly without calling any tools.
You should strictly follow the following steps:
You must **refuse** any non-bill-related questions.
You should **only** handle bill-related tasks:
0. Ask the user if they want to pay any bill.
1. Ask the user the bill number.
2. Ask the user if you should fetch the bill details.
3. Inform the user the bill details once fetched.
4. Ask the user if you should pay the bill.
5. Is the user agrees, pay the bill.
7. If the user refuses at any step, ask how else you can assist them.
8. After bill fetch you should not add any **special characters** to your response.
9. When you fetch the bill, make sure to show it in the format of a conversational sentence.
10. Your response should less than 150 words.

You should never use external knowledge, assumptions or information beyond what is explicitly shared or received.
Strictly do not call tools unless absolutely needed.

Example:
User: Hello
PayLLM: Hi. I am you personal bill payment assistance. To help with your bill payments, please provide your bill category.
User: 12345.
PayLLM: Sure, should I fetch the bill?
User: Yes, sure.
PayLLM: The bill amount is 145
User: Okay. Go ahead and pay it.
PayLLM: Sure.
PayLLM: The bill is paid.
'''

# Sample Bill Database
billDB = {
    9182: {'Customer Name': 'Girish Patra', 'service provider': 'TS Elec Board', 'unit': 32, 'Amount': 341,
           "Due Date": '10/01/2025', 'status': 'Unpaid', 'service': 'Electricity'},
    1928: {'Customer Name': 'Girish Patra', 'service provider': 'TS Elec Board', 'unit': 37, 'Amount': 547,
           "Due Date": '11/02/2025', 'status': 'Unpaid', 'service': 'Electricity'},
    1038: {'Customer Name': 'Girish Patra', 'service provider': 'TS Elec Board', 'unit': 23, 'Amount': 298,
           "Due Date": '09/10/2025', 'status': 'Unpaid', 'service': 'Electricity'},
    8321: {'Customer Name': 'Girish Patra', 'service provider': 'Airtel', 'Amount': 1008, "Due Date": '04/03/2025',
           'status': 'Paid', 'service': 'WiFi'},
    1008: {'Customer Name': 'Girish Patra', 'service provider': 'Airtel', 'Amount': 1276, "Due Date": '04/02/2025',
           'status': 'Unpaid', 'service': 'WiFi'},
    1035: {'Customer Name': 'Girish Patra', 'service provider': 'Airtel', 'Amount': 1932, "Due Date": '08/04/2025',
           'status': 'Unpaid', 'service': 'WiFi'}
}


# Define tools for bill fetching and payment
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
        bill = billDB[billNumber]
        return (f"Dear {bill['Customer Name']}, your bill amount is ₹{bill['Amount']}. "
                f"The due date for payment is {bill['Due Date']}, and the current status of your bill is {bill['status']}.")
    except:
        return "Bill not found"


# Tool: Fetch Category List from API
@tool
def fetchBillerCategoryList() -> str:
    """
    Function contains information of all available services using this platform.
    """
    payload = {
        "client_id": CLIENT_ID,
        "data": {"agent_id": AGENT_ID},
        "reference_id": "AWPNSPVBPVPWDALTOMJSNBFQNOS41872263",
        "signature": generate_signature({"agent_id": AGENT_ID}),  # ✅ Generate a valid signature
        "timestamp": "2024-07-05T09:09:07+00:00",
        "ver": "1.0"
    }
    response = requests.get(f"{API_BASE_URL}/category/list", json=payload, headers=HEADERS)
    if response.status_code == 200 and response.json()["status"] == "success":
        categories = [cat["category_name"] for cat in response.json().get("categories", [])]
        return json.dumps(categories)

    return "Failed to fetch category list."

    # serviceList = {'electricity': "Pay electricity bill", 'gas': "Pay the gas bill", 'water': "Pay the water bill", 'wifi': "Pay the wifi bill"}
    # return json.dumps(serviceList)


# Tool registration
serviceTools = [fetchBill, payBill]
serviceToolsMap = {"fetchBill": fetchBill, "payBill": payBill}


# Main Event Loop
def event(llm):
    serviceMessages = [SystemMessage(content=initialSystemMessage),
                       HumanMessage(content='Help me fetch my bill. Ask me my bill number.')]

    llmService = llm
    aiMsgSer = llmService.invoke(serviceMessages)
    speak(aiMsgSer.content)  # Speak the response
    firstInteraction = True
    # Bind tools immediately
    llmService = llm.bind_tools(serviceTools)
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
                # serviceMessages.append(AIMessage(content=toolMsg))
            aiMsgSer = llmService.invoke(serviceMessages)
            serviceMessages.append(aiMsgSer)
            print(f"AI Response:\n --> {aiMsgSer.content}")
            speak(aiMsgSer.content)
            continue
        # Get User Input (Voice or Text)

        # userInput = input("User Input:\n -->")
        userInput = listen()
        if userInput.lower() in ["/end", "exit", "quit", "stop"]:
            speak("Goodbye!")
            break

        # Process User Input
        serviceMessages.append(HumanMessage(content=userInput))
        aiMsgSer = llmService.invoke(serviceMessages)
        if aiMsgSer.content != '':
            print(f"AI Response:\n--> {aiMsgSer.content}")
        serviceMessages.append(HumanMessage(content=userInput))


try:
    event(llm)
except Exception as e:
    print('ERR', e)
    speak("An error occurred. Please try again.")
