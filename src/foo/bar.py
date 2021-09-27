import numpy as np
from math import factorial as std_factorial


def hello(name: str) -> str:
    return f"Hello {name}!!"


# Implement factorial for numpy arrays:
factorial = np.vectorize(std_factorial)
