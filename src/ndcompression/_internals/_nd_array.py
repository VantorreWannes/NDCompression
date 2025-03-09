import random
from ndcompression._internals._nd_shape import NDShape

class NDArray:
    def __init__(self, shape: NDShape, data: list):
        self.ndshape = shape
        self.data = data
        self.len = len(data)
        if self.len != len(self.ndshape):
            raise ValueError(
                f"Data length must match shape product. "
                f"Expected {len(self.ndshape)}, got {self.len}"
            )

    def _is_valid_index(self, index: int) -> bool:
        return index < self.len and index >= 0

    def __getitem__(self, indices: tuple[int]):
        index = self.ndshape.flat_index(indices)
        if not self._is_valid_index(index):
            raise IndexError(
                f"Index {index} out of bounds for array with length {self.len}"
            )
        return self.data[index]

    def __setitem__(self, indices: tuple[int], value):
        index = self.ndshape.flat_index(indices)
        if not self._is_valid_index(index):
            raise IndexError(
                f"Index {index} out of bounds for array with length {self.len}"
            )
        self.data[index] = value

    def slices(self):
        for slice in self.ndshape.flat_slices():
            yield [self.data[index] for index in slice]

class LinearNDArray(NDArray):
    def __init__(self, shape: NDShape):
        super().__init__(shape, range(len(shape)))

class RandomNDArray(NDArray):
    def __init__(self, shape: NDShape, max_value: int = 255):
        super().__init__(shape, [random.randint(0, max_value) for _ in range(len(shape))])