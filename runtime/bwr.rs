mod graph;
mod memory;
mod tensors;
pub use graph::Graph;
pub use memory::Memory;
pub use tensors::Tensor;

#[derive(Debug, Default)]
pub struct BraneworldRuntime { pub graph: Graph, pub memory: Memory }

impl BraneworldRuntime {
    pub fn new(capacity: usize) -> Self { Self { graph: Graph::default(), memory: Memory::with_capacity(capacity) } }
}
