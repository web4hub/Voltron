#[derive(Clone, Debug)]
pub struct Tensor {
    pub shape: Vec<usize>,
    pub data: Vec<f32>,
}

impl Tensor {
    pub fn new(shape: Vec<usize>, data: Vec<f32>) -> Result<Self, String> {
        let expected: usize = shape.iter().product();
        if expected != data.len() {
            return Err("tensor data does not match shape".into());
        }
        Ok(Self { shape, data })
    }

    pub fn len(&self) -> usize { self.data.len() }
}
