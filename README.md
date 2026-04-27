# 📦 Gemini AI Agent (Function Calling + FastAPI + SQLite + Docker + Caddy)

A minimal yet **production-ready AI backend** demonstrating **Gemini function calling** with:

* 🌦️ Weather API
* ⏰ Time API
* 🗄️ SQLite Database
* 🚀 FastAPI backend
* 🐳 Dockerized setup
* 🔐 JWT Authentication (Signup + Login)
* ⚡ Redis Caching
* 🌐 Caddy Reverse Proxy (HTTPS + Rate Limiting)

---

## 🚀 Features

* 🤖 **Gemini Function Calling**

  * AI intelligently decides when to call tools

* 🌦️ **Live Weather Data**

  * Real-time weather via Open-Meteo API

* ⏰ **Current Time (IST Default)**

  * Timezone-based time (default: Asia/Kolkata)

* 🗄️ **SQLite Database Integration**

  * Fetch user data via AI queries

* ⚡ **Redis Caching**

  * Caches weather, time, and DB responses for performance

* 🔌 **Multi-Tool Support**

  * Weather + Time + Database tools

* 🧠 **AI Response Synthesis**

  * Tool → Gemini → Human-friendly response

* 🚀 **FastAPI Endpoint**

  * `/ask` endpoint for AI interaction

* 🔐 **JWT Authentication**

  * Signup, login, and protected routes

* 🌐 **Caddy Reverse Proxy**

  * Automatic HTTPS (local TLS)
  * Auth header enforcement
  * Rate limiting at edge

* 🐳 **Dockerized Infrastructure**

  * Multi-service setup (FastAPI + Redis + Caddy)

---

## 📂 Project Structure

```bash
.
├── app/
│   ├── main.py        # FastAPI entrypoint + auth routes
│   ├── agent.py       # Gemini + tool calling logic
│   ├── tools.py       # Tool functions (weather, time, DB)
│   ├── schemas.py     # Request/response models
│   ├── auth.py        # JWT + password hashing
│   ├── cache.py       # Redis caching layer
│
├── init_db.py         # Initialize SQLite DB
├── app.db
├── Dockerfile
├── Dockerfile.caddy   # Custom Caddy build (rate limit plugin)
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

### 2. Add environment variables

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

👉 Run once to trust local TLS:

```bash
docker exec -it caddy-server caddy trust
```

---

## 🔐 Authentication Flow

### 1. Signup

```bash
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

### 2. Login

```bash
POST /login
```

---

### 3. Use Protected Endpoint

```bash
POST /ask
Authorization: Bearer <token>
```

---

## 🧪 Example Queries

```bash
weather in Delhi
time now
user id 1
```

---

## 🧠 How It Works

1. User signs up → password hashed → JWT issued
2. Request hits **Caddy**

   * Auth header check
   * Rate limiting
3. Request forwarded to FastAPI
4. Token verified
5. Gemini analyzes query
6. Calls tool if needed
7. Tool executes (API / DB / Cache)
8. Response synthesized and returned

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

## 🚧 Future Improvements

* Async tool execution
* Multi-step agent loop
* Vector search (RAG)
* PostgreSQL + persistent users
* Observability (Prometheus + Grafana)
* Per-user rate limiting

---

## 🏷️ Project Name

**gemini-ai-agent**

---