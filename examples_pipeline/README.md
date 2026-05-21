# Pipeline Examples

These notebooks demonstrate the newer package-facing StormLab API. They are intended for demos, EDA, and future processing-pipeline design.

Run them from the notebook environment:

```bash
conda env create -f environment-notebooks.yml
conda activate stormlab-notebooks
pip install -e .[dev]
python -m ipykernel install --user --name stormlab-notebooks --display-name "StormLab notebooks"
jupyter lab
```

Choose the `StormLab notebooks` kernel when opening these notebooks. This environment includes `matplotlib-base` and `matplotlib-inline` for notebook plotting without pulling in a heavier desktop GUI backend.

If you already created the environment before NetCDF backends were added, update it with:

```bash
conda env update -f environment-notebooks.yml --prune
```

## Notebooks

- `01_tracking_demo.ipynb`: identify and track IVT/rainstorm objects from CESM2 fields.
- `02_distribution_fitting_demo.ipynb`: fit one-grid TNGD parameters from bundled ERA5/AORC dataframe inputs.
- `03_noise_generation_demo.ipynb`: generate correlated Gaussian noise on a spatial subset.
- `04_rainfall_simulation_demo.ipynb`: transform noise into rainfall with fitted distribution parameters.
- `05_end_to_end_demo.ipynb`: sketch a small subset workflow across tracking, noise, and simulation stages.

The notebooks use small subsets by default so they stay interactive. Optional save cells are included but commented out.
