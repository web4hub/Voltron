from dataclasses import dataclass

@dataclass
class TransformerSpec:
    hidden_size: int
    heads: int
    layers: int

    def validate(self):
        if self.hidden_size < 1 or self.heads < 1 or self.layers < 1:
            raise ValueError("transformer dimensions must be positive")
        if self.hidden_size % self.heads:
            raise ValueError("hidden_size must be divisible by heads")
        return True
