from typing import Any

class Perception:
    def observe(self, value: Any) -> dict[str, Any]:
        if isinstance(value, dict):
            modalities=list(value.get("modalities", []))
            signals=dict(value.get("signals", value))
        else:
            modalities=["text"] if isinstance(value, str) else ["object"]
            signals={"value": value}
        return {"modalities": modalities, "signals": signals}
