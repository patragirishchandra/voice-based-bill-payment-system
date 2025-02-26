# 🏦 Voice-Based Bill Payment System

## 🚀 Introduction
The **Voice-Based Bill Payment System** is an AI-powered assistant that enables users to check and pay their bills using voice commands. It leverages **Ollama's Llama3.2 LLM**, **LangChain**, and **Whisper for Speech-to-Text (STT)** to provide a seamless, voice-driven experience.

## ✨ Features
✅ Supports multiple Indian languages.  
✅ Fetch bill details and process payments securely.  
✅ Voice input & output support using Whisper.  
✅ Interactive and user-friendly AI assistant.  
✅ Open-source and extendable architecture.  

---

## 🛠️ Installation Guide

### 🔹 Step 1: Install Ollama
1️⃣ Download **Ollama** from the official website: [Ollama Download](https://ollama.com/download/windows)  
2️⃣ Install Ollama on your system.  
3️⃣ Open Command Prompt and run the following command to install **Llama3.2**:  
   ```sh
   ollama run llama3.2
   ```
4️⃣ To exit the Ollama prompt, use:  
   ```sh
   /bye
   ```
5️⃣ To restart Ollama anytime, run:  
   ```sh
   ollama run llama3.2
   ```

### 🔹 Step 2: Install Python & Dependencies
1️⃣ Download and install **Python 3.11.10** from [Python Official Website](https://www.python.org/downloads/).  
2️⃣ Set Python in your **environment variables**.  
3️⃣ Install the required dependencies by running:  
   ```sh
   pip3 install langchain
   pip3 install pyttsx3
   pip3 install speech_recognition
   ```

### 🔹 Step 3: Clone the Project Repository
Clone this repository to your local machine:
```sh
git clone <your-repo-link>
cd voice-based-bill-payment-system
```

### 🔹 Step 4: Run the Application
Navigate to the project base directory and start the service by running:
```sh
python serviceClassLLM.py
```
📝 **Note:** `serviceClassLLM.py` is the main application that processes bill payments via voice interaction.

---

## 🎤 Usage Instructions
1️⃣ Run the app as mentioned above.  
2️⃣ Follow the voice prompts to provide bill details.  
3️⃣ Confirm payment when prompted.  
4️⃣ The AI will fetch, display, and process your bill payment securely.  

---

## 🤝 Contributions
This project is **open-source**, and contributions are welcome!  
Feel free to **create a pull request** with any improvements.  

---

## 📜 License
This project is licensed under the **MIT License**.

