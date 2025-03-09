import random
from ndcompression import NDArray, NDShape, ShapeGenerator

def is_constant_pattern(data: list[int]) -> bool:
    first = data[0]
    return all(x == first for x in data)

def random_list(length: int, max_value: int = 255):
    return [random.randint(0, max_value) for _ in range(length)]

def main(length: int = 1000, max_value: int = 255):
    DATA = random_list(length, max_value)
    total_constant_count = 0
    total_constant_length = 0
    total_count = 0
    for shape in ShapeGenerator(length):
        ndshape = NDShape(shape)
        ndarray = NDArray(ndshape, DATA)
        for slice in ndarray.slices():
            total_count += 1
            if is_constant_pattern(slice) and len(slice) > 1:
                total_constant_count += 1
                total_constant_length += len(slice)

    print(f"Length: {length}")
    print(f"Shape Count: {len(ShapeGenerator(length))}")
    print(f"Total Slices Count: {total_count}")
    print(f"Constant Slices Count: {total_constant_count}")
    print(f"Constant Slices Total Length: {total_constant_length}")

if __name__ == "__main__":
    # main(2000, 255)
    print(list(ShapeGenerator(8)))
    print(list(NDShape([2, 2]).flat_slices()))

    