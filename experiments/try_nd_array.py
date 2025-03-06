from ndcompression import LinearNDArray, NDShape

if __name__ == "__main__":
    NDSHAPE = NDShape([2, 3, 4])
    NDARRAY = LinearNDArray(NDSHAPE)
    print(NDARRAY[(1, 2)])