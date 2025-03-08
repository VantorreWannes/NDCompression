from ndcompression import NDShape

if __name__ == "__main__":
    NDSHAPE = NDShape([2, 2])
    for row in NDSHAPE.multi_slices():
        print(row)
