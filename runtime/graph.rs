use std::collections::HashMap;

#[derive(Default, Debug)]
pub struct Graph {
    edges: HashMap<String, Vec<String>>,
}

impl Graph {
    pub fn connect(&mut self, a: impl Into<String>, b: impl Into<String>) {
        self.edges.entry(a.into()).or_default().push(b.into());
    }

    pub fn neighbors(&self, node: &str) -> &[String] {
        self.edges.get(node).map(Vec::as_slice).unwrap_or(&[])
    }
}
