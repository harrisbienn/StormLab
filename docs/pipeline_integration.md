# Pipeline Integration Notes

StormLab started as research code organized around notebooks. The package layer in this repository keeps those notebooks working while also making the model usable from a larger processing pipeline.

## Recommended Environment

Use Python 3.12 for the first modernization target:

```bash
conda env create -f environment.yml
conda activate stormlab
pip install -e .[dev]
pytest
```

Python 3.13 should also be possible once the scientific dependency stack is available in your deployment environment. Python 3.14 is newer, but it is a less conservative target for production scientific processing.

For notebooks and EDA plots, use the separate `environment-notebooks.yml` environment. It includes `matplotlib-base`, `matplotlib-inline`, JupyterLab, and an IPython kernel while keeping plotting dependencies out of the core pipeline environment:

```bash
conda env create -f environment-notebooks.yml
conda activate stormlab-notebooks
pip install -e .[dev]
python -m ipykernel install --user --name stormlab-notebooks --display-name "StormLab notebooks"
jupyter lab
```

## Public Imports

Prefer the package imports in new code:

```python
from stormlab.config import NoiseGenerationConfig, TrackingConfig
from stormlab.fitting import fit_tngd
from stormlab.noise import generate_noise, temporal_autocorrelation
from stormlab.simulation import simulate_rainfall
from stormlab.tracking import attach_precipitation_events, track_rainstorms
```

The original modules remain available for the existing notebooks:

```python
from noise_generation import noise_generation
from simulation import rainfall_simulation
```

## Package-Facing API

Use the package-facing wrappers in production code because they validate shapes and use typed configuration:

```python
tracking_config = TrackingConfig(
    low_threshold=250,
    high_threshold=500,
    morph_radius=1,
    expand_distance=5,
    overlap_ratio=0.2,
    dry_spell_time=0,
)

track_array = track_rainstorms(ivt_array, tracking_config)
attached_prcp = attach_precipitation_events(prcp_array, track_array)

noise_config = NoiseGenerationConfig(
    window_size=(128, 128),
    overlap_ratio=0.3,
    ssft_war_thr=0.1,
    seed=1,
)

noise_array = generate_noise(
    prcp_array,
    acf_array,
    u_array,
    v_array,
    lon_data,
    lat_data,
    noise_config,
)

simulated_rainfall = simulate_rainfall(
    noise_array,
    wet_probability,
    gamma_shape,
    gamma_scale,
    generalized_gamma_c,
)
```

The lower-level notebook-era functions are still useful for comparing against published examples, but they do less validation.

## Suggested Pipeline Stages

1. Load and validate climate inputs.
2. Track IVT/rainstorm objects.
3. Attach precipitation regions to tracked objects.
4. Fit or load distribution parameters.
5. Generate correlated Gaussian noise fields.
6. Convert noise fields into rainfall simulations.
7. Save outputs with coordinates, units, realization ID, seed, and source metadata.

## Demo Notebooks

The `examples_pipeline/` folder contains modern demo notebooks that use the package-facing API:

- `01_tracking_demo.ipynb`
- `02_distribution_fitting_demo.ipynb`
- `03_noise_generation_demo.ipynb`
- `04_rainfall_simulation_demo.ipynb`
- `05_end_to_end_demo.ipynb`

Use these for demos, EDA, and as templates for pipeline tasks. The original notebooks in `examples/` are preserved as reference material for the published workflow.

## Integration Boundary

The scientific functions are mostly pure array transformations. For production use, keep file I/O outside these functions when possible:

- pipeline code reads NetCDF/CSV/NumPy files
- StormLab functions transform arrays
- pipeline code writes outputs and metadata

That separation makes testing, retries, provenance tracking, and batch execution much easier.

## Compatibility Notes

The previous implementation used `scipy.interpolate.interp2d`, which was removed in SciPy 1.14. The interpolation helper now uses `RegularGridInterpolator`.

For robust production runs, add validation around:

- expected array dimensions: usually `(time, lat, lon)`
- coordinate ordering, especially latitude
- units for precipitation and wind
- missing values and all-dry timesteps
- random seed and realization ID
