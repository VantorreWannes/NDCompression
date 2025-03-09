use criterion::{BenchmarkId, Criterion, Throughput, criterion_group, criterion_main};
use nd_compression::nd_shape::generate_shapes;
use std::hint::black_box;

const LENGTHS: [usize; 5] = [10, 100, 1000, 10_000, 100_000];

fn bench_generate_shapes(c: &mut Criterion) {
    let mut group = c.benchmark_group("generate_shapes");

    for length in LENGTHS {
        group.throughput(Throughput::Bytes(length as u64));
        let length = black_box(length);
        let id = BenchmarkId::new("AI Generate Shapes", format!("n={length}"));
        group.bench_function(id, |b| b.iter(|| generate_shapes(length.try_into().unwrap())));
    }
    group.finish();
}

criterion_group!(benches, bench_generate_shapes);
criterion_main!(benches);
