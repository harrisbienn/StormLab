"""Rainfall simulation entry points."""

from simulation import rainfall_simulation as _rainfall_simulation

from .validation import validate_rainfall_inputs


def simulate_rainfall(
    noise_array,
    logic_mu_array,
    scipy_a_array,
    scipy_scale_array,
    scipy_gg_c_array,
):
    """Generate rainfall fields after validating the simulation inputs."""

    noise, wet_probability, gamma_shape, gamma_scale, gg_c = validate_rainfall_inputs(
        noise_array,
        logic_mu_array,
        scipy_a_array,
        scipy_scale_array,
        scipy_gg_c_array,
    )
    return _rainfall_simulation(noise, wet_probability, gamma_shape, gamma_scale, gg_c)


rainfall_simulation = _rainfall_simulation

__all__ = ["rainfall_simulation", "simulate_rainfall"]
