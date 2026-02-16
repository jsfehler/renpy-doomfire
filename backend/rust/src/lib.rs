use pyo3::prelude::*;
use rand::Rng;

/// Maximum colour index in the palette.
const MAX_COLOUR_INDEX: i32 = 36;

/// Backend for the fire simulation.
pub struct DoomFireBackend {
    /// Current value for every pixel's colour height.
    colour_heights: Vec<i32>,
    /// Indexes for every pixel in colour_heights.
    fire_positions: Vec<usize>,
}

impl DoomFireBackend {
    pub fn new() -> Self {
        Self {
            colour_heights: Vec::new(),
            fire_positions: Vec::new(),
        }
    }

    /// Populate the colour_heights and fire_positions attributes.
    /// colour_heights: Zero-filled list of length(width * height).
    ///   Represents the current height of every pixel.
    ///
    /// fire_positions: Tuple of the index for every pixel, except the bottom row.
    pub fn setup_height_map(&mut self, width: usize, height: usize) {
        let array_size = width * height;
        self.colour_heights = vec![0i32; array_size];
        self.fire_positions = Vec::with_capacity(width * (height - 1));

        // Set bottom line to last colour in palette.
        for x in 0..width {
            self.colour_heights[(height - 1) * width + x] = MAX_COLOUR_INDEX;
        }

        for x in 0..width {
            for y in 1..height {
                self.fire_positions.push(y * width + x);
            }
        }
    }

    /// Return a reference to the full colour‑height map.
    pub fn colour_heights(&self) -> &[i32] {
        &self.colour_heights
    }

    /// Advance the fire simulation by one frame.
    pub fn spread_fire(&mut self, width: usize) {
        let mut rng = rand::rng();

        for &pos in &self.fire_positions {
            let pixel = self.colour_heights[pos];

            if pixel == 0 {
                // If the pixel is already dark, just propagate darkness up.
                if pos >= width {
                    self.colour_heights[pos - width] = 0;
                }
            } else {
                // Add horizontal jitter and cooling.
                let r_index: i32 = rng.random_range(0..4);

                let dst = (pos as i32) - r_index + 1;
                let target = (dst - width as i32) as usize;

                if target < self.colour_heights.len() {
                    self.colour_heights[target] = pixel - (r_index & 1);
                }
            }
        }
    }
}

/// Python wrapper.
///
/// Exposed to Python as `doom_fire_rust.DoomFireBackend`.
#[pyclass(name = "DoomFireBackend")]
struct PyDoomFire {
    inner: DoomFireBackend,
}

#[pymethods]
impl PyDoomFire {
    #[new]
    fn new() -> Self {
        Self {
            inner: DoomFireBackend::new(),
        }
    }

    fn setup_height_map(&mut self, width: usize, height: usize) {
        self.inner.setup_height_map(width, height);
    }

    fn spread_fire(&mut self, width: usize) {
        self.inner.spread_fire(width);
    }

    fn colour_heights(&self) -> &[i32] {
        return &self.inner.colour_heights
    }


}

/// A Python module implemented in Rust via PyO3.
#[pymodule]
fn doom_fire_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyDoomFire>()?;
    Ok(())
}
