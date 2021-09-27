from rotations import UnitQuaternion


def test_constructors():
    q1 = UnitQuaternion([1, 0, 0, 0])
    assert q1.is_unit

    q2 = UnitQuaternion([1, 0, 2, 0])

    print(q2.norm)
    assert q2.is_unit

    q3 = q2.inverse()
    assert q3.is_unit

    print(q3.imag)
    print(q2.imag)
    print(q2.imag == q3.imag)
