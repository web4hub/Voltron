from typing import Any

class Cortex:
    def process(self, observation: dict[str, Any], memories: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "modalities": sorted(observation.get("modalities", [])),
            "signals": observation.get("signals", {}),
            "memory_count": len(memories),
            "context": [m.get("result") for m in memories[-4:]],
        }
