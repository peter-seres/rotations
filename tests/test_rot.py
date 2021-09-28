from rotations import RotationMatrix
import numpy as np
import pytest


def test_constructors():
    a = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

    b = ((1, 2, 3),
         (4, 5, 6),
         (7, 8, 9))

    c = np.array(a)

    d = c.flatten()

    R1 = RotationMatrix(a)
    R2 = RotationMatrix(b)
    R3 = RotationMatrix(c)
    R4 = RotationMatrix.from_vector(d)

    assert (R1 == R2).all()
    assert (R2 == R3).all()
    assert (R3 == R4).all()


def test_wrong_constructors():

    a = [[1, 2, 3, 4],
         [4, 5, 6, 5],
         [7, 8, 9, 7]]

    with pytest.raises(Exception):
        R1 = RotationMatrix(a)

    with pytest.raises(Exception):
        R2 = RotationMatrix(np.array(a).flatten())


def test_identity():
    R1 = RotationMatrix.default()
    R2 = RotationMatrix.identity()
    assert (R1 == np.eye(3)).all()
    assert (R2 == np.eye(3)).all()


def test_yawz():
    R1 = RotationMatrix.from_yaw_and_z(0, [0.0, 0.0, 1.0])
    R2 = RotationMatrix.from_yaw_and_z()

    assert (R1 == np.eye(3)).all()
    assert (R2 == np.eye(3)).all()

    with pytest.raises(Exception):
        R3 = RotationMatrix.from_yaw_and_z(0, [0.0, 0.0, 1.0, 5.0])


def test_repr():
    repr(RotationMatrix.default())
