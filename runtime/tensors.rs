#[derive(Debug, Clone, PartialEq)]
pub struct Tensor { pub shape: Vec<usize>, pub data: Vec<f32> }

impl Tensor {
    pub fn new(shape: Vec<usize>, data: Vec<f32>) -> Result<Self, &'static str> {
        if shape.iter().product::<usize>() != data.len() { return Err("shape/data size mismatch"); }
        Ok(Self { shape, data })
    }
}
