import math
from collections import deque
from typing import Any

class Hippocampus:
    def __init__(self, limit: int = 128):
        if limit < 1:
            raise ValueError("limit must be positive")
        self.items = deque(maxlen=limit)

    def store(self, item: dict[str, Any]) -> None:
        self.items.append(item)

    def retrieve(self, tokens: list[str], limit: int = 8) -> list[dict[str, Any]]:
        query = set(tokens)
        scored = []
        for item in self.items:
            text = str(item).lower()
            score = sum(1 for token in query if token in text)
            scored.append((score, item))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [item for _, item in scored[:limit]]

    @staticmethod
    def similarity(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        return dot / (na * nb) if na and nb else 0.0
