"""Benchmark harness for Bubble Sort vs Quicksort (scaffold).

This script generates datasets, times the two algorithms, saves results to CSV,
and produces a performance plot. The algorithm implementations are intentionally
left as stubs in `algorithms/` — the benchmark will skip algorithms that raise
`NotImplementedError`.
"""

import argparse
import copy
import os
import time
from typing import List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from algorithms.sort_bubble import bubble_sort
from algorithms.sort_quick import quicksort


def generate_dataset(n: int, dtype: str) -> List[int]:
    if dtype == 'random':
        return np.random.randint(0, max(1, n * 10), size=n).tolist()
    if dtype == 'sorted':
        return list(range(n))
    if dtype == 'reversed':
        return list(range(n, 0, -1))
    raise ValueError(f'Unknown dataset type: {dtype}')


def time_function(func, arr: List[int], trials: int) -> Tuple[float, float]:
    times = []
    for _ in range(trials):
        a = list(arr)
        t0 = time.perf_counter()
        try:
            func(a)
        except NotImplementedError:
            return None
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return float(np.mean(times)), float(np.std(times))


def main():
    parser = argparse.ArgumentParser(description='Benchmark sorts (scaffold)')
    parser.add_argument('--trials', type=int, default=5)
    parser.add_argument('--output-csv', default='analysis/sort_results.csv')
    parser.add_argument('--output-plot', default='graph/sort_performance.png')
    args = parser.parse_args()

    sizes = [100, 500, 1000, 5000, 10000]
    dtypes = ['random', 'sorted', 'reversed']
    algorithms = [
        ('bubble', bubble_sort),
        ('quick', quicksort),
    ]

    results = []

    for alg_name, alg_func in algorithms:
        for dtype in dtypes:
            for n in sizes:
                arr = generate_dataset(n, dtype)
                res = time_function(alg_func, arr, args.trials)
                if res is None:
                    print(f"Skipping {alg_name} for n={n}, type={dtype} (not implemented)")
                    results.append({
                        'algorithm': alg_name,
                        'dtype': dtype,
                        'n': n,
                        'mean_time': None,
                        'std_time': None,
                        'skipped': True,
                    })
                    continue

                mean_t, std_t = res
                print(f"{alg_name} | {dtype} | n={n} -> mean={mean_t:.6f}s std={std_t:.6f}s")
                results.append({
                    'algorithm': alg_name,
                    'dtype': dtype,
                    'n': n,
                    'mean_time': mean_t,
                    'std_time': std_t,
                    'skipped': False,
                })

    df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(args.output_csv), exist_ok=True)
    df.to_csv(args.output_csv, index=False)
    print(f"Saved results to {args.output_csv}")

    # Plotting: one plot per dataset type
    os.makedirs(os.path.dirname(args.output_plot), exist_ok=True)
    plt.figure(figsize=(10, 6))
    markers = {'bubble': 'o', 'quick': 's'}
    for dtype in dtypes:
        for alg_name, _ in algorithms:
            sub = df[(df['algorithm'] == alg_name) & (df['dtype'] == dtype) & (df['skipped'] == False)]
            if sub.empty:
                continue
            plt.plot(sub['n'], sub['mean_time'], marker=markers.get(alg_name, 'o'), label=f"{alg_name} ({dtype})")

    plt.xlabel('Input size n')
    plt.ylabel('Mean time (s)')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.grid(True, which='both', ls='--', alpha=0.6)
    plt.title('Sort Performance (mean time)')
    plt.tight_layout()
    plt.savefig(args.output_plot)
    print(f"Saved plot to {args.output_plot}")


if __name__ == '__main__':
    main()
