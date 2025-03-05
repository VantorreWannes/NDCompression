from ndcompression._internals._nd_shape import NDShape

if __name__ == "__main__":
    NDSHAPE = NDShape([2, 3, 4])
    MULTI_INDEX = [1, 2, 3]
    FLAT_INDEX = NDSHAPE.flat_index(MULTI_INDEX)
    assert NDSHAPE.multi_index(FLAT_INDEX) == MULTI_INDEX