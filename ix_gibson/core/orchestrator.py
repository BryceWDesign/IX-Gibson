"""
IX-Gibson Orchestrator Core - Specialist Domain Routing Edition

This orchestrator routes queries dynamically to domain-specialist sibling AI nodes based on
query classification. Each sibling represents an expert in a domain (e.g. coding, biology, physics).
Gibson directs questions only to the relevant expert to improve answer quality, reduce conflicts,
and increase response speed.

Features:
- Lightweight domain classifier using keyword-based or ML model (stub here for now)
- Directed query routing to specialist sibling(s)
- Fallback to generalist sibling if classification confidence low or unknown domain
- Aggregation logic mainly passthrough but can be extended for multi-domain queries
"""

import asyncio
import aiohttp
from typing import Dict, Tuple

class DomainClassifier:
    """
    Stub classifier that assigns a domain label based on simple keyword matching.
    Replace or extend with ML-based intent classification for production.
    """
    DOMAIN_KEYWORDS = {
        "coding": ["code", "program", "python", "javascript", "algorithm", "bug", "compile"],
        "biology": ["cell", "organism", "dna", "gene", "anatomy", "medicine", "virus"],
        "physics": ["quantum", "particle", "gravity", "relativity", "force", "aerospace", "velocity"],
        "general": [],  # Default fallback domain
    }

    def classify(self, query: str) -> Tuple[str, float]:
        """
        Returns domain label and confidence score (0.0 to 1.0).
        Simple keyword matching counts matches normalized by length.
        """
        query_lower = query.lower()
        scores = {}
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            if not keywords:
                continue
            count = sum(query_lower.count(kw) for kw in keywords)
            scores[domain] = count / max(len(keywords), 1)
        if not scores:
            return "general", 1.0
        best_domain = max(scores, key=scores.get)
        confidence = scores[best_domain]
        if confidence == 0:
            return "general", 0.5
        return best_domain, min(confidence, 1.0)

class GibsonOrchestrator:
    """
    Main orchestrator class for IX-Gibson.
    """

    # Map domain labels to sibling API URLs
    DOMAIN_SIBLINGS = {
        "coding": "http://localhost:8002",       # IX-Kate
        "biology": "http://localhost:8003",      # IX-Dade
        "physics": "http://localhost:8004",      # IX-Paul
        "general": "http://localhost:8001",      # IX-Joey (generalist fallback)
        # Extend this dict as you add more specialists
    }

    def __init__(self):
        self.classifier = DomainClassifier()

    async def _query_sibling(self, session: aiohttp.ClientSession, url: str, query: str) -> Dict:
        try:
            async with session.post(f"{url}/query", json={"query": query}, timeout=5) as resp:
                if resp.status == 200:
                    return await resp.json()
                return {"error": f"{url} responded with status {resp.status}"}
        except Exception as e:
            return {"error": f"{url} failed: {str(e)}"}

    async def route_query(self, query: str) -> Dict:
        """
        Classify the domain and route query to the correct sibling.
        Falls back to generalist sibling if domain confidence is low or domain unknown.
        """
        domain, confidence = self.classifier.classify(query)
        # Threshold confidence below which fallback is used
        CONFIDENCE_THRESHOLD = 0.3

        if domain not in self.DOMAIN_SIBLINGS or confidence < CONFIDENCE_THRESHOLD:
            domain = "general"

        sibling_url = self.DOMAIN_SIBLINGS.get(domain)
        async with aiohttp.ClientSession() as session:
            response = await self._query_sibling(session, sibling_url, query)
        # Tag response with domain info for tracing/debugging
        if "answer" in response:
            response["domain"] = domain
            response["confidence"] = confidence
        return response

    async def handle_query(self, query: str) -> Dict:
        """
        Public entry to handle incoming query.
        """
        return await self.route_query(query)

# Manual test
if __name__ == "__main__":
    import sys
    import asyncio

    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py \"Your query here\"")
        sys.exit(1)

    test_query = sys.argv[1]
    orchestrator = GibsonOrchestrator()

    result = asyncio.run(orchestrator.handle_query(test_query))
    print("Response:", result)
