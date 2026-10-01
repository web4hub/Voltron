import math
from collections import deque
from typing import Any

class Hippocampus:
    def __init__(self, limit: int = 128):
        self.items = deque(maxlen=limit)

    def store(self, item: dict[str, Any]) -> None:
        self.items.append(item)

    def retrieve(self, tokens: list[str], limit: int = 8) -> list[dict[str, Any]]:
        query=set(tokens)
        scored=[]
        for item in self.items:
            text=str(item).lower()
            score=sum(1 for t in query if t in text)
            scored.append((score, item))
        scored.sort(key=lambda x:x[0], reverse=True)
        return [item for _, item in scored[:limit]]

    def similarity(self, a: list[float], b: list[float]) -> float:
        dot=sum(x*y for x,y in zip(a,b))
        na=math.sqrt(sum(x*x for x in a))
        nb=math.sqrt(sum(y*y for y in b))
        return dot/(na*nb) if na and nb else 0.0
