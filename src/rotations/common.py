from typing import Union, List
from enum import Enum, auto
import numpy as np


Vector = Union[tuple, List, np.ndarray]
Matrix = Union[tuple, List, np.ndarray]


class AngleType(Enum):
    RADIANS = auto()
    DEGREES = auto()
