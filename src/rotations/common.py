from typing import Union, List
from enum import Enum, auto
import numpy as np


Vector = Union[tuple, List, np.ndarray]
Matrix = Union[tuple, List, np.ndarray]


class AngleType(Enum):
    RADIANS = auto()
    DEGREES = auto()


def hat(v: np.ndarray = np.zeros(3)):
    """ Skew-symmetric matrix in SO(3) from 3D vector. """
    return np.array([[0, -v[2], v[1]],
                     [v[2], 0, -v[0]],
                     [-v[1], v[0], 0]])
