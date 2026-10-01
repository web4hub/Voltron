#[derive(Debug, Default)]
pub struct Memory { items: Vec<String>, capacity: usize }

impl Memory {
    pub fn with_capacity(capacity: usize) -> Self { Self { items: Vec::new(), capacity } }
    pub fn push(&mut self, value: impl Into<String>) {
        if self.capacity == 0 { return; }
        if self.items.len() >= self.capacity { self.items.remove(0); }
        self.items.push(value.into());
    }
    pub fn len(&self) -> usize { self.items.len() }
}
