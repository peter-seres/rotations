from __future__ import annotations
import numpy as np
from .common import Vector, Matrix


class RotationMatrix(np.ndarray):
    def __new__(cls, R: Matrix) -> RotationMatrix:
        obj = np.asarray(R, dtype=float).view(cls)

        if obj.shape != (3, 3):
            raise ValueError("Input array must have equivalent shape (3, 3).")

        return obj

    def __repr__(self):
        return f"RotationMatrix: ({self})"

    @staticmethod
    def from_vector(v: Vector) -> RotationMatrix:
        """Generate rotation matrix from 9-by-1 matrix."""

        return RotationMatrix(np.array(v).reshape(3, 3))

    @staticmethod
    def identity() -> RotationMatrix:
        """Generate identity rotation matrix."""

        return RotationMatrix(np.eye(3))

    @staticmethod
    def default() -> RotationMatrix:
        """Default no-rotation matrix returns the identity matrix."""

        return RotationMatrix.identity()

    @staticmethod
    def from_yaw_and_z(yaw: float = 0.0, z: Vector = None) -> RotationMatrix:
        """Generate rotation matrix from yaw angle and inertial Z axis."""

        if z is None:
            z = np.array([0.0, 0.0, 1.0])
        else:
            if len(z) != 3:
                raise ValueError("Input z-axis must have length 3.")

            z = np.array(z)
            z /= np.linalg.norm(z)

        # Body Y axis (East)
        y = np.array([-np.sin(yaw), np.cos(yaw), 0.0])

        # Body X axis (North)
        x = np.cross(y, z)
        x /= np.linalg.norm(x)

        # Recompute body Y axis (East)
        y = np.cross(z, x)

        return RotationMatrix(np.hstack((x[:, None], y[:, None], z[:, None])))
