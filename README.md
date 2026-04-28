# 📦 Gemini AI Agent (Function Calling + FastAPI + SQLite + Docker + Caddy)

A **production-ready AI backend** demonstrating a **multi-step Gemini agent (tool-calling loop)** with real-world integrations and infrastructure.

---

## 🚀 Tech Stack

* 🤖 Gemini API (Function Calling)
* 🚀 FastAPI
* 🗄️ SQLite
* ⚡ Redis
* 🌐 Caddy (Reverse Proxy + HTTPS)
* 🐳 Docker & Docker Compose
* 🔐 JWT Authentication
* ⚙️ GitHub Actions (CI/CD)

---

## ✨ Features

### 🤖 Multi-Step AI Agent

* Supports **tool chaining & reasoning**
* Executes multiple tools sequentially
* Example:

  ```
  user id 1 weather
  → get_user_info → extract city → get_weather → final response
  ```

---

### 🌦️ Live Weather Tool

* Real-time weather via Open-Meteo API
* Cached (TTL: 10 min)

---

### ⏰ Time Tool (IST Default)

* Timezone-aware (`Asia/Kolkata` by default)
* Cached (TTL: 1 min)

---

### 🗄️ Database Tool (SQLite)

* Fetch user data via natural language
* Cached (TTL: 5 min)

---

### ⚡ Redis Caching Layer

* Reduces latency & external API calls
* Improves performance significantly

---

### 🔌 Extensible Tool System

* Plug-and-play tool architecture
* Easily add new tools

---

### 🧠 AI Response Synthesis

* Converts raw tool output into:

  * Natural responses
  * Context-aware suggestions
  * Friendly tone + light humor

---

### 🚀 FastAPI Backend

* Clean REST API
* `/ask` → AI interaction endpoint

---

### 🔐 JWT Authentication

* Signup & Login
* Protected endpoints using Bearer tokens

---

### 🌐 Caddy Reverse Proxy

* Automatic HTTPS (local TLS)
* Reverse proxy to FastAPI
* Rate limiting support

---

### 🐳 Dockerized Architecture

* Multi-container setup:

  * FastAPI (AI Agent)
  * Redis (Cache)
  * Caddy (Proxy)

---

### ⚙️ CI/CD (GitHub Actions)

* Auto build & push Docker image
* DockerHub integration:

  ```
  dhiraj918106/gemini-ai-agent
  ```

---

## 📂 Project Structure

```bash
.
├── app/
│   ├── main.py        # FastAPI + auth routes
│   ├── agent.py       # Multi-step AI agent loop
│   ├── tools.py       # Weather, Time, DB tools
│   ├── schemas.py     # Request/response models
│   ├── auth.py        # JWT + hashing
│   ├── cache.py       # Redis layer
│
├── init_db.py
├── app.db
├── Dockerfile
├── Dockerfile.caddy
├── docker-compose.yml
├── Caddyfile
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Local Setup

### 1. Install dependencies

```bash
pip install google-genai python-dotenv fastapi uvicorn passlib python-jose redis
```

---

### 2. Configure environment

```env
GEMINI_API_KEY=your_api_key_here
JWT_SECRET=your_jwt_secret_here
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

### 3. Initialize DB

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

### Start services

```bash
docker compose up --build
```

---

### Initialize DB (first run)

```bash
docker compose run ai-agent python init_db.py
```

---

## 🌐 Access API

👉 Swagger Docs:

```
https://myapp.localhost/docs
```

👉 Trust local TLS:

```bash
docker exec -it caddy-server caddy trust
```

---

## 🔐 Authentication Flow

### Signup

```http
POST /signup
```

```json
{
  "username": "john",
  "password": "secret123"
}
```

---

### Login

```http
POST /login
```

---

### Protected Endpoint

```http
POST /ask
Authorization: Bearer <token>
```

```json
{
  "query": "weather in London"
}
```

---

## 🧪 Example Queries

```bash
weather in Delhi
time now
user id 1
user id 1 weather
```

---

## 🧠 How It Works

1. User authenticates (JWT)
2. Request hits **Caddy**

   * HTTPS
   * Rate limiting
3. Forwarded to FastAPI
4. Token verified
5. Gemini agent loop starts:

   * Understand query
   * Call tools (multi-step)
   * Chain results
6. Tools execute (API / DB / Cache)
7. Final response generated
8. Returned to user

---

## ⚡ Caching Strategy

| Tool    | TTL    |
| ------- | ------ |
| Weather | 10 min |
| Time    | 1 min  |
| User DB | 5 min  |

---

## 🎯 Use Cases

* AI Assistants
* Backend AI services
* Tool-enabled chat systems
* Internal knowledge systems

---

## 🏷️ Project Name

**gemini-ai-agent**

---
