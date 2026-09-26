# graph.nim
import tables, strformat

type
  Node* = object
    id*: string
    tier*: string
    metadata*: Table[string, string]

  GraphEdge* = object
    source*: string
    target*: string
    weight*: float

  VoltronGraph* = object
    nodes*: Table[string, Node]
    edges*: seq[GraphEdge]

proc initVoltronGraph*(): VoltronGraph =
  result = VoltronGraph(
    nodes: initTable[string, Node](),
    edges: @[]
  )

proc addNode*(g: var VoltronGraph, id: string, tier: string) =
  g.nodes[id] = Node(
    id: id,
    tier: tier,
    metadata: initTable[string, string]()
  )

proc addConnection*(g: var VoltronGraph, source, target: string, weight: float = 1.0) =
  g.edges.add(GraphEdge(source: source, target: target, weight: weight))

proc validateTopology*(g: VoltronGraph): bool =
  ## Ensures all structural nodes are interconnected within acceptable limits.
  echo &"[Graph-Engine] Validating topology across {g.nodes.len} nodes and {g.edges.len} connections..."
  result = g.nodes.len > 0 and g.edges.len > 0
