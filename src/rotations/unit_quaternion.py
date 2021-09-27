from __future__ import annotations
import numpy as np
from .common import AngleType, Vector, Matrix
from .euler_angles import EulerAngles
from .rotation_matrix import RotationMatrix
from typing import Union
import common


class UnitQuaternion(np.ndarray):

    """
    UnitQuaternion class. Subclassed from numpy array for performance.

    0: scalar element, real part, w
    1-2-3: vector element, imaginary part, x-y-z
    """

    def __new__(cls, q: Vector):

        if len(q) != 4:
            raise ValueError(f"Input array q: {q} must have length 4.")

        obj = np.asarray(q, dtype=float).view(cls)
        return obj

    # noinspection PyMissingConstructor
    def __init__(self, q: Vector):
        self.normalize()

    @property
    def w(self) -> float:
        return self[0]

    @property
    def x(self) -> float:
        return self[1]

    @property
    def y(self) -> float:
        return self[2]

    @property
    def z(self) -> float:
        return self[3]

    @property
    def norm(self) -> float:
        return np.linalg.norm(self)

    @property
    def is_unit(self, tolerance: float = 1e-15) -> bool:
        return abs(1.0 - self.norm) < tolerance

    @property
    def real(self) -> float:
        """ Real / Scalar part of quaternion. """
        return self.w

    @property
    def imag(self) -> np.ndarray:
        """ Imaginary / Vector part of a quaternion """
        return self[1:4]

    @imag.setter
    def imag(self, value: Vector) -> None:
        if len(value) != 3:
            raise ValueError("Setting imaginary part must be done using an array with 3 elements.")

        self[1:4] = value

    def normalize(self):
        if not self.is_unit:
            if self.norm > 0:
                self.__itruediv__(self.norm)

    def conjugate(self):
        q = self.copy()
        q.imag *= -1
        return q

    def inverse(self):
        """ inverse = conjugate / norm for general quaternions. Unit quats are already normalized."""
        return self.conjugate()

    def flipped(self):
        """ The quaternion on the opposite side of the 4D sphere."""
        return UnitQuaternion([-self.w, self.x, self.y, self.z])

    def __mul__(self, other):
        """ Override of the multiplication operator. """
        raise TypeError("UnitQuaternion does not support multiplication. Use @ operator for quaternion rotations.")

    def __matmul__(self, other) -> Union[UnitQuaternion, np.ndarray]:
        if type(other) is UnitQuaternion:
            return self.quat_product(q=other)
        elif type(other) in [np.ndarray, list, tuple]:
            if len(other) == 3:
                return self.quat_rotate(v=np.array(other))
            else:
                raise ValueError("Quaternion rotation must involve a 3D vector")
        else:
            raise TypeError("Unsupported type for quaternion rotation.")

    def as_prodmat(self):
        """ Return quaternion product matrix (Kronecker matrix) """

        Q = np.eye(4) * self.real
        Q[0, 1:4] -= self.imag
        Q[1:4, 0] += self.imag
        Q[1:4, 1:4] += common.hat(self.imag)
        return Q

    def quat_product(self, q: UnitQuaternion) -> UnitQuaternion:
        return UnitQuaternion(self.as_prodmat() @ q)

    def quat_rotate(self, v) -> np.ndarray:
        v = UnitQuaternion([0.0, *v])
        v_rotated = self.as_prodmat() @ v.as_prodmat() @ self.inverse()

        return UnitQuaternion(v_rotated)

