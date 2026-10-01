from dataclasses import dataclass

@dataclass(frozen=True)
class TransformerSpec:
    hidden_size: int = 768
    heads: int = 12
    layers: int = 12
    def __post_init__(self):
        if min(self.hidden_size, self.heads, self.layers) < 1 or self.hidden_size % self.heads:
            raise ValueError("invalid transformer dimensions")
    @property
    def head_dim(self): return self.hidden_size // self.heads
