import pytest
from ndcompression._internals._nd_shape import NDShape

@pytest.fixture
def nd_shape():
    return NDShape([2, 3, 4])

def test_flat_index(nd_shape: NDShape):
    assert nd_shape.flat_index([1, 2, 3]) == 23
    assert nd_shape.flat_index([1, 0, 2]) == 14
    assert nd_shape.flat_index([1, 1, 1]) == 17

def test_multi_index(nd_shape: NDShape):
    assert nd_shape.multi_index(23) == [1, 2, 3]
    assert nd_shape.multi_index(14) == [1, 0, 2]
    assert nd_shape.multi_index(17) == [1, 1, 1]