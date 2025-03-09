from more_itertools import distinct_permutations, flatten


class ShapeGenerator:
    def __init__(self, length: int):
        self.length = length
        self._factorizations = self._generate_factorizations(length)
        self.shapes = list(
            flatten([distinct_permutations(f) for f in self._factorizations])
        )

    @staticmethod
    def _generate_factorizations(number: int, min_factor=2) -> list[list[int]]:
        factorizations = []
        stack = [(number, min_factor, [])]
        while stack:
            n, d, path = stack.pop()
            for i in range(d, int(n**0.5) + 1):
                if n % i == 0:
                    q = n // i
                    stack.append((q, i, path + [i]))
                    if q >= i:
                        factorizations.append(path + [i, q])
        return factorizations

    def __iter__(self):
        return iter(self.shapes)

    def __len__(self):
        return len(self.shapes)
