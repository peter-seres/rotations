from rotations import UnitQuaternion, RotationMatrix
import pytest
import numpy as np


@pytest.fixture
def q_default():
    return UnitQuaternion.default()


@pytest.fixture
def q_test():
    return UnitQuaternion([1, 0, 0, 0.1])


def test_constructors():
    q1 = UnitQuaternion([1, 0, 0, 0])
    q2 = UnitQuaternion.default()
    q3 = UnitQuaternion.from_(1.0, 0.0, 0.0, 0.0)
    q4 = UnitQuaternion.from_parts(real=1.0, imag=[0.0, 0.0, 0.0])
    q5 = UnitQuaternion.from_rotmat(RotationMatrix.default())

    assert q1 == pytest.approx(q5)
    assert q1 == pytest.approx(q2)
    assert q2 == pytest.approx(q3)
    assert q4 == pytest.approx(q5)


def test_properties(q_test):

    assert q_test.w > 0.0
    assert q_test.z > 0.0
    assert q_test.x == q_test.y == 0.0


def test_wrong_constructors():
    with pytest.raises(Exception):
        _ = UnitQuaternion.from_rotmat([2, 3])

    with pytest.raises(Exception):
        _ = UnitQuaternion.from_rotmat(2.0)

    with pytest.raises(Exception):
        _ = UnitQuaternion([1, 0, 0])


def test_rotations():
    pass
