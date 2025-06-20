"""
IX-Kate Specialist AI Server — Coding Expert

This sibling API server provides expert coding knowledge and assistance.
It inherits from the generic sibling template and overrides the query processing
to give detailed and relevant coding-related answers.

Uses FastAPI and provides asynchronous API.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import traceback

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class IXKateAI:
    domain_name = "coding"

    def process_query(self, query: str) -> str:
        """
        Implements domain-specific logic for coding queries.
        For demonstration, it uses hardcoded logic and examples.
        Replace with actual knowledge base or ML model inference.
        """
        q_lower = query.lower()
        if "python" in q_lower:
            return ("Python is a versatile programming language. "
                    "If you need help with syntax, libraries, or debugging, just ask!")
        elif "algorithm" in q_lower:
            return ("An algorithm is a step-by-step procedure for solving a problem. "
                    "Examples include sorting algorithms like quicksort and mergesort.")
        elif "bug" in q_lower:
            return ("To debug, try using print statements or a debugger like pdb in Python. "
                    "Identify where the code deviates from expected behavior.")
        else:
            # Generic fallback coding answer
            return ("I'm IX-Kate, your coding expert. Please specify your coding question "
                    "for detailed assistance.")

ix_kate_ai = IXKateAI()

@app.post("/query")
async def handle_query(request: QueryRequest):
    if not request.query or request.query.strip() == "":
        raise HTTPException(status_code=400, detail="Query must not be empty.")
    try:
        answer = ix_kate_ai.process_query(request.query)
        return {"answer": answer}
    except Exception:
        # Return error with traceback for debugging
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Server error:\n{tb}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
