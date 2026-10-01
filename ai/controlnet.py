def condition(signal, strength: float = 1.0):
    if strength < 0: raise ValueError("strength must be non-negative")
    return {"signal": signal, "strength": float(strength)}
