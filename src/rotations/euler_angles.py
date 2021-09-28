from __future__ import annotations
import numpy as np
from .common import AngleType, Vector
from .rotation_matrix import RotationMatrix
import typing

if typing.TYPE_CHECKING:
    from .unit_quaternion import UnitQuaternion


class EulerAngles(np.ndarray):
    """ Euler angle representation of 3D rotation. """

    def __new__(cls, v: Vector):

        if len(v) != 3:
            raise ValueError(f"Input array v: {v} must have length 3.")

        obj = np.asarray(v, dtype=float).view(cls)
        return obj

    @staticmethod
    def from_angles(roll: float = 0.0, pitch: float = 0.0, yaw: float = 0.0,
                    angletype: AngleType = AngleType.RADIANS):

        if angletype == AngleType.DEGREES:
            roll, pitch, yaw = np.deg2rad([roll, pitch, yaw])

        return EulerAngles([roll, pitch, yaw])

    @property
    def roll(self) -> float:
        return self[0]

    @roll.setter
    def roll(self, value: float) -> None:
        self[0] = value

    @property
    def pitch(self) -> float:
        return self[1]

    @pitch.setter
    def pitch(self, value: float) -> None:
        self[1] = value

    @property
    def yaw(self):
        return self[2]

    @yaw.setter
    def yaw(self, value: float) -> None:
        self[2] = value

    def as_vector(self, angletype: AngleType = AngleType.RADIANS) -> np.ndarray:
        """ Represent class as a 3-by-1 vector. """

        if angletype == AngleType.DEGREES:
            return np.rad2deg(self)
        else:
            return self

    def R_roll(self) -> np.ndarray:
        """ Generate (inertial-to-body) rotation matrix (due to roll) in East-Down plane. """

        sin_phi, cos_phi = np.sin(self.roll), np.cos(self.roll)

        return np.array([
            [1, 0, 0],
            [0, cos_phi, sin_phi],
            [0, -sin_phi, cos_phi]
        ])

    def R_pitch(self) -> np.ndarray:
        """ Generate (inertial-to-body) rotation matrix (due to pitch) in North-Down plane. """

        sin_theta, cos_theta = np.sin(self.pitch), np.cos(self.pitch)

        return np.array([
            [cos_theta, 0, -sin_theta],
            [0, 1, 0],
            [sin_theta, 0, cos_theta]
        ])

    def R_yaw(self) -> np.ndarray:
        """ Generate (inertial-to-body) rotation matrix (due to yaw) in North-East plane. """

        sin_psi, cos_psi = np.sin(self.yaw), np.cos(self.yaw)

        return np.array([
            [cos_psi, sin_psi, 0],
            [-sin_psi, cos_psi, 0],
            [0, 0, 1]
        ])

    def R_bi(self) -> np.ndarray:
        """ Generate 3-by-3 rotation matrix from body to inertial frame (NED) """

        return (self.R_roll() @ self.R_pitch() @ self.R_yaw()).T

    def T_eb(self) -> np.ndarray:
        """ Generate 3-by-3 transformation matrix from Euler-rates to body-rates. """

        sin_phi, cos_phi = np.sin(self.roll), np.cos(self.roll)
        sin_theta, cos_theta = np.sin(self.pitch), np.cos(self.pitch)

        return np.array([
            [1, 0, -sin_theta],
            [0, cos_phi, sin_phi * cos_theta],
            [0, -sin_phi, cos_phi * cos_theta]
        ])

    def T_be(self) -> np.ndarray:
        """ Generate 3-by-3 transformation matrix from body-rates to Euler-rates. """

        sin_phi, cos_phi = np.sin(self.roll), np.cos(self.roll)
        sin_theta, cos_theta = np.sin(self.pitch), np.cos(self.pitch)

        return np.array([
            [cos_theta, sin_phi * sin_theta],
            [cos_phi * sin_theta, 0, cos_phi * cos_theta],
            [-sin_phi * cos_theta, 0, sin_phi, cos_phi]
        ]) / cos_theta

    @staticmethod
    def from_rotmat(R: RotationMatrix) -> EulerAngles:
        """ Generate EulerAngles object from RotationMatrix """
        if type(R) is RotationMatrix:
            R = R.as_matrix()
        else:
            raise ValueError("Input R must be of type RotationMatrix.")

        phi = np.arctan(R[2, 1] / R[2, 2])
        theta = -np.arcsin(R[2, 0])
        psi = np.arctan(R[1, 0] / R[0, 0])

        return EulerAngles([phi, theta, psi])

    @staticmethod
    def from_quat(q: UnitQuaternion) -> EulerAngles:
        """ Generate euler angles from unit quaternion. """
        pass
        # if type(q) is quat.UnitQuaternion:
        #     q = quaternion.as_vector()
        # elif type(quaternion) is np.array:
        #     q = quaternion
        # else:
        #     raise TypeError('Input has to be 4D vector or quaternion.')
        #
        # roll_atan_first = 2 * (q[0] * q[1] + q[2] * q[3])
        # roll_atan_second = 1.0 - 2.0 * (q[1] ** 2 + q[2] ** 2)
        # yaw_atan_first = 2 * (q[0] * q[3] + q[1] * q[2])
        # yaw_atan_second = 1.0 - 2.0 * (q[2] ** 2 + q[3] ** 2)
        # pitch_arcsin = 2 * (q[0] * q[2] - q[1] * q[3])
        #
        # roll = np.arctan2(roll_atan_first, roll_atan_second)
        # pitch = np.arcsin(pitch_arcsin)
        # yaw = np.arctan2(yaw_atan_first, yaw_atan_second)
        #
        # return EulerAngles([roll, pitch, yaw])

    def __repr__(self) -> str:
        return f"EulerAngles[rad](roll = {self.roll}, pitch = {self.pitch}, yaw = {self.yaw})"
