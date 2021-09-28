from __future__ import annotations
import numpy as np
from .common import AngleType, Vector, array_like
from .so3 import SO3 as so3
from .euler_angles import EulerAngles
from .rotation_matrix import RotationMatrix
from typing import Union


class UnitQuaternion(np.ndarray):
    """
    UnitQuaternion class. Subclassed from numpy array for performance.
    0: scalar element, real part, w
    1-2-3: vector element, imaginary part, x-y-z
    """

    def __new__(cls, q: Vector) -> UnitQuaternion:

        if len(q) != 4:
            raise ValueError(f"Input array q: {q} must have length 4.")

        obj = np.asarray(q, dtype=float).view(cls)
        return obj

    # noinspection PyMissingConstructor
    def __init__(self, _: Vector) -> None:
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
        """ Check whether the quaternion is on the 4D unit sphere with a tolerance. """
        return abs(1.0 - self.norm) < tolerance

    @property
    def real(self) -> float:
        """ Real / Scalar part of quaternion. """
        return self.w

    @real.setter
    def real(self, value) -> None:
        """ Settter for the Real / Scalar part of quaternion. """
        self[0] = value
        self.normalize()

    @property
    def imag(self) -> np.ndarray:
        """ Imaginary / Vector part of the quaternion (3 by 1 numpy array) """
        return self[1:4]

    @imag.setter
    def imag(self, value: Vector) -> None:
        """ Setter of the imaginary part of the quaternion."""

        if len(value) != 3:
            raise ValueError("Setting imaginary part must be done using an array with 3 elements.")

        self[1:4] = value
        self.normalize()

    def normalize(self) -> None:
        if not self.is_unit:
            if self.norm > 0:
                self.__itruediv__(self.norm)

    def normalized(self) -> UnitQuaternion:
        self.normalize()
        return self

    def conjugate(self) -> UnitQuaternion:
        q = self.copy()
        q.imag *= -1
        return q

    def inverse(self) -> UnitQuaternion:
        """ inverse = conjugate / norm for general quaternions. Unit quats are already normalized."""
        return self.conjugate()

    def flipped(self) -> UnitQuaternion:
        """ The quaternion on the opposite side of the 4D sphere."""
        q = self.copy()
        q.real *= -1
        return q

    def unitX(self) -> np.ndarray:
        """ Return X axis of respective rotation matrix (body X). """

        return np.array([self.w ** 2 + self.x ** 2 - self.y ** 2 - self.z ** 2,
                        2 * (self.x * self.y + self.w * self.z),
                        2 * (self.x * self.z - self.w * self.y)])

    def unitY(self) -> np.ndarray:
        """ Return Y axis of respective rotation matrix (body Y). """

        return np.array([2 * (self.x * self.y - self.w * self.z),
                        self.w ** 2 + self.y ** 2 - self.x ** 2 - self.z ** 2,
                        2 * (self.y * self.z + self.w * self.x)])

    def unitZ(self) -> np.ndarray:
        """ Return Z axis of respective rotation matrix (body Z). """

        return np.array([2 * (self.x * self.z + self.w * self.y),
                        2 * (self.y * self.z - self.w * self.x),
                        self.w ** 2 + self.z ** 2 - self.x ** 2 - self.y ** 2])

    def __mul__(self, other):
        """ Override of the multiplication operator. """
        raise TypeError("UnitQuaternion does not support multiplication. Use @ operator for quaternion rotations.")

    def __matmul__(self, other: Union[UnitQuaternion, np.ndarray]) -> Union[UnitQuaternion, np.ndarray]:
        if type(other) is UnitQuaternion:
            return self.quat_product(q=other)
        elif type(other) in array_like:
            other = np.array(other)
            if len(other) == 3:
                return self.quat_rotate(v=np.array(other))
            else:
                raise ValueError("Quaternion rotation must involve a 3D vector")
        else:
            raise TypeError("Unsupported type for quaternion rotation.")

    def as_prodmat(self) -> np.ndarray:
        """ Return quaternion product matrix (Kronecker matrix) """

        Q = np.eye(4) * self.real
        Q[0, 1:4] -= self.imag
        Q[1:4, 0] += self.imag
        Q[1:4, 1:4] += so3.hat(self.imag)
        return Q

    def quat_product(self, q: UnitQuaternion) -> UnitQuaternion:
        return UnitQuaternion(self.as_prodmat() @ q)

    def quat_rotate(self, v: Vector) -> np.ndarray:
        v = UnitQuaternion([0.0, *v])
        v_rotated = self.as_prodmat() @ v.as_prodmat() @ self.inverse()
        return UnitQuaternion(v_rotated).normalized().imag

    def q_dot(self, omega: array_like) -> np.ndarray:
        """
        Returns a 4D numpy array representing the rate of the change of the quaternion.
        q_dot = 0.5 * Q * [0, omega]^T
        """

        if len(omega) != 3:
            raise ValueError("Input omega must have length 3.")

        omega = np.array([0, *omega])  # Add a zero as the scalar part
        return 0.5 * self.as_prodmat() @ omega

    def R_bi(self) -> RotationMatrix:
        """ Generate body-to-inertial rotation matrix from quaternion. """
        R = np.eye(3) + 2 * self.real * so3.hat(self.imag) + 2 * np.linalg.matrix_power(so3.hat(self.imag), 2)
        return RotationMatrix(R)

    def as_euler(self) -> EulerAngles:
        """ Return EulerAngles representation of rotation."""

        roll_atan_first = 2 * (self.w * self.x + self.y * self.z)
        roll_atan_second = 1.0 - 2.0 * (self.x ** 2 + self.y ** 2)
        yaw_atan_first = 2 * (self.w * self.z + self.x * self.y)
        yaw_atan_second = 1.0 - 2.0 * (self.y ** 2 + self.z ** 2)
        pitch_arcsin = 2 * (self.w * self.y - self.x * self.z)

        roll = np.arctan2(roll_atan_first, roll_atan_second)
        pitch = np.arcsin(pitch_arcsin)
        yaw = np.arctan2(yaw_atan_first, yaw_atan_second)

        return EulerAngles([roll, pitch, yaw])

    @staticmethod
    def default() -> UnitQuaternion:
        """ Zero-rotation quaternion. """
        return UnitQuaternion([1.0, 0.0, 0.0, 0.0])

    @staticmethod
    def from_(w: float, x: float, y: float, z: float) -> UnitQuaternion:
        """ Return UnitQuaternion from w, x, y, z elements."""
        return UnitQuaternion([w, x, y, z])

    @staticmethod
    def from_parts(real: float, imag: np.ndarray) -> UnitQuaternion:
        """ Return UnitQuaternion from scalar (real) and vector (imag) parts. """
        return UnitQuaternion([real, *imag])

    @staticmethod
    def from_rotmat(R: Union[RotationMatrix, array_like]):
        """ Generate UnitQuaternion from RotationMatrix """

        if type(R) not in [RotationMatrix, *array_like]:
            raise TypeError("Input matrix must be of type RotationmMatrix or array-like (numpy array, list, tuple)")

        elif type(R) in array_like:
            R = np.array(R)
            if R.shape != (3, 3):
                raise ValueError("Input numpy array must be of size 3x3")

        angle = np.arccos((np.trace(R) - 1) / 2.0)
        real_part = np.cos(angle / 2.0)
        return UnitQuaternion.from_parts(
            real=real_part,
            imag=so3.vex(so3.asymproj(R)) / (2.0 * real_part)
        )

    @staticmethod
    def from_euler_angles(roll: float = 0, pitch: float = 0, yaw: float = 0,
                          angletype: AngleType = AngleType.RADIANS) -> UnitQuaternion:
        """ Generate UnitQuaternion from roll, pitch and yaw angles."""

        if angletype == AngleType.DEGREES:
            roll, pitch, yaw = np.deg2rad([roll, pitch, yaw])

        q_yaw = UnitQuaternion.from_parts(
            real=np.cos(yaw / 2.0),
            imag=np.array([0.0, 0.0, np.sin(yaw / 2.0)])
        )

        q_pitch = UnitQuaternion.from_parts(
            real=np.cos(pitch / 2.0),
            imag=np.array([0.0, np.sin(pitch / 2.0), 0.0])
        )

        q_roll = UnitQuaternion.from_parts(
            real=np.cos(roll / 2.0),
            imag=np.array([np.sin(roll / 2.0), 0., 0.]))

        return q_yaw @ q_pitch @ q_roll

    @staticmethod
    def from_euler(eul: EulerAngles) -> UnitQuaternion:
        """ Generate UnitQuaternion from EulerAngles object."""
        return UnitQuaternion.from_euler_angles(eul.roll, eul.pitch, eul.yaw)
