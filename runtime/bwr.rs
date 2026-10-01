mod graph;
mod memory;
mod tensors;

pub use graph::Graph;
pub use memory::Memory;
pub use tensors::Tensor;

#[derive(Debug)]
pub struct BraneworldRuntime {
    pub graph: Graph,
    pub memory_size: usize,
}

impl BraneworldRuntime {
    pub fn new(memory_capacity: usize) -> Self {
        Self { graph: Graph::default(), memory_size: memory_capacity }
    }
}
