# ix_gibson/core/orchestrator.py

"""
IX-Gibson Orchestrator Core

The master orchestrator for the IX-AI family. This module sends queries to sibling AI nodes,
aggregates their responses, and forms a unified result. Siblings are expected to expose a
'/query' API endpoint that accepts a JSON body: {"query": "your question here"} and responds
with: {"answer": "response from sibling"}.
"""

import asyncio
import aiohttp
from typing import List, Dict, Optional
from collections import Counter

class GibsonOrchestrator:
    def __init__(self, sibling_urls: List[str]):
        """
        Initialize the orchestrator with a list of sibling node URLs.
        Example: ["http://localhost:8001", "http://localhost:8002"]
        """
        self.siblings = sibling_urls

    async def _query_sibling(self, session: aiohttp.ClientSession, url: str, query: str) -> Dict:
        try:
            async with session.post(f"{url}/query", json={"query": query}, timeout=5) as resp:
                if resp.status == 200:
                    return await resp.json()
                return {"error": f"{url} responded with status {resp.status}"}
        except Exception as e:
            return {"error": f"{url} failed: {str(e)}"}

    async def broadcast_query(self, query: str) -> List[Dict]:
        """
        Send a query to all sibling nodes and gather their responses.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self._query_sibling(session, url, query) for url in self.siblings]
            return await asyncio.gather(*tasks)

    def aggregate_responses(self, responses: List[Dict]) -> Dict:
        """
        Aggregate all sibling responses into a final answer.
        Currently uses majority vote if possible.
        """
        valid_answers = [r["answer"] for r in responses if "answer" in r]
        errors = [r["error"] for r in responses if "error" in r]

        if not valid_answers:
            return {
                "answer": None,
                "errors": errors,
                "status": "no valid responses"
            }

        common = Counter(valid_answers).most_common(1)[0]
        return {
            "answer": common[0],
            "confidence": common[1] / len(valid_answers),
            "votes": dict(Counter(valid_answers)),
            "errors": errors,
            "status": "aggregated"
        }

    async def handle_query(self, query: str) -> Dict:
        """
        Main entry point to handle a user query.
        Sends to siblings and aggregates results.
        """
        responses = await self.broadcast_query(query)
        return self.aggregate_responses(responses)
