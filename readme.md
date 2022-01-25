# Rotations

Rotations is a python package for describing rotations using Rotation Matrices, Euler Angles and Quaternions. 

## Usage

```python
from rotations import UnitQuaternion, RotationMatrix, EulerAngles, AngleType

# Specify unit quaternions
q1 = UnitQuaternion.from_(1.0, 0.0, 0.0, 0.0)
q2 = UnitQuaternion.from_euler_angles(roll=0.5, pitch=0, yaw=0, angletype=AngleType.DEGREES)

# Use it for quaternion rotations
rotated_vector = q2 @ [1.0, 0.0, 0.0]

```
// todo: complete usage description

## CI
The repo is set up for automated tests with:

- `pytest`: unit tests
- `flake8`: linter
- `tox`: multiple environments

![Tests](https://github.com/Speterius/python-template/actions/workflows/test.yml/badge.svg)
