# Rotations

A python package to describe 3D rotations using unit quaternions, rotation matrices, Euler angles. 

![Tests](https://github.com/Speterius/python-template/actions/workflows/test.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
 [![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

## Dependencies

Only depends on `numpy`

Tested for: `Python 3.8, 3.9, 3.10`

## Usage

```python
from rotations import UnitQuaternion, RotationMatrix, EulerAngles, AngleType

# Specify unit quaternions
q1 = UnitQuaternion.from_(1.0, 0.0, 0.0, 0.0)
q2 = UnitQuaternion.from_euler_angles(roll=30.0, pitch=10.0, yaw=0, angletype=AngleType.DEGREES)

# Use it for quaternion rotations
rotated_vector = q2 @ [1.0, 0.0, 0.0]
```

## Development guide

### Install package 

```
git clone git@github.com:peter-seres/rotations.git
cd rotations
python -m venv venv
venv\scripts\Activate
pip install -r requirements.txt
pip install -r requirements_dev.txt
pip install -e .
```

### CI
- Automate tests with `pytest`
- Automate linting using `black`
- `tox`: automate github actions for multiple environments
