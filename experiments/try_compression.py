from copy import deepcopy
import random
from ndcompression import NDShape, ShapeGenerator

def random_list(length: int, max_value: int = 255):
    return [random.randint(0, max_value) for _ in range(length)]

def is_constant_pattern(data: list[int]) -> bool:
    first = data[0]
    return all(x == first for x in data)


def all_slices(data_length: int):
    for shape in ShapeGenerator(data_length):
        ndshape = NDShape(shape)
        for slice in ndshape.flat_slices():
            if len(slice) > 1:
                yield slice


def all_constant_slices(data: list[int]):
    for shape in ShapeGenerator(len(data)):
        ndshape = NDShape(shape)
        for slice in ndshape.flat_slices():
            slice_data = [data[index] for index in slice]
            if is_constant_pattern(slice_data) and len(slice_data) > 1:
                yield slice


def inital_bitmap(length: int):
    return [True for _ in range(length)]


def encoded_bitmap(bitmap: list[bool], constant_slices: list[list[int]]):
    bitmap = deepcopy(bitmap)
    constant_slices = deepcopy(constant_slices)
    for slice in constant_slices:
        min_index = min(slice)
        other_indexes = [index for index in slice if index != min_index]
        for index in other_indexes:
            bitmap[index] = False
    return bitmap


def encoded_data(encoded_bitmap: list[bool], data: list[int]):
    return [data[index] if value else 0 for index, value in enumerate(encoded_bitmap)]


def decoded_data(encoded_data: list[int], bitmap: list[bool], constant_slices: list[list[int]]):
    decoded = deepcopy(encoded_data)
    bitmap = deepcopy(bitmap)
    constant_slices = deepcopy(constant_slices)
    for slice in constant_slices:
        constant_value = decoded[slice[0]]
        for index in slice:
            if not bitmap[index]:
                decoded[index] = constant_value
    return decoded


def main(data: list[int]):
    constant_slices = list(all_constant_slices(data))
    slices = list(all_slices(len(data)))
    bitmap = inital_bitmap(len(data))
    encoded_bitmap_list = encoded_bitmap(bitmap, constant_slices)
    print("Bytes Normalised:", len([val for val in encoded_bitmap_list if not val]))
    encoded_data_list = encoded_data(encoded_bitmap_list, data)
    decoded_data_list = decoded_data(encoded_data_list, encoded_bitmap_list, constant_slices)

    print("Original Data:", data)
    print("---")
    print("All Slices:")
    print(*slices, sep="\n")
    print("---")
    print("Constant Slices:")
    print(*constant_slices, sep="\n")
    print("---")
    print("Initial Bitmap:", bitmap)
    print("---")
    print("Encoded Bitmap:", encoded_bitmap_list)
    print("---")
    print("Encoded Data:", encoded_data_list)
    print("---")
    print("Decoded Data:", decoded_data_list)
    print("---")
    print("Match:", data == decoded_data_list)
    print("---")
    print("Constant slices:", len(constant_slices))
    print("---")
    print("Bytes Normalised:", len([0 for val in encoded_data_list if val == 0]))
    assert data == decoded_data_list


if __name__ == "__main__":
    DATA = random_list(2000, 2)
    main(DATA)