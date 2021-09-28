use crate::pyo3::prelude::*;

#[pyclass]
#[derive(Clone, Copy, Debug)]
pub struct UnitQuaternion {
    w: f64,
    x: f64,
    y: f64,
    z: f64,
}

#[pymethods]
impl UnitQuaternion {
    #[new]
    pub fn new(w: f64, x: f64, y: f64, z: f64) -> Self {
        Self{w, x, y, z}.normalized()
    }

    #[staticmethod]
    #[inline]
    pub fn identity() -> Self {
        Self{ w: 1.0, x: 0.0, y: 0.0, z: 0.0 }
    }

    #[inline]
    pub fn real(&self) -> PyResult<f64> {
        Ok(self.w)
    }

    #[inline]
    fn normalized(self) -> Self {
        let n = self.norm();
        if n < 1e-7 {
            Self::identity()
        } else {
            Self{
                w: self.w / n,
                x: self.x / n,
                y: self.y / n,
                z: self.z / n
            }
        }
    }

    #[inline]
    fn norm(&self) -> f64 {
        (self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z).sqrt()
    }
}
