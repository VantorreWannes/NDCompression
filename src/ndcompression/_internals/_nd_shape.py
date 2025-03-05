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

    def __len__(self):
        return self.len
