from dataclasses import dataclass, field
from typing import Any, Callable

from .cortex import Cortex
from .hippocampus import Hippocampus
from .planner import Planner
from .perception import Perception
from .reasoning import Reasoner
from .tokenizer import Tokenizer


@dataclass
class EngineConfig:
    memory_limit: int = 128
    planner_horizon: int = 4
    tools: dict[str, Callable[[dict[str, Any]], Any]] = field(default_factory=dict)


class BraneworldEngine:
    def __init__(self, config: EngineConfig | None = None):
        self.config = config or EngineConfig()
        self.perception = Perception()
        self.tokenizer = Tokenizer()
        self.cortex = Cortex()
        self.memory = Hippocampus(self.config.memory_limit)
        self.reasoner = Reasoner()
        self.planner = Planner(self.config.planner_horizon)

    def run(self, input_data: Any) -> dict[str, Any]:
        observation = self.perception.observe(input_data)
        tokens = self.tokenizer.encode(observation)
        memories = self.memory.retrieve(tokens)
        features = self.cortex.process(observation, memories)
        hypotheses = self.reasoner.infer(features, memories)
        plan = self.planner.plan(hypotheses, features)
        result = self.execute(plan)
        self.memory.store({"input": observation, "result": result, "features": features})
        return {
            "observation": observation,
            "tokens": tokens,
            "memories": memories,
            "features": features,
            "hypotheses": hypotheses,
            "plan": plan,
            "result": result,
        }

    def execute(self, plan: list[dict[str, Any]]) -> list[dict[str, Any]]:
        results = []
        for step in plan:
            action = step.get("action", "observe")
            tool = self.config.tools.get(action)
            value = tool(step) if tool else {"action": action, "status": "planned"}
            results.append({"action": action, "value": value})
        return results
