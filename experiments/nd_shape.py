from ndcompression._internals._nd_shape import NDShape

if __name__ == "__main__":
    NDSHAPE = NDShape([2, 2, 2])
    MULTI_INDEX = [1, 1, 1]
    print(NDSHAPE.flat_index(MULTI_INDEX))
    print(NDSHAPE.multi_index(17))