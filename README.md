# 📦 Gemini AI Agent (Function Calling + FastAPI + SQLite + Docker)

A minimal yet production-ready Python project demonstrating **Gemini function calling** with:

* 🌦️ Weather API
* ⏰ Time API
* 🗄️ SQLite Database
* 🚀 FastAPI backend
* 🐳 Dockerized setup

---

## 🚀 Features

* 🤖 **Gemini Function Calling**

  * AI decides when to call tools automatically

* 🌦️ **Live Weather Data**

  * Fetches real-time weather using Open-Meteo API

* ⏰ **Current Time (IST Default)**

  * Retrieves timezone-based time (defaults to Asia/Kolkata)

* 🗄️ **SQLite Database Integration**

  * Fetch user data using AI-powered queries

* 🔌 **Multi-Tool Support**

  * Weather + Time + Database tools

* 🧠 **AI Response Synthesis**

  * Tool results → Gemini → Human-friendly response

* 🚀 **FastAPI Endpoint**

  * Exposes AI agent via `/ask` API

* 🐳 **Docker Support**

  * Fully containerized for easy deployment

* 🔑 **Secure API Key Handling**

  * Uses `.env` with `python-dotenv`

---

## 📂 Project Structure

```bash
.
├── app/
│   ├── main.py        # FastAPI entrypoint
│   ├── agent.py       # Gemini + tool calling logic
│   ├── tools.py       # All tool functions
│   ├── schemas.py     # Request/response models
│
├── init_db.py         # Initialize SQLite DB
├── app.db
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Setup (Local)

### 1. Install dependencies

```bash
pip install google-genai python-dotenv fastapi uvicorn
```

---

### 2. Add your API key

```env
GEMINI_API_KEY=your_api_key_here
```

---

### 3. Initialize database

```bash
python init_db.py
```

---

### 4. Run API

```bash
uvicorn app.main:app --reload
```

---

## 🐳 Run with Docker

### Build & Start

```bash
docker compose up --build
```

---

### Initialize DB (first time only)

```bash
docker compose run ai-agent python init_db.py
```

---

### Access API

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Test API

### Endpoint:

```bash
POST /ask
```

### Request:

```json
{
  "query": "weather in London"
}
```

---

### Example Queries:

```bash
weather in Delhi
time now
user id 1
```

---

## 🧠 How It Works

1. User sends query to FastAPI
2. Gemini analyzes intent
3. Decides whether to call a tool
4. Tool executes (API / DB)
5. Result sent back to Gemini
6. Gemini generates final response

---

## 🎯 Use Cases

* AI Assistants
* Backend AI services
* Tool-enabled chat systems
* Internal data retrieval systems

---

## 🚧 Future Improvements

* Redis caching
* Authentication (JWT)
* Async tool execution
* Multi-step agent loop
* Vector search (RAG)

---

## 🏷️ Project Name

**gemini-ai-agent**

---
