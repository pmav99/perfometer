from __future__ import annotations

import importlib.metadata

from ._core import benchmark
from ._core import describe_timings
from ._core import get_z_value
from ._core import get_required_sample_size

__version__ = importlib.metadata.version(__name__)


__all__: list[str] = [
    "benchmark",
    "describe_timings",
    "get_z_value",
    "get_required_sample_size",
    "__version__",
]
