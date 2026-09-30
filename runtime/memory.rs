use std::collections::VecDeque;

#[derive(Clone, Debug)]
pub struct Memory<T> {
    capacity: usize,
    items: VecDeque<T>,
}

impl<T> Memory<T> {
    pub fn new(capacity: usize) -> Self {
        Self { capacity, items: VecDeque::with_capacity(capacity) }
    }

    pub fn push(&mut self, item: T) {
        if self.items.len() == self.capacity { self.items.pop_front(); }
        self.items.push_back(item);
    }

    pub fn len(&self) -> usize { self.items.len() }
}
