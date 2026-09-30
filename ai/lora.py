from typing import Sequence

def lora_shapes(out_dim: int, in_dim: int, rank: int, kernel: Sequence[int] | None=None):
    if rank < 1:
        raise ValueError("rank must be >= 1")
    rank=min(rank,out_dim,in_dim)
    if kernel is None:
        return (out_dim,rank),(rank,in_dim)
    return (out_dim,rank,1,1),(rank,in_dim,*kernel)
