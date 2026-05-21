"""Noise-generation entry points."""

from noise_generation import (
    FFST_based_noise_generation,
    linear_interpolation,
    noise_generation as _noise_generation,
    temporal_autocorrelation,
)

from .config import NoiseGenerationConfig
from .validation import validate_noise_inputs


def generate_noise(
    prcp_array,
    acf_array,
    u_array,
    v_array,
    lon_data,
    lat_data,
    config: NoiseGenerationConfig | None = None,
):
    """Generate correlated Gaussian noise with validation and typed configuration."""

    config = config or NoiseGenerationConfig()
    prcp, acf, u, v, lon, lat = validate_noise_inputs(
        prcp_array,
        acf_array,
        u_array,
        v_array,
        lon_data,
        lat_data,
    )

    return _noise_generation(
        prcp,
        acf,
        u,
        v,
        lon,
        lat,
        config.window_size,
        config.overlap_ratio,
        config.ssft_war_thr,
        config.seed,
    )


noise_generation = _noise_generation

__all__ = [
    "FFST_based_noise_generation",
    "NoiseGenerationConfig",
    "generate_noise",
    "linear_interpolation",
    "noise_generation",
    "temporal_autocorrelation",
]
