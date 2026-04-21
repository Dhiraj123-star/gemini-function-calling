from fastapi import FastAPI
from app.schemas import QueryRequest,QueryResponse
from app.agent import run_agent 

app = FastAPI(title= "AI Tool Calling API")

@app.post("/ask",response_model=QueryResponse)
def ask_ai(request:QueryRequest):
    result = run_agent(request.query)
    return QueryResponse(response=result)