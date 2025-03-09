import random
import math
from more_itertools import peekable, spy
from ndcompression._internals._nd_array import LinearNDArray, NDArray, RandomNDArray
from ndcompression._internals._nd_shape import NDShape
from more_itertools import chunked


# Define the is_raw_pattern function
def is_raw_pattern(pattern: list[int]) -> bool:
    # For now, just return True (this function is not implemented)
    return True


# Define the print_all_patterns function
def print_all_pattern_counts(data: list[int]):
    raw_total = 0
    constant_total = 0
    incremental_total = 0
    repeating_total = 0
    for shape in all_shapes(len(data)):
        ndshape = NDShape(shape)
        ndarray = NDArray(ndshape, data)
        raw, constant, incremental, repeating = pattern_count(ndarray)
        raw_total += raw
        constant_total += constant
        incremental_total += incremental
        repeating_total += repeating

    print(f"Raw: {raw_total}")
    print(f"Constant: {constant_total}")
    print(f"Incremental: {incremental_total}")
    print(f"Repeating: {repeating_total}")

def print_all_pattern_lengths(data: list[int]):
    raw_total = 0
    constant_total = 0
    incremental_total = 0
    repeating_total = 0
    for shape in all_shapes(len(data)):
        ndshape = NDShape(shape)
        ndarray = NDArray(ndshape, data)
        raw, constant, incremental, repeating = pattern_length(ndarray)
        raw_total += raw
        constant_total += constant
        incremental_total += incremental
        repeating_total += repeating

    print(f"Raw: {raw_total}")
    print(f"Constant: {constant_total}")
    print(f"Incremental: {incremental_total}")
    print(f"Repeating: {repeating_total}")


# Define the factorize function with a base case
def factorize(N):
    if N == 1:
        return [(1,)]
    factors = [(N,)]
    for d in range(2, int(math.sqrt(N)) + 1):
        if N % d == 0:
            for sub in factorize(N // d):
                factors.append((d,) + sub)
    return factors


# Define the all_shapes function
def all_shapes(n):
    return sorted(list(set(factorize(n))))


# Define the pattern_count function with error handling
def pattern_count(ndarray: NDArray):
    raw = 0
    constant = 0
    incremental = 0
    repeating = 0
    for slice in ndarray.slices():
        if is_raw_pattern(slice):
            raw += 1
        if is_constant_pattern(slice) and len(slice) > 1:
            constant += 1
        if is_incremental_pattern(slice) and len(slice) > 2:
            incremental += 1
        if is_repeating_pattern(slice) and len(slice) > 3:
            repeating += 1
    return raw, constant, incremental, repeating


# Define the pattern_count function with error handling
def pattern_length(ndarray: NDArray):
    raw = 0
    constant = 0
    incremental = 0
    repeating = 0
    for slice in ndarray.slices():
        if is_raw_pattern(slice):
            raw += len(slice)
        if is_constant_pattern(slice) and len(slice) > 1:
            constant += len(slice)
        if is_incremental_pattern(slice) and len(slice) > 2:
            incremental += len(slice)
        if is_repeating_pattern(slice) and len(slice) > 3:
            repeating += len(slice)
    return raw, constant, incremental, repeating


# Define the random_list function with a default value
def random_list(length: int, max_value: int = 255):
    return [random.randint(0, max_value) for _ in range(length)]


# Define the is_constant_pattern function
def is_constant_pattern(values: list[int]) -> bool:
    first = values[0]
    return all(x == first for x in values)


# Define the is_incremental_pattern function
def is_incremental_pattern(values: list[int]) -> bool:
    if len(values) == 1:
        return True
    return is_constant_pattern(
        [values[i] - values[i + 1] for i in range(len(values) - 1)]
    )


# Define the is_repeating_pattern function
def is_repeating_pattern(values: list[int]) -> bool:
    length = len(values)
    divisors = get_divisors(length)
    for k in divisors:
        chunks = list(chunked(values, k))
        if all(chunk == chunks[0] for chunk in chunks):
            return True
    return False


# Define the get_divisors function
def get_divisors(n):
    divisors = set()
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.add(i)
            other = n // i
            if other != n:
                divisors.add(other)
    return sorted(divisors, reverse=True)


if __name__ == "__main__":
    DATA = random_list(3000)
    print_all_pattern_counts(DATA)
    print_all_pattern_lengths(DATA)
