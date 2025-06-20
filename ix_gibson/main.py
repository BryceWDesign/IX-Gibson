# ix_gibson/main.py

"""
IX-Gibson CLI Entry Point

This script serves as a simple command-line interface for sending a query to the Gibson
Orchestrator and printing the aggregated response from sibling AI nodes.
"""

import asyncio
import sys
from core.orchestrator import GibsonOrchestrator

# Define the URLs for all sibling AI nodes
SIBLING_URLS = [
    "http://localhost:8001",  # IX-Joey
    "http://localhost:8002",  # IX-Dade
    "http://localhost:8003",  # IX-Kate
    "http://localhost:8004",  # IX-CrashOverride
    "http://localhost:8005",  # IX-ZeroCool
    "http://localhost:8006",  # IX-AcidBurn
    "http://localhost:8007",  # IX-CerealKiller
    "http://localhost:8008",  # IX-LordNikon
    "http://localhost:8009",  # IX-PhantomPhreak
    "http://localhost:8010",  # IX-ThePlague
]

async def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"Your question here\"")
        sys.exit(1)

    query = sys.argv[1]
    orchestrator = GibsonOrchestrator(SIBLING_URLS)
    result = await orchestrator.handle_query(query)

    print("\n🧠 Gibson AI Aggregated Response 🧠")
    print(f"Final Answer: {result.get('answer')}")
    print(f"Confidence: {result.get('confidence', 'N/A')}")
    print(f"Votes: {result.get('votes', {})}")
    if result.get("errors"):
        print("\nSibling Errors:")
        for err in result["errors"]:
            print(f" - {err}")

if __name__ == "__main__":
    asyncio.run(main())
