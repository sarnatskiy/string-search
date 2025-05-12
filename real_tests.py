import time
import math
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from algorithms import naive_search, kmp_search, boyer_moore_search, rabin_karp_search
from generate_real_cases import generate_test_case


def measure_performance(algorithm: callable, text: str, pattern: str, runs: int = 11) -> tuple[dict, list[int]]:
    # Прогрев
    for _ in range(3):
        algorithm(text, pattern)

    times = []
    for _ in range(runs):
        start = time.perf_counter_ns()
        algorithm(text, pattern)
        end = time.perf_counter_ns()
        times.append(end - start)

    avg = sum(times) / runs
    stats = {
        'avg_time_ns': avg,
        'min_time_ns': min(times),
        'max_time_ns': max(times),
        'std_dev_ns': math.sqrt(sum((t - avg) ** 2 for t in times) / runs),
        'runs': runs
    }

    return stats, times


def run_single_test(algo_name: str, algo_func: callable, size: int, case_type: str):
    try:
        text, pattern = generate_test_case(size, case_type, algo_name)
        stats, times = measure_performance(algo_func, text, pattern, 30)

        summary_result = {
            'algorithm': algo_name,
            'data_size_bytes': size,
            'case_type': case_type,
            'pattern_length': len(pattern),
            **stats
        }

        per_run_results = []
        for run_idx, t in enumerate(times):
            per_run_results.append({
                'algorithm': algo_name,
                'data_size_bytes': size,
                'case_type': case_type,
                'pattern_length': len(pattern),
                'run_index': run_idx + 1,
                'time_ns': t
            })

        print(f"{algo_name:12} | size={size:8} | case={case_type:6} | "
              f"avg={stats['avg_time_ns'] / 1e9:.6f}s ± {stats['std_dev_ns'] / 1e9:.6f}s "
              f"(min={stats['min_time_ns'] / 1e9:.6f}s, max={stats['max_time_ns'] / 1e9:.6f}s)")

        return summary_result, per_run_results

    except Exception as e:
        print(f"Error in {algo_name} with size {size} ({case_type}): {str(e)}")
        return None


def run_benchmark():
    algorithms = {
        'naive': naive_search,
        'kmp': kmp_search,
        'boyer_moore': boyer_moore_search,
        'rabin_karp': rabin_karp_search
    }

    sizes = [
        1_000, 10_000, 100_000, 1_000_000,
        10_000_000, 100_000_000, 500_000_000
    ]

    case_types = ['best', 'worst', 'random']
    summary_results = []
    per_run_results = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for algo_name, algo_func in algorithms.items():
            for size in sizes:
                for case_type in case_types:
                    futures.append(
                        executor.submit(
                            run_single_test,
                            algo_name,
                            algo_func,
                            size,
                            case_type
                        )
                    )

        for future in as_completed(futures):
            result = future.result()
            if result:
                summary_result, per_run_result = result
                summary_results.append(summary_result)
                per_run_results.extend(per_run_result)

    df_summary = pd.DataFrame(summary_results)
    df_runs = pd.DataFrame(per_run_results)

    df_summary.to_csv('substring_search_benchmark_summary.csv', index=False)
    df_runs.to_csv('substring_search_benchmark_runs.csv', index=False)

    print("\nSummary results saved to substring_search_benchmark_summary.csv")
    print("Per-run results saved to substring_search_benchmark_runs.csv")


if __name__ == "__main__":
    run_benchmark()
