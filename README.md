# 📦 Gemini Weather Tool (Function Calling Demo)

A minimal Python project demonstrating **function calling using Gemini API** with a real-world example — fetching **live weather data**.

---

## 🚀 Features

* 🤖 **Gemini Function Calling**

  * The model intelligently decides when to call a function

* 🌦️ **Live Weather Data**

  * Fetches real-time temperature using Open-Meteo API

* 🔌 **Custom Tool Integration**

  * Easily plug in your own Python functions as tools

* 🔑 **Secure API Key Handling**

  * Uses `.env` with `python-dotenv`

* ⚡ **Lightweight & Minimal**

  * No frameworks, no complexity — pure Python

* 🧠 **AI-Driven Execution**

  * User query → Gemini → Tool decision → Execution → Result

---

## 📂 Project Structure

```bash
.
├── main.py
├── .env
└── README.md
```

---

## ⚙️ Setup

### 1. Install dependencies

```bash
pip install google-genai python-dotenv
```

### 2. Add your API key

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Run

```bash
python main.py
```

Example:

```bash
Ask something: weather in London
```

---

## 🧠 How It Works

1. User enters a query
2. Gemini analyzes the request
3. If needed, it triggers the `get_current_weather` function
4. The function fetches real-time data
5. Result is returned to the user

---

## 🎯 Use Case

This project is a **starting point for building AI agents**:

* AI Assistants
* Tool-enabled chatbots
* Automation systems
* Backend AI services

---

## 🚧 Future Improvements

* Multiple tools (news, currency, time)
* FastAPI integration
* Multi-step tool chaining
* Response synthesis (tool → AI → final answer)

---

