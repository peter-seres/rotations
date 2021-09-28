extern crate pyo3;
mod unit_quaternion;
use crate::unit_quaternion::UnitQuaternion;
pub use pyo3::prelude::*;
pub use pyo3::wrap_pyfunction;

#[pyfunction]
fn add(a: i64, b: i64) -> PyResult<i64> {
    Ok(a + b)
}


#[pymodule]
fn rotations_rs(_: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    m.add_class::<UnitQuaternion>()?;

    Ok(())
}
