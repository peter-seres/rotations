from __future__ import annotations
import numpy as np
from .common import Vector


class RotationMatrix:
    def __init__(self, R: np.ndarray = None):
        if R is None:
            self._R = np.eye(3)
        else:
            self._R = R

    def __repr__(self):
        return f"RotationMatrix: ({self._R})"

    def as_vector(self) -> np.ndarray:
        return self._R.reshape(9)

    def as_matrix(self) -> np.ndarray:
        return self._R

    @staticmethod
    def from_vector(v: Vector) -> RotationMatrix:
        """ Generate rotation matrix from 9-by-1 matrix. """

        return RotationMatrix(np.array(v).reshape(3, 3))

    @staticmethod
    def from_yaw_and_z(yaw: float = 0.0, z: np.ndarray = None) -> RotationMatrix:
        """ Generate rotation matrix from yaw angle and inertial Z axis. """

        if z is None:
            z = np.array([0.0, 0.0, 1.0])
        elif type(z) is np.ndarray:
            z /= np.linalg.norm(z)
        else:
            raise ValueError("Input z-axis must be numpy array.")

        # Body Y axis (East)
        y = np.array([-np.sin(yaw), np.cos(yaw), 0.0])

        # Body X axis (North)
        x = np.cross(y, z)
        x /= np.linalg.norm(x)

        # Recompute body Y axis (East)
        y = np.cross(z, x)

        return RotationMatrix(np.hstack((x[:, None], y[:, None], z[:, None])))
