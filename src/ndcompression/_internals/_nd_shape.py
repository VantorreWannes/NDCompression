import itertools
import math


class NDShape:
    def __init__(self, shape: list[int]):
        self.shape = shape
        self.strides = self.calculate_strides(shape)
        self.len = math.prod(self.shape)

    @staticmethod
    def calculate_strides(shape: list[int]) -> list[int]:
        strides = []
        current_stride = 1
        for dim in reversed(shape):
            strides.append(current_stride)
            current_stride *= dim
        return list(reversed(strides))

    def flat_index(self, indexes: list[int]) -> int:
        return sum(index * stride for index, stride in zip(indexes, self.strides))

    def multi_index(self, index: int) -> list[int]:
        remaining = index
        indices = []
        for stride in self.strides:
            indices.append(remaining // stride)
            remaining %= stride
        return indices
    
    def slices(self):
        n = len(self.shape)
        for axis in range(n):
            other_axes = [i for i in range(n) if i != axis]
            other_dims = [self.shape[i] for i in other_axes]
            ranges = [range(dim) for dim in other_dims]
            for fixed_indices in itertools.product(*ranges):
                line = []
                for m in range(self.shape[axis]):
                    index = [0] * n
                    for i, pos in enumerate(other_axes):
                        index[pos] = fixed_indices[i]
                    index[axis] = m
                    line.append(index)
                yield line

    def __len__(self):
        return self.len
