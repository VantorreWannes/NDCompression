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
        rows_template = self.__rows_template()
        for shape_index, length in enumerate(self.shape):
            num_rows = math.prod(self.shape) // length
            for row in itertools.islice(rows_template, num_rows):
                for length_index, indecies in enumerate(row):
                    indecies = list(indecies)
                    indecies[shape_index] = length_index
                    row[length_index] = tuple(indecies)
                yield row

    def __trimmed_shape(self):
        for shape_index in range(len(self.shape)):
            yield [
                1 if i == shape_index else self.shape[i] for i in range(len(self.shape))
            ]

    def __column_parts(self):
        for column in self.__trimmed_shape():
            yield itertools.product(*[range(length) for length in column])

    def __column(self):
        for column in itertools.chain(*self.__column_parts()):
            yield tuple(column)

    def __rows_template(self):
        column = self.__column()
        for length in self.shape:
            for _ in range((math.prod(self.shape) // length)):
                yield list(itertools.repeat(next(column), length))

    def __len__(self):
        return self.len
