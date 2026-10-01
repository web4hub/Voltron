def linear_beta_schedule(steps: int, beta_start=1e-4, beta_end=2e-2):
    if steps < 1 or not 0 < beta_start < beta_end < 1: raise ValueError("invalid diffusion schedule")
    if steps == 1: return [beta_start]
    return [beta_start + (beta_end-beta_start)*i/(steps-1) for i in range(steps)]
