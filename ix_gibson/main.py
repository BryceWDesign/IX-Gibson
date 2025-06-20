"""
IX-Gibson CLI Entry Point

Allows users to send queries directly to IX-Gibson's orchestrator via command line.
Prints the response from the appropriate specialist sibling AI.
"""

import asyncio
import sys
from core.orchestrator import GibsonOrchestrator

async def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"Your question here\"")
        sys.exit(1)

    query = sys.argv[1]
    orchestrator = GibsonOrchestrator()
    result = await orchestrator.handle_query(query)

    print("\n🧠 IX-Gibson Response 🧠")
    if "answer" in result:
        print(f"Answer (Domain: {result.get('domain', 'unknown')} - Confidence: {result.get('confidence', 'N/A')}):\n{result['answer']}")
    elif "error" in result:
        print(f"Error: {result['error']}")
    else:
        print("No valid response received.")

if __name__ == "__main__":
    asyncio.run(main())
