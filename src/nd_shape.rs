use itertools::Itertools;
use std::collections::VecDeque;

fn generate_factorizations(number: u64) -> Vec<Vec<u64>> {
    let mut factorizations = Vec::new();
    let mut stack = VecDeque::from([(number, 2, Vec::new())]);

    while let Some((n, d, path)) = stack.pop_back() {
        let sqrt_n = (n as f64).sqrt() as u64;
        (d..=sqrt_n).filter(|&i| n % i == 0).for_each(|i| {
            let q = n / i;
            let mut new_path = path.clone();
            new_path.push(i);
            stack.push_back((q, i, new_path.clone()));
            if q >= i {
                let mut factorization = new_path.clone();
                factorization.push(q);
                factorizations.push(factorization);
            }
        });
    }
    factorizations
}

fn distinct_permutations<T: Clone + Eq + Ord>(input: &[T]) -> Vec<Vec<T>> {
    let input = input.iter().sorted().cloned().collect_vec();
    let mut result = Vec::new();
    let mut used = vec![false; input.len()];
    let mut current = Vec::with_capacity(input.len());
    permute_unique(&input, &mut used, &mut current, &mut result);
    result
}

fn permute_unique<T: Eq + Ord + Clone>(
    input: &[T],
    used: &mut [bool],
    current: &mut Vec<T>,
    result: &mut Vec<Vec<T>>,
) {
    if current.len() == input.len() {
        result.push(current.clone());
        return;
    }
    for i in 0..input.len() {
        if used[i] || (i > 0 && input[i] == input[i - 1] && !used[i - 1]) {
            continue;
        }
        if !used[i] {
            used[i] = true;
            current.push(input[i].clone());
            permute_unique(input, used, current, result);
            current.pop();
            used[i] = false;
        }
    }
}

pub fn generate_shapes(length: u64) -> Vec<Vec<u64>> {
    let factorizations = generate_factorizations(length);
    factorizations
        .into_iter()
        .flat_map(|f| distinct_permutations(&f))
        .collect()
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NDShape {
    shape: Vec<usize>,
    strides: Vec<usize>,
    len: usize,
    dimensions: usize,
}

impl NDShape {
    pub fn new(shape: Vec<usize>) -> Self {
        let dimensions = shape.len();
        let strides = Self::calculate_strides(&shape);
        let len = shape.iter().product();
        Self {
            shape,
            strides,
            len,
            dimensions,
        }
    }

    fn calculate_strides(shape: &[usize]) -> Vec<usize> {
        let mut strides = Vec::with_capacity(shape.len());
        let mut current_stride = 1;
        for &dim in shape.iter().rev() {
            strides.push(current_stride);
            current_stride *= dim;
        }
        strides.reverse();
        strides
    }

    pub fn flat_index(&self, indexes: &[usize]) -> usize {
        indexes
            .iter()
            .zip(&self.strides)
            .map(|(&i, &s)| i * s)
            .sum()
    }

    pub fn multi_index(&self, index: usize) -> Vec<usize> {
        let mut remaining = index;
        self.strides
            .iter()
            .map(|&stride| {
                let idx = remaining / stride;
                remaining %= stride;
                idx
            })
            .collect()
    }

    pub fn multi_slices(&self) -> Vec<Vec<Vec<usize>>> {
        (0..self.dimensions)
            .flat_map(|axis| {
                let axis_len = self.shape[axis];
                let ranges = self.shape
                    .iter()
                    .enumerate()
                    .filter_map(|(i, &d)| (i != axis).then(|| 0..d))
                    .collect_vec();
                
                ranges
                    .into_iter()
                    .multi_cartesian_product()
                    .map(move |indices| {
                        (0..axis_len)
                            .map(|m| {
                                let mut cloned = indices.clone();
                                cloned.insert(axis, m);
                                cloned
                            })
                            .collect_vec()
                    })
                    .collect_vec()
            })
            .collect_vec()
    }

    pub fn flat_slices(&self) -> Vec<Vec<usize>> {
        self.multi_slices()
            .into_iter()
            .map(|slice| {
                slice
                    .into_iter()
                    .map(|indices| self.flat_index(&indices))
                    .collect_vec()
            })
            .collect_vec()
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_all_shapes() {
        println!("{:?}", generate_shapes(12));
    }

    #[test]
    fn test_ndshape() {
        let nd_shape = NDShape::new(vec![2, 2]);
        println!("{:?}", nd_shape.flat_slices());
    }
}
