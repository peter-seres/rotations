from typing import Optional
import numpy as np


class SO3:
    @staticmethod
    def hat(v: Optional[np.ndarray] = None):
        """Skew-symmetric matrix in SO(3) from 3D vector."""
        if v is None:
            v = np.zeros(3)
        return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

    @staticmethod
    def vex(m: Optional[np.ndarray] = None):
        """3D vector from skew-symmetric matrix in SO(3)."""
        if m is None:
            m = np.eye(3)
        return np.array([m[2, 1], m[0, 2], m[1, 0]])

    @staticmethod
    def symproj(H: Optional[np.ndarray] = None):
        """Symmetric projection of a square matrix."""
        if H is None:
            H = np.eye(3)
        return (H + H.T) / 2

    @staticmethod
    def asymproj(H: Optional[np.ndarray] = None):
        """Anti-symmetric projection of a square matrix."""
        if H is None:
            H = np.eye(3)
        return (H - H.T) / 2
