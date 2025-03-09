use criterion::{BenchmarkId, Criterion, Throughput, criterion_group, criterion_main};
use nd_compression::nd_shape::{NDShape, generate_shapes};
use std::hint::black_box;

const LENGTHS: [usize; 5] = [10, 100, 1000, 10_000, 100_000];

const SHAPE_DIMENSIONS: [usize; 3] = [2, 5, 10];
const SHAPE_LENGTHS: [usize; 3] = [10, 25, 50];

fn bench_generate_shapes(c: &mut Criterion) {
    let mut group = c.benchmark_group("generate_shapes");

    for length in LENGTHS {
        group.throughput(Throughput::Elements(length as u64)); // Changed to Elements if appropriate
        let length = black_box(length);
        let id = BenchmarkId::new("run", format!("len{length}"));
        group.bench_function(id, |b| {
            b.iter(|| generate_shapes(length.try_into().unwrap()))
        });
    }
    group.finish();
}

fn bench_nd_shape(c: &mut Criterion) {
    let mut new_group = c.benchmark_group("NDShape::new");
    for dimensions in SHAPE_DIMENSIONS {
        for length in SHAPE_LENGTHS {
            let size = (dimensions * length) as u64;
            new_group.throughput(Throughput::Elements(size)); // Adjust if bytes are correct
            let shape = vec![length; dimensions];
            let id = BenchmarkId::from_parameter(format!("len{length}_dims{dimensions}"));
            new_group.bench_with_input(id, &shape, |b, shape| {
                b.iter(|| NDShape::new(black_box(shape.clone())))
            });
        }
    }
    new_group.finish();

    let mut slices_group = c.benchmark_group("NDShape::slices");
    for dimensions in SHAPE_DIMENSIONS {
        for length in SHAPE_LENGTHS {
            let shape = vec![length; dimensions];
            let nd_shape = NDShape::new(shape.clone());
            let size = (dimensions * length) as u64;
            
            slices_group.throughput(Throughput::Elements(size));
            let id = BenchmarkId::new("multi_slices", format!("len{length}_dims{dimensions}"));
            slices_group.bench_function(id, |b| b.iter(|| nd_shape.multi_slices()));

            let id = BenchmarkId::new("flat_slices", format!("len{length}_dims{dimensions}"));
            slices_group.bench_function(id, |b| b.iter(|| nd_shape.flat_slices()));
        }
    }
    slices_group.finish();
}

criterion_group!(benches, bench_generate_shapes, bench_nd_shape);
criterion_main!(benches);