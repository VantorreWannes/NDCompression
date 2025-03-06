from abc import ABC


class Pattern(ABC):
    def __init__(self, shape: list[int], direction: int, length: int):
        self.shape = shape
        self.direction = direction
        self.length = length


class RawPattern(Pattern):
    def __init__(self, shape: list[int], direction: int, length: int, data: list[int]):
        super().__init__(shape, direction, length)
        self.data = data


class IncrementalPattern(Pattern):
    def __init__(
        self,
        shape: list[int],
        direction: int,
        length: int,
        start_value: int,
        delta: int,
    ):
        super().__init__(shape, direction, length)
        self.start_value = start_value
        self.delta = delta


class ConstantPattern(Pattern):
    def __init__(self, shape: list[int], direction: int, length: int, value: int):
        super().__init__(shape, direction, length)
        self.value = value


class RepeatingPattern(Pattern):
    def __init__(
        self,
        shape: list[int],
        direction: int,
        length: int,
        pattern_length: int,
        pattern: list[int],
    ):
        super().__init__(shape, direction, length)
        self.pattern = pattern
        self.pattern_length = pattern_length
