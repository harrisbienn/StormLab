import numpy as np
import pytest

from stormlab.config import NoiseGenerationConfig, TrackingConfig
from stormlab.noise import generate_noise, linear_interpolation, temporal_autocorrelation
from stormlab.simulation import rainfall_simulation, simulate_rainfall


def test_linear_interpolation_regular_grid_preserves_orientation():
    old_x = np.array([0.0, 1.0])
    old_y = np.array([1.0, 0.0])
    field = np.array(
        [
            [10.0, 11.0],
            [0.0, 1.0],
        ]
    )

    new_x = np.array([0.0, 0.5, 1.0])
    new_y = np.array([1.0, 0.5, 0.0])

    interpolated = linear_interpolation(field, old_x, old_y, new_x, new_y)

    expected = np.array(
        [
            [10.0, 10.5, 11.0],
            [5.0, 5.5, 6.0],
            [0.0, 0.5, 1.0],
        ]
    )
    np.testing.assert_allclose(interpolated, expected)


def test_temporal_autocorrelation_returns_one_value_per_timestep():
    prcp = np.array(
        [
            [[0.0, 1.0], [2.0, 0.0]],
            [[0.0, 2.0], [1.0, 0.0]],
            [[1.0, 2.0], [0.0, 0.0]],
        ]
    )

    acf = temporal_autocorrelation(prcp)

    assert acf.shape == (3,)
    assert acf[0] == 0.5


def test_rainfall_simulation_returns_nonnegative_field():
    noise = np.zeros((2, 2, 2))
    wet_probability = np.ones((2, 2, 2))
    gamma_shape = np.ones((2, 2, 2))
    gamma_scale = np.ones((2, 2, 2))
    generalized_gamma_c = np.ones((2, 2))

    simulated = rainfall_simulation(
        noise,
        wet_probability,
        gamma_shape,
        gamma_scale,
        generalized_gamma_c,
    )

    assert simulated.shape == noise.shape
    assert np.all(simulated >= 0)


def test_simulate_rainfall_accepts_time_varying_generalized_gamma_c():
    noise = np.zeros((2, 2, 2))
    wet_probability = np.ones((2, 2, 2))
    gamma_shape = np.ones((2, 2, 2))
    gamma_scale = np.ones((2, 2, 2))
    generalized_gamma_c = np.ones((2, 2, 2))

    simulated = simulate_rainfall(
        noise,
        wet_probability,
        gamma_shape,
        gamma_scale,
        generalized_gamma_c,
    )

    assert simulated.shape == noise.shape


def test_simulate_rainfall_rejects_mismatched_shapes():
    with pytest.raises(ValueError, match="logic_mu_array shape"):
        simulate_rainfall(
            np.zeros((2, 2, 2)),
            np.ones((1, 2, 2)),
            np.ones((2, 2, 2)),
            np.ones((2, 2, 2)),
            np.ones((2, 2)),
        )


def test_noise_config_rejects_invalid_overlap():
    with pytest.raises(ValueError, match="overlap_ratio"):
        NoiseGenerationConfig(overlap_ratio=1.0)


def test_tracking_config_rejects_reversed_thresholds():
    with pytest.raises(ValueError, match="low_threshold"):
        TrackingConfig(low_threshold=500, high_threshold=250)


def test_generate_noise_validates_time_dimension_before_heavy_work():
    with pytest.raises(ValueError, match="acf_array length"):
        generate_noise(
            np.zeros((2, 2, 2)),
            np.ones(1),
            np.zeros((2, 2, 2)),
            np.zeros((2, 2, 2)),
            np.array([0.0, 1.0]),
            np.array([1.0, 0.0]),
            NoiseGenerationConfig(window_size=(2, 2)),
        )
