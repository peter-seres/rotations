from rotations import UnitQuaternion, RotationMatrix, EulerAngles, AngleType
import pytest


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

    q_f = q_test.flipped()
    assert q_f.real == -q_test.real

    with pytest.raises(Exception):
        q_test.imag = [0.1, 2]


def test_wrong_constructors():
    with pytest.raises(Exception):
        _ = UnitQuaternion.from_rotmat([2, 3])

    with pytest.raises(Exception):
        _ = UnitQuaternion.from_rotmat(2.0)

    with pytest.raises(Exception):
        _ = UnitQuaternion([1, 0, 0])


def test_rotations(q_test, q_default):
    q_test @ q_default
    q_test @ [1.0, 0.0, 0.0]

    with pytest.raises(Exception):
        _ = q_test * q_default

    with pytest.raises(Exception):
        _ = q_test @ 2.0

    with pytest.raises(Exception):
        _ = q_test @ [0.0, 1.0]


def test_unit_dirs(q_default):
    x = q_default.unitX()
    y = q_default.unitY()
    z = q_default.unitZ()

    assert x == pytest.approx([1, 0, 0])
    assert y == pytest.approx([0, 1, 0])
    assert z == pytest.approx([0, 0, 1])


def test_qdot(q_default):
    omega1 = [0, 0, 0]
    qdot1 = q_default.q_dot(omega1)

    assert qdot1 == pytest.approx([0, 0, 0, 0])

    rate = 0.1
    omega2 = [0.0, 0.0, rate]
    qdot2 = q_default.q_dot(omega2)

    assert qdot2 == pytest.approx([0, 0, 0, rate/2])

    with pytest.raises(Exception):
        _ = q_default.q_dot([0, 0])


def test_transforms(q_default):
    assert q_default.R_bi() == pytest.approx(RotationMatrix.default())

    e = EulerAngles([0, 0, 0])

    assert q_default.as_euler() == pytest.approx(e)

    q = UnitQuaternion.from_euler(e)

    assert q.as_euler() == pytest.approx(e)

    q2 = q.from_euler_angles(0, 0, 180, AngleType.DEGREES)

    assert q2 == pytest.approx([0, 0, 0, 1])
