# StormLab: Space-time Nonstationary Rainfall Model for Large Area Basins

![StormLab overview: (A) Graphical showing how StormLab converts large-scale climate model predictions into thousands of realistic high-resolution rainfall simulations. (B) Rainfall "frequency curve" for Mississippi Basin rainfall, showing close agreement between high-resolution StormLab simulations and validation measurements.](/images/brief_figure_20231130.png)

## Introduction

This repository contains code to implement StormLab,
a stochastic rainfall generator that simulate 6-hour,
0.03° resolution rainfall fields over large-area river basins
conditioned on global climate model data.

## Dependencies

Required packages are listed in `environment.yml` and `requirements.txt`.

For new work, use the installable package interface:

```bash
conda env create -f environment.yml
conda activate stormlab
pip install -e .[dev]
pytest
```

For demo notebooks and EDA plots, use the separate notebook environment:

```bash
conda env create -f environment-notebooks.yml
conda activate stormlab-notebooks
pip install -e .[dev]
python -m ipykernel install --user --name stormlab-notebooks --display-name "StormLab notebooks"
jupyter lab
```

If the environment already exists, update it after dependency changes with:

```bash
conda env update -f environment-notebooks.yml --prune
```

Then import StormLab from another script or pipeline:

```python
from stormlab.noise import noise_generation
from stormlab.simulation import rainfall_simulation
from stormlab.tracking import rainstorm_tracking
```

For pipeline code, prefer the validated wrappers:

```python
from stormlab.config import NoiseGenerationConfig
from stormlab.noise import generate_noise
from stormlab.simulation import simulate_rainfall
from stormlab.tracking import track_rainstorms
```

See `docs/pipeline_integration.md` for integration notes.

Modern demo notebooks are available in `examples_pipeline/`. The original notebooks in `examples/` are kept as reference examples for the published workflow.

## Usage

1. Download the example data and unzip at the code folder "/StormLab."

    - Google Drive: <https://drive.google.com/file/d/1x090aVFbe0c3PPZnvwevptN4nP7GuCf7/view?usp=drive_link>
    - The folder should look like: "/StormLab/data"

2. Rainstorm tracking
    - See `/examples/Storm_tracking_on_CESM2_data.ipynb`
3. TNGD distribution fitting
    - See `/examples/TNGD_distribution_fitting.ipynb`
4. Noise generation
    - See `/examples/Noise_generation.ipynb`
5. Rainfall simulation
    - See `/examples/Rainfall_simulation.ipynb`

## Citation

If you use this model in your work, please cite:

Liu, Y., Wright, D. B., & Lorenz, D. J. (2024). A Nonstationary Stochastic Rainfall Generator Conditioned on Global Climate Models for Design Flood Analyses in the Mississippi and Other Large River Basins. Water Resources Research, 60(5), e2023WR036826. <https://doi.org/10.1029/2023WR036826>

## Contributing

Feel free to open an issue for bugs and feature requests.

## License

StormLab is released under the [MIT License](https://opensource.org/licenses/MIT).

## Authors

- [Yuan Liu](https://her.cee.wisc.edu/group-members/) - *research & developer*
- [Daniel B. Wright](https://her.cee.wisc.edu/group-members/) - *research*
- [David J. Lorenz](http://djlorenz.github.io/) - *research*

## Attribution

This project uses code from the following repositories:

- [pysteps](https://pysteps.readthedocs.io/en/stable/)
- [STREAM](https://github.com/sam-hartke/STREAM)
- [starch](https://github.com/lorenliu13/starch/tree/master)
