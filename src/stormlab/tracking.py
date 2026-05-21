"""Storm tracking entry points."""

from tracking import attach_precipitation as _attach_precipitation
from tracking import rainstorm_tracking as _rainstorm_tracking

from .config import TrackingConfig
from .validation import validate_matching_time_space, validate_tracking_inputs


def track_rainstorms(ivt_array, config: TrackingConfig | None = None):
    """Identify and track IVT/rainstorm objects using a typed configuration."""

    config = config or TrackingConfig()
    ivt = validate_tracking_inputs(ivt_array)
    return _rainstorm_tracking(
        ivt,
        low_threshold=config.low_threshold,
        high_threshold=config.high_threshold,
        morph_radius=config.morph_radius,
        expand_distance=config.expand_distance,
        overlap_ratio=config.overlap_ratio,
        dry_spell_time=config.dry_spell_time,
    )


def attach_precipitation_events(prcp_array, track_array):
    """Attach precipitation regions to tracked events after checking array shapes."""

    prcp, tracks = validate_matching_time_space(
        "prcp_array",
        prcp_array,
        "track_array",
        track_array,
    )
    return _attach_precipitation(prcp, tracks)


rainstorm_tracking = _rainstorm_tracking
attach_precipitation = _attach_precipitation

__all__ = [
    "TrackingConfig",
    "attach_precipitation",
    "attach_precipitation_events",
    "rainstorm_tracking",
    "track_rainstorms",
]
