from more_itertools import flatten, distinct_permutations

class ShapeGenerator:
    def __init__(self, length: int):
        self.length = length
        self._factorizations = self._generate_factorizations(length)
        self.shapes = list(flatten([distinct_permutations(f) for f in self._factorizations]))

    @staticmethod
    def _generate_factorizations(number: int, min_factor=2) -> list[list[int]]:
        factorizations = []
        for d in range(min_factor, int(number**0.5) + 1):
            if number % d == 0:
                q = number // d
                factorizations += [
                    [d] + sub for sub in ShapeGenerator._generate_factorizations(q, d)
                ]
                if q >= d:
                    factorizations.append([d, q])
        return factorizations

    def __iter__(self):
        return iter(self.shapes)
    
    def __len__(self):
        return len(self.shapes)
