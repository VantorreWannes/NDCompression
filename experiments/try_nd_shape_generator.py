from ndcompression._internals._shape_generator import ShapeGenerator


if __name__ == "__main__":
    ND_SHAPE_GENERATOR = ShapeGenerator(12)
    print(list(ND_SHAPE_GENERATOR))