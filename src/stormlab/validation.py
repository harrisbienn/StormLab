"""Validation helpers for package-facing StormLab APIs."""

from collections.abc import Sequence

import numpy as np


def as_array(name: str, value, ndim: int | None = None) -> np.ndarray:
    """Convert a value to a NumPy array and optionally check dimensionality."""

    array = np.asarray(value)
    if ndim is not None and array.ndim != ndim:
        raise ValueError(f"{name} must be {ndim}D, got shape {array.shape}.")
    return array


def require_same_shape(*named_arrays: tuple[str, np.ndarray]) -> None:
    """Require all named arrays to have identical shapes."""

    if not named_arrays:
        return

    expected_name, expected = named_arrays[0]
    for name, array in named_arrays[1:]:
        if array.shape != expected.shape:
            raise ValueError(
                f"{name} shape {array.shape} must match "
                f"{expected_name} shape {expected.shape}."
            )


def require_trailing_shape(name: str, array: np.ndarray, shape: Sequence[int]) -> None:
    """Require an array's trailing dimensions to match a known shape."""

    expected = tuple(shape)
    if array.shape[-len(expected):] != expected:
        raise ValueError(
            f"{name} trailing dimensions {array.shape[-len(expected):]} "
            f"must match {expected}."
        )


def validate_coordinates(lon_data, lat_data, spatial_shape: tuple[int, int]) -> tuple[np.ndarray, np.ndarray]:
    """Validate one-dimensional lon/lat coordinates against a lat-lon field shape."""

    lon_array = as_array("lon_data", lon_data, ndim=1)
    lat_array = as_array("lat_data", lat_data, ndim=1)
    expected_lat, expected_lon = spatial_shape

    if lat_array.shape[0] != expected_lat:
        raise ValueError(
            f"lat_data length {lat_array.shape[0]} must match field latitude size {expected_lat}."
        )
    if lon_array.shape[0] != expected_lon:
        raise ValueError(
            f"lon_data length {lon_array.shape[0]} must match field longitude size {expected_lon}."
        )
    return lon_array, lat_array


def validate_noise_inputs(prcp_array, acf_array, u_array, v_array, lon_data, lat_data):
    """Validate array shapes for noise generation."""

    prcp = as_array("prcp_array", prcp_array, ndim=3)
    acf = as_array("acf_array", acf_array, ndim=1)
    u = as_array("u_array", u_array, ndim=3)
    v = as_array("v_array", v_array, ndim=3)

    require_same_shape(("u_array", u), ("v_array", v), ("prcp_array", prcp))
    if acf.shape[0] != prcp.shape[0]:
        raise ValueError(
            f"acf_array length {acf.shape[0]} must match prcp_array time size {prcp.shape[0]}."
        )
    lon, lat = validate_coordinates(lon_data, lat_data, prcp.shape[1:])
    return prcp, acf, u, v, lon, lat


def validate_rainfall_inputs(
    noise_array,
    logic_mu_array,
    scipy_a_array,
    scipy_scale_array,
    scipy_gg_c_array,
):
    """Validate array shapes for rainfall simulation."""

    noise = as_array("noise_array", noise_array, ndim=3)
    wet_probability = as_array("logic_mu_array", logic_mu_array, ndim=3)
    gamma_shape = as_array("scipy_a_array", scipy_a_array, ndim=3)
    gamma_scale = as_array("scipy_scale_array", scipy_scale_array, ndim=3)
    gg_c = as_array("scipy_gg_c_array", scipy_gg_c_array)

    require_same_shape(
        ("logic_mu_array", wet_probability),
        ("noise_array", noise),
        ("scipy_a_array", gamma_shape),
        ("scipy_scale_array", gamma_scale),
    )
    if gg_c.ndim == 2:
        if gg_c.shape != noise.shape[1:]:
            raise ValueError(
                f"scipy_gg_c_array shape {gg_c.shape} must match spatial shape {noise.shape[1:]}."
            )
    elif gg_c.ndim == 3:
        if gg_c.shape != noise.shape:
            raise ValueError(
                f"scipy_gg_c_array shape {gg_c.shape} must match noise_array shape {noise.shape}."
            )
    else:
        raise ValueError(f"scipy_gg_c_array must be 2D or 3D, got shape {gg_c.shape}.")

    return noise, wet_probability, gamma_shape, gamma_scale, gg_c


def validate_tracking_inputs(ivt_array):
    """Validate IVT input shape for storm tracking."""

    return as_array("ivt_array", ivt_array, ndim=3)


def validate_matching_time_space(first_name: str, first, second_name: str, second) -> tuple[np.ndarray, np.ndarray]:
    """Validate two time-lat-lon arrays have the same shape."""

    first_array = as_array(first_name, first, ndim=3)
    second_array = as_array(second_name, second, ndim=3)
    require_same_shape((first_name, first_array), (second_name, second_array))
    return first_array, second_array
