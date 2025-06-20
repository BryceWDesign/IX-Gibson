"""
IX-Gibson Domain Classifier Module

Provides a modular and extendable domain classification service
for routing queries to appropriate specialist siblings.

The current implementation uses keyword matching with
confidence scoring but can be replaced by ML models in future.
"""

from typing import Tuple

class DomainClassifier:
    """
    Classifies a query string into a domain with a confidence score.
    """

    DOMAIN_KEYWORDS = {
        "coding": ["code", "program", "python", "javascript", "algorithm", "bug", "compile"],
        "biology": ["cell", "organism", "dna", "gene", "anatomy", "medicine", "virus"],
        "physics": ["quantum", "particle", "gravity", "relativity", "force", "aerospace", "velocity"],
        "general": [],  # fallback domain
    }

    def classify(self, query: str) -> Tuple[str, float]:
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

# Example usage
if __name__ == "__main__":
    dc = DomainClassifier()
    test_queries = [
        "How do I fix a bug in my Python code?",
        "What is the function of mitochondria in a cell?",
        "Explain gravity in the context of relativity.",
        "Tell me a joke."
    ]
    for q in test_queries:
        domain, conf = dc.classify(q)
        print(f"Query: '{q}' -> Domain: {domain}, Confidence: {conf}")
