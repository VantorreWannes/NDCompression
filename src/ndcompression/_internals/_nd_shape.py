class NDShape:
    def __init__(self, shape: list[int]):
        self.shape = shape
        self.strides = []
        current_stride = 1
        for dim in reversed(shape):
            self.strides.append(current_stride)
            current_stride *= dim
        self.strides = list(reversed(self.strides))
        self.len = current_stride

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