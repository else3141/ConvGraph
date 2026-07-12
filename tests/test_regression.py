"""Locks the pipeline output for the example graph against a known-good result."""
import numpy as np

from examples.demo import build

EXPECTED = np.array([
    [7, 8, 5, 6, 2, 1, 7],
    [7, 3, 4, 4, 4, 1, 7],
    [7, 3, 4, 4, 3, 1, 7],
    [7, 3, 4, 4, 3, 1, 7],
    [7, 3, 3, 3, 3, 1, 7],
    [7, 3, 3, 3, 3, 1, 7],
    [7, 7, 7, 7, 7, 7, 7],
])


def test_example_floorplan():
    assert np.array_equal(build(), EXPECTED)
