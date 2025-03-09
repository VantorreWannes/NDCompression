use crate::nd_shape::NDShape;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NDArray<'a> {
    nd_shape: NDShape,
    data: &'a [u8],
}

impl<'a> NDArray<'a> {
    pub fn new(nd_shape: NDShape, data: &'a [u8]) -> Self {
        Self { nd_shape, data }
    }

    pub fn from_shape(shape: Vec<usize>, data: &'a [u8]) -> Self {
        let nd_shape = NDShape::new(shape);
        Self { nd_shape, data }
    }

    pub fn nd_shape(&self) -> &NDShape {
        &self.nd_shape
    }

    pub fn data(&self) -> &'a [u8] {
        self.data
    }

    fn is_constant_slice(&self, slice: &[u8]) -> bool {
        if let Some(&first) = slice.first() {
            return slice.iter().all(|&x| x == first);
        }
        true
    }

    pub fn multi_constant_slices(&self) -> Vec<Vec<u8>> {
        self.nd_shape
            .flat_slices()
            .iter()
            .map(|slice_indexes| {
                slice_indexes
                    .into_iter()
                    .map(|&index| self.data[index])
                    .collect::<Vec<u8>>()
            })
            .filter(|slice| self.is_constant_slice(slice))
            .collect()
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ndarray() {
        let nd_shape = NDShape::new(vec![2, 2]);
        let data = vec![0, 1, 0, 1];
        let nd_array = NDArray::new(nd_shape, &data);
        println!("{:?}", nd_array.multi_constant_slices());
    }
}