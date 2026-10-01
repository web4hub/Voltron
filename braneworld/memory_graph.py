from dataclasses import dataclass, field

@dataclass
class MemoryNode:
    id: str
    value: object
    edges: set[str] = field(default_factory=set)

class MemoryGraph:
    def __init__(self):
        self.nodes: dict[str, MemoryNode] = {}

    def add(self, node_id: str, value: object) -> MemoryNode:
        node = self.nodes.setdefault(node_id, MemoryNode(node_id, value))
        node.value = value
        return node

    def connect(self, a: str, b: str) -> None:
        self.add(a, None).edges.add(b)
        self.add(b, None).edges.add(a)

    def neighbors(self, node_id: str) -> list[MemoryNode]:
        node = self.nodes.get(node_id)
        return [self.nodes[n] for n in node.edges] if node else []
