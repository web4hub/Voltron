class Planner:
    def __init__(self, horizon: int = 4):
        self.horizon = max(1, int(horizon))

    def plan(self, hypotheses: list[dict], features: dict) -> list[dict]:
        actions = []
        for hypothesis in hypotheses[:self.horizon]:
            actions.append({
                "action": hypothesis.get("action", "observe"),
                "reason": hypothesis.get("reason", "default"),
                "confidence": float(hypothesis.get("confidence", 0.0)),
            })
        return actions or [{"action": "observe", "reason": "no hypothesis", "confidence": 0.0}]
