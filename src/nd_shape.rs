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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_all_shapes() {
        println!("{:?}", generate_shapes(12));
    }
}
