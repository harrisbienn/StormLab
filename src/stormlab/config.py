"""Configuration objects for pipeline-facing StormLab calls."""

from dataclasses import dataclass


@dataclass(frozen=True)
class NoiseGenerationConfig:
    """Parameters for generating correlated Gaussian noise fields."""

    window_size: tuple[int, int] = (128, 128)
    overlap_ratio: float = 0.3
    ssft_war_thr: float = 0.1
    seed: int | None = 1

    def __post_init__(self) -> None:
        if len(self.window_size) != 2:
            raise ValueError("window_size must contain two integers: (lat_window, lon_window).")
        if self.window_size[0] <= 0 or self.window_size[1] <= 0:
            raise ValueError("window_size values must be positive.")
        if not 0 <= self.overlap_ratio < 1:
            raise ValueError("overlap_ratio must be in the interval [0, 1).")
        if not 0 <= self.ssft_war_thr <= 1:
            raise ValueError("ssft_war_thr must be in the interval [0, 1].")


@dataclass(frozen=True)
class TrackingConfig:
    """Parameters for identifying and tracking IVT/rainstorm objects."""

    low_threshold: float = 250
    high_threshold: float = 500
    morph_radius: int = 1
    expand_distance: int = 5
    overlap_ratio: float = 0.2
    dry_spell_time: int = 0

    def __post_init__(self) -> None:
        if self.low_threshold > self.high_threshold:
            raise ValueError("low_threshold must be less than or equal to high_threshold.")
        if self.morph_radius <= 0:
            raise ValueError("morph_radius must be positive.")
        if self.expand_distance < 0:
            raise ValueError("expand_distance must be nonnegative.")
        if self.overlap_ratio < 0:
            raise ValueError("overlap_ratio must be nonnegative.")
        if self.dry_spell_time < 0:
            raise ValueError("dry_spell_time must be nonnegative.")
