from typing import Any

class Reasoner:
    def infer(self, features: dict[str, Any], memories: list[dict[str, Any]]) -> list[dict[str, Any]]:
        context=features.get("context", [])
        if context:
            return [{"action":"retrieve", "reason":"context available", "confidence":0.75}]
        if features.get("signals"):
            return [{"action":"observe", "reason":"new signal requires grounding", "confidence":0.60}]
        return [{"action":"observe", "reason":"empty perception", "confidence":0.20}]
