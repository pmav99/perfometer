# Perfometer

Benchmark the execution time of python functions by dynamically adjusting the number of runs.

## Installation

There are no 3rd party dependencies.

```
poetry add -G dev 'git+https://github.com/pmav99/perfometer'
python -m pip install 'git+https://github.com/pmav99/perfometer'
uv pip install 'git+https://github.com/pmav99/perfometer'
```

## Features

- Benchmark the execution time of any Python function.
- Optionally include warmup runs (on by default).
- Control parameters such as allowed deviation and the confidence level.
- Measure timings using wall-time or process-time.
- Output descriptive statistics (e.g., mean, min, max, standard deviation).

## Notes

- This package is not suitable for microbenchmarks due to the potential overhead
  introduced by the measurement system.
- Warmup runs help mitigate issues caused by caching or JIT compilation.
- The `_allowed_deviation` and `_confidence_level` parameters ensure the benchmark
  reaches the desired statistical significance.

## Usage

### Benchmarking

The main function in the `perfometer` package is `benchmark()`. Here is an example of how to use it:

```python
import random
import time
import perfometer

def do_calc(sleep_time):
    jitter = random.uniform(0, 0.05)
    time.sleep(sleep_time + jitter)

timings = perfometer.benchmark(do_calc, 0.3, _allowed_deviation=0.01, _wall_time=True)
print(timings)
```

will output something like:

```
[0.33189456001855433,
 0.30625631200382486,
 0.31478919298388064,
 0.3210337000200525,
 0.3467220180318691,
 0.30861941300099716,
 0.3299146000063047,
 0.3299472130020149]
```

### Analyzing results

You can use `describe_timings()` to get a summary of these timings:

```python
timing_stats = perfometer.describe_timings(timings)
print(timing_stats)
```

which will print:

```json
{
  "count": 8,
  "min": 0.30625631200382486,
  "max": 0.3467220180318691,
  "mean": 0.32364712613343727,
  "stdev": 0.013591008997159886,
  "total": 2.589177009067498
}
```

### Comparing runtime performance

If you want to compare the performance of multiple function, it is quite convenient to compare them using pandas:

```python
import pandas as pd

df = pd.DataFrame({
    "func1": perfometer.describe_timings(func1_timings),
    "func2": perfometer.describe_timings(func2_timings),
    "func3": perfometer.describe_timings(func3_timings),
}).T
```

which will output something like this:

```python
       count       min       max      mean     stdev     total
func1    8.0  0.306256  0.346722  0.323647  0.013591  2.589177
func2    6.0  0.407999  0.437488  0.423678  0.011938  2.542071
func3    9.0  0.205959  0.245123  0.229371  0.014514  2.064338
```

## License

This package is licensed under the MIT License.
