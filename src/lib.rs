use bitvec::{bitvec, vec::BitVec};
use nd_shape::{NDShape, generate_shapes};

pub mod nd_array;
pub mod nd_shape;

pub fn normalise(data: &[u8]) -> (BitVec, Vec<u8>) {
    let mut normalised_data = data.to_vec();
    let mut bitmap = bitvec![1; normalised_data.len()];
    let shapes = generate_shapes(normalised_data.len());

    for shape in shapes {
        let nd_shape = NDShape::new(shape);
        let nd_array = nd_array::NDArray::new(nd_shape, data);

        for slice in nd_array.flat_constant_slices() {
            for index in slice.into_iter().skip(1) {
                bitmap.set(index, false);
                normalised_data[index] = 0;
            }
        }
    }

    (bitmap, normalised_data)
}

#[cfg(test)]
mod tests {

    use rand::{
        distr::{Distribution, Uniform},
        rng,
    };

    use super::*;

    fn generate_random_data(length: usize, alphabet_size: u8) -> Vec<u8> {
        let mut rng = rng();
        let die = Uniform::try_from(1..=alphabet_size+1).unwrap();
        die.sample_iter(&mut rng).take(length).collect()
    }

    #[test]
    fn test_example_normalise() {
        let data = vec![0, 1, 0, 1, 2, 3, 2, 3];
        let (bitmap, normalised_data) = normalise(&data);
        println!("{:?}", bitmap);
        println!("{:?}", normalised_data);
    }

    #[test]
    fn test_normalise() {
        let data = generate_random_data(5100, 4);
        let (_, normalised_data) = normalise(&data);
        let normalised_count = normalised_data.iter().filter(|&x| *x == 0).count();
        // println!("{:?}", bitmap);
        // println!("{:?}", normalised_data);
        println!("{:?}", data.len());
        println!("{:?}", normalised_count);
    }
}
