from dataclasses import dataclass

@dataclass
class Synapse:
    source: str
    target: str
    weight: float = 1.0
    kind: str = "semantic"

    def activate(self, signal: float) -> float:
        return signal * self.weight

    def reinforce(self, reward: float, rate: float = 0.01) -> None:
        self.weight = max(-1.0, min(1.0, self.weight + rate * reward))
