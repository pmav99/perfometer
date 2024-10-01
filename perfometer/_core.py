from __future__ import annotations

import math
import statistics
import time
import typing as T

_NORMAL_DISTRIBUTION = statistics.NormalDist()


def get_z_value(confidence_level: float) -> float:
    z_value: float = _NORMAL_DISTRIBUTION.inv_cdf((1 + confidence_level) / 2)
    return z_value


def get_required_sample_size(
    data: T.Collection[float],
    allowed_deviation: float,
    confidence_level: float = 0.95,
) -> int:
    z_value = get_z_value(confidence_level)
    std_dev = statistics.stdev(data)
    required_sample_size = (z_value * std_dev / allowed_deviation) ** 2
    required_sample_size = max(2, math.ceil(required_sample_size))
    return required_sample_size


def benchmark(
    func: T.Callable[..., T.Any],
    *args: T.Any,
    _allowed_deviation: float = 0.1,
    _confidence_level: float = 0.95,
    _warmup: bool = True,
    _min_runs: int = 3,
    _max_time: float = 600,
    _wall_time: bool = False,
    **kwargs: T.Any,
) -> list[float]:
    """Benchmark the execution time of a given function.

    Note:
        This is not suitable for microbenchmarks!

    This function repeatedly executes the specified function and measures its execution time,
    returning a list of recorded timings. It supports warmup runs and allows for configuration
    of minimum runs while enforcing a maximum total execution time. The benchmarking can be
    performed using either wall clock time or process time based on the `_wall_time` parameter.

    The warmup run is designed to mitigate any initial overhead due to caching or JIT compilation.
    The function continues running until the required sample size, determined by the allowed
    deviation and confidence level, is achieved.

    Arguments prefixed with an underscore (e.g., `_allowed_deviation`) are used to avoid name
    clashes with the arguments of the function being benchmarked (`func`).

    Args:
        func (T.Callable[..., T.Any]): The function to benchmark.
        *args (T.Any): Positional arguments to pass to `func`.
        _allowed_deviation (float, optional): Allowed deviation for sample size calculation (default: 0.1).
        _confidence_level (float, optional): Confidence level for sample size calculation (default: 0.95).
        _warmup (bool, optional): If True, performs a warmup run (default: True).
        _min_runs (int, optional): Minimum number of runs to execute (default: 3).
        _max_time (float, optional): Maximum allowed total execution time in seconds (default: 600).
        _wall_time (bool, optional): If True, uses wall time for measurements; if False, uses process time (default: False).
        **kwargs (T.Any): Keyword arguments to pass to `func`.

    Returns:
        list[float]: A list containing the recorded execution times for each run of `func`.

    Raises:
        ValueError: If the total execution time exceeds `_max_time`.

    """

    def check_max_time() -> None:
        total_time = sum(timings)
        if total_time > _max_time:
            raise ValueError(f"Exceeded maximum allowed time: {total_time} > {_max_time}")

    def run() -> None:
        start = timer()
        func(*args, **kwargs)
        end = timer()
        timings.append(end - start)
        check_max_time()

    if _wall_time:
        timer = time.perf_counter
    else:
        timer = time.process_time

    timings: list[float] = []
    for _ in range(_min_runs + _warmup):
        run()

    if _warmup:
        timings = timings[1:]

    while len(timings) < get_required_sample_size(timings, _allowed_deviation, _confidence_level):
        run()

    return timings


def describe_timings(timings: T.Sequence[float]) -> dict[str, float]:
    """
    Provides descriptive statistics for a sequence of timing values.

    Args:
        timings: A sequence of floating-point numbers representing timing measurements or data points.

    Returns:
        dict[str, float]: A dictionary containing the following descriptive statistics:
            - "count": The number of elements in the sequence.
            - "min": The minimum value in the sequence.
            - "max": The maximum value in the sequence.
            - "mean": The arithmetic mean of the values.
            - "stdev": The standard deviation of the values.
            - "total": The sum of the values in the sequence.
    """
    return {
        "count": len(timings),
        "min": min(timings),
        "max": max(timings),
        "mean": statistics.mean(timings),
        "stdev": statistics.stdev(timings),
        "total": sum(timings),
    }
