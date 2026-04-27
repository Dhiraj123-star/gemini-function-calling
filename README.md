# 📦 Gemini AI Agent (Function Calling + FastAPI + SQLite + Docker + Caddy)

A **production-ready AI backend** demonstrating **multi-step Gemini function calling (agent loop)** with real-world integrations:

* 🌦️ Weather API
* ⏰ Time API
* 🗄️ SQLite Database
* ⚡ Redis Caching
* 🔐 JWT Authentication
* 🌐 Caddy Reverse Proxy (HTTPS + Rate Limiting)
* 🐳 Fully Dockerized

---

## 🚀 Features

### 🤖 AI Agent (Multi-Step Tool Calling)

* Gemini can **call multiple tools in sequence**
* Supports **reasoning + chaining**
* Example:

  * Get user → extract city → fetch weather → respond

---

### 🌦️ Live Weather Data

* Real-time weather via Open-Meteo API
* Cached for performance (10 min)

---

### ⏰ Current Time (IST Default)

* Timezone-aware (default: `Asia/Kolkata`)
* Cached for 1 minute

---

### 🗄️ SQLite Database Integration

* Fetch user data dynamically via AI queries
* Cached for 5 minutes

---

### ⚡ Redis Caching

* Reduces API calls and latency
* Improves response speed significantly

---

### 🔌 Multi-Tool Support

* Weather + Time + Database tools
* Easily extensible

---

### 🧠 AI Response Synthesis

* Tool results → Gemini → **Human-friendly output**
* Adds:

  * Context (hot/cold, suggestions)
  * Friendly tone + light humor

---

### 🚀 FastAPI Backend

* `/ask` → AI agent endpoint
* Clean REST API

---

### 🔐 JWT Authentication

* Signup + Login
* Protected endpoints with Bearer token

---

### 🌐 Caddy Reverse Proxy

* Automatic HTTPS (local TLS)
* Reverse proxy to FastAPI
* Rate limiting support

---

### 🐳 Dockerized Infrastructure

* Multi-container setup:

  * FastAPI (AI Agent)
  * Redis (Cache)
  * Caddy (Proxy)

---

## 📂 Project Structure

```bash
.
├── app/
│   ├── main.py        # FastAPI + auth routes
│   ├── agent.py       # Multi-step AI agent loop
│   ├── tools.py       # Weather, Time, DB tools
│   ├── schemas.py     # Request/response models
│   ├── auth.py        # JWT + password hashing
│   ├── cache.py       # Redis caching layer
│
├── init_db.py         # Initialize SQLite DB
├── app.db
├── Dockerfile
├── Dockerfile.caddy   # Custom Caddy (rate limit plugin)
├── docker-compose.yml
├── Caddyfile
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Setup (Local)

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

## 🌐 Access via Caddy (HTTPS)

```bash
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

👉 Returns JWT (auto-login)

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
5. Gemini agent starts loop:

   * Analyze query
   * Call tools (if needed)
   * Chain multiple tools
6. Tool execution (API / DB / Cache)
7. Final response synthesized
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
* Internal data retrieval systems

---

---

## 🏷️ Project Name

**gemini-ai-agent**

---
