use std::collections::HashMap;

#[derive(Debug, Default)]
pub struct Graph { edges: HashMap<String, Vec<String>> }

impl Graph {
    pub fn connect(&mut self, a: impl Into<String>, b: impl Into<String>) {
        let (a,b)=(a.into(),b.into());
        self.edges.entry(a.clone()).or_default().push(b.clone());
        self.edges.entry(b).or_default().push(a);
    }
    pub fn neighbors(&self, node: &str) -> &[String] {
        self.edges.get(node).map(Vec::as_slice).unwrap_or(&[])
    }
}
