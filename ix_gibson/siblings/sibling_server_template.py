"""
Generic Sibling AI API Server Template

This server template is designed for specialist sibling repos (e.g., IX-Kate, IX-Dade).
It listens for query requests from IX-Gibson orchestrator and returns domain-specific answers.

Each sibling instance should customize the `process_query` method with
its domain expertise logic.

Uses FastAPI for async API handling.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class SiblingAI:
    """
    Base class for sibling AI domain experts.
    """

    domain_name = "generic"

    def process_query(self, query: str) -> str:
        """
        Override this method to implement domain-specific query handling logic.
        For now, returns a stub response.
        """
        return f"[{self.domain_name} AI] Response to query: '{query}'"

sibling_ai = SiblingAI()

@app.post("/query")
async def handle_query(request: QueryRequest):
    if not request.query or request.query.strip() == "":
        raise HTTPException(status_code=400, detail="Query must not be empty.")
    try:
        answer = sibling_ai.process_query(request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
