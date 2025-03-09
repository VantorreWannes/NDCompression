pub mod nd_shape;

pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {

    use super::*;
    use prime_factorization::Factorization;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }

    #[test]
    fn factors() {
        let result = Factorization::run(12u32);
        println!("{:?}", result.factors);
    }   
}
