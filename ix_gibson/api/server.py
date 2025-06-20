"""
IX-Gibson REST API Server

Provides an HTTP API endpoint to accept user queries and forward them to the orchestrator.
Uses FastAPI for async web server with JSON request/response.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio
from core.orchestrator import GibsonOrchestrator

app = FastAPI()
orchestrator = GibsonOrchestrator()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_handler(request: QueryRequest):
    if not request.query or request.query.strip() == "":
        raise HTTPException(status_code=400, detail="Query must not be empty.")
    try:
        response = await orchestrator.handle_query(request.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    # Run server on localhost:8000 by default
    uvicorn.run(app, host="127.0.0.1", port=8000)
