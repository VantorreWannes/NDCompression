import itertools
from ndcompression import NDShape

def example_slices(dimensions):
    slices = []
    n = len(dimensions)
    for axis in range(n):
        other_axes = [i for i in range(n) if i != axis]
        other_dims = [dimensions[i] for i in other_axes]
        ranges = [range(dim) for dim in other_dims]
        for fixed_indices in itertools.product(*ranges):
            line = []
            for m in range(dimensions[axis]):
                index = [0] * n
                for i, pos in enumerate(other_axes):
                    index[pos] = fixed_indices[i]
                index[axis] = m
                line.append(tuple(index))
            slices.append(line)
    return slices

if __name__ == "__main__":
    SHAPE = [3, 3]
    NDSHAPE = NDShape(SHAPE)
    for row in NDSHAPE.slices():
        print(list(row))
