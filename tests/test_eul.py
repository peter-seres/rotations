import numpy as np
import pytest
from rotations import EulerAngles, AngleType, RotationMatrix


def test_constructors():
    e1 = EulerAngles([0, 0, np.pi])
    e2 = EulerAngles.from_angles(0, 0, np.pi)
    e3 = EulerAngles.from_rotmat(RotationMatrix.default())

    assert e1.roll == e2.roll
    assert e1.pitch == e2.pitch
    assert e1.yaw == pytest.approx(e2.yaw)
    assert e3.roll == e3.pitch == e3.yaw == pytest.approx(0.0)


def test_properties():
    e1 = EulerAngles([0, 0, np.pi / 2])
    e2 = e1.copy()

    e2.roll = 0.2
    e2.pitch = -0.2

    e1.yaw = 1.0
    e2.yaw = 1.0

    assert e1.roll < e2.roll
    assert e1.pitch > e2.pitch
    assert e1.yaw == e2.yaw


def test_wrong_constructors():
    with pytest.raises(Exception):
        _ = EulerAngles([1, 2, 3, 4])


def test_angle_types():
    e1 = EulerAngles([0, 0, np.pi / 2])
    e2 = EulerAngles.from_angles(0, 0, 90, AngleType.DEGREES)

    assert e1.yaw == pytest.approx(e2.yaw)
    assert e1.as_vector(AngleType.DEGREES)[2] == pytest.approx(90.0)
    assert (e1.as_vector() == np.array([0, 0, np.pi / 2])).all()


def test_rotation_matrix():
    e1 = EulerAngles([1, 2, 3])

    R_known = np.array(
        [
            [0.4119822, -0.8337377, -0.3676305],
            [-0.0587266, -0.4269176, 0.9023816],
            [-0.9092974, -0.3501755, -0.2248451],
        ]
    )

    assert e1.R_bi() == pytest.approx(R_known)


def test_repr():
    e1 = EulerAngles([1, 2, 3])
    repr(e1)
