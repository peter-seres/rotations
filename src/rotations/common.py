from typing import Union, List
from enum import Enum, auto
import numpy as np

array_like = [tuple, list, np.ndarray]
Vector = Union[tuple, list, np.ndarray]
Matrix = Union[tuple, list, np.ndarray]


class AngleType(Enum):
    RADIANS = auto()
    DEGREES = auto()
