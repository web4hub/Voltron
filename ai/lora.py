from typing import Sequence

def lora_shapes(out_dim: int, in_dim: int, rank: int, kernel: Sequence[int] | None = None):
    if min(out_dim, in_dim, rank) < 1: raise ValueError("dimensions and rank must be positive")
    rank = min(rank, out_dim, in_dim)
    return ((out_dim, rank), (rank, in_dim)) if kernel is None else ((out_dim, rank, 1, 1), (rank, in_dim, *kernel))
