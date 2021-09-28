import rotations_rs
import pytest


def test_unitquat():
    q = rotations_rs.UnitQuaternion(1, 0, 0, 0)
    assert q.norm() == pytest.approx(1.0)
