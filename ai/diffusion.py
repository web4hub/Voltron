from dataclasses import dataclass

@dataclass
class DiffusionSchedule:
    steps: int = 20
    beta_start: float = 0.0001
    beta_end: float = 0.02

    def betas(self) -> list[float]:
        if self.steps < 1:
            raise ValueError("steps must be positive")
        if self.beta_start <= 0 or self.beta_end <= self.beta_start:
            raise ValueError("invalid beta range")
        step=(self.beta_end-self.beta_start)/(self.steps-1 or 1)
        return [self.beta_start+i*step for i in range(self.steps)]
