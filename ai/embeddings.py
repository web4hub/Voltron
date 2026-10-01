import hashlib, math

def hash_embedding(text: str, dimensions: int = 32) -> list[float]:
    if dimensions < 1: raise ValueError("dimensions must be positive")
    values = []
    for i in range(dimensions):
        n = int.from_bytes(hashlib.sha256(f"{i}:{text}".encode()).digest()[:4], "big") / 2**32
        values.append(2*n-1)
    norm = math.sqrt(sum(v*v for v in values)) or 1.0
    return [v/norm for v in values]
