# Sorting Algorithm Benchmark

A Python script for comparing the execution speed of different sorting algorithms.

The program generates several types of input data, runs sorting algorithms against them, measures execution time, and calculates basic statistics.

## Sorting Algorithms

The benchmark currently includes:

- Python built-in `sort()`
- Python built-in `sorted()`
- Bubble Sort
- Insertion Sort
- Selection Sort
- Merge Sort
- Quick Sort
- Heap Sort

## Input Data Patterns

Each algorithm is tested against four different data patterns:

- **Chaos** – randomly generated numbers.
- **Reverse** – numbers sorted in descending order.
- **Almost** – mostly sorted numbers with a few misplaced elements.
- **Dizzy** – numbers shuffled in small groups.

## Benchmark Settings

The main settings can be adjusted at the beginning of the script:

- `LOW` / `HIGH` – range of generated numbers.
- `SIZE` – number of elements in each dataset.
- `TRIALS` – repetitions for faster algorithms.
- `TRIALS_SLOW` – repetitions for slower algorithms.

The script uses fewer repetitions for slower algorithms to keep execution time manageable.

## Results

For each algorithm and input pattern, the program calculates:

- Mean execution time
- Median execution time
- Standard deviation

Results are printed in the terminal and exported to:

`benchmark_sorting_output.json`

## Requirements

- Python 3
- NumPy

Install NumPy if necessary:

```bash
pip install numpy
```

## Run

```bash
python sorting_benchmark.py
```

**Note:** This is an experimental benchmarking project. Results can vary depending on hardware, system load, Python version, and benchmark settings.

Visualization of the results is planned as a separate module.
