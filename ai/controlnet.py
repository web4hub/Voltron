from dataclasses import dataclass

@dataclass
class ControlSignal:
    name: str
    strength: float = 1.0

    def apply(self, feature: float) -> float:
        return feature * self.strength
