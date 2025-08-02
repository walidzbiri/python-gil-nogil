import concurrent.futures
import contextlib
import os
from typing import Generator
import time
import sys
import json
from datetime import datetime


NB_ITERATIONS= 100_000_000
NB_TASKS= 20

@contextlib.contextmanager
def time_it(what: str) -> Generator[None, None, None]:
    t0 = time.monotonic()
    try:
        yield
    finally:
        elapsed = time.monotonic() - t0
        print(f"{what} took {elapsed:.4f}s")
        return elapsed

def do_work() -> int:
    with time_it("work"):
        x = 0
        for _ in range(NB_ITERATIONS):
            x += 1
        return x

def run_benchmark(number_of_threads: int = 4, scenario_name: str = "benchmark") -> dict:
    print(f"\n=== Running {scenario_name} scenario ===")
    
    start_time = time.monotonic()
    
    with concurrent.futures.ThreadPoolExecutor(number_of_threads) as pool:
        futures = [pool.submit(do_work) for _ in range(NB_TASKS)]
        
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            result = future.result()
            print(f"Task {i+1} completed: result={result}")
    
    total_time = time.monotonic() - start_time
    throughput = NB_TASKS / total_time
    
    result = {
        'scenario': scenario_name,
        'threads': number_of_threads,
        'total_time': total_time,
        'throughput': throughput,
    }
    
    print(f"Total time: {total_time:.4f}s, Throughput: {throughput:.2f} tasks/sec")
    return result

def create_simple_chart(results: list[dict]):
    print("\n" + "="*60)
    print("BENCHMARK RESULTS")
    print("="*60)
    
    # Time comparison
    print("\n📊 EXECUTION TIME COMPARISON")
    print("-" * 40)
    max_time = max(r['total_time'] for r in results)
    for result in results:
        bar_length = int((result['total_time'] / max_time) * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)
        print(f"{result['scenario']:20} │{bar}│ {result['total_time']:6.2f}s")
    
    # Throughput comparison  
    print("\n🚀 THROUGHPUT COMPARISON")
    print("-" * 40)
    max_throughput = max(r['throughput'] for r in results)
    for result in results:
        bar_length = int((result['throughput'] / max_throughput) * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)
        print(f"{result['scenario']:20} │{bar}│ {result['throughput']:6.1f} tasks/s")
    
    # Speedup analysis
    print("\n⚡ SPEEDUP ANALYSIS")
    print("-" * 40)
    single_thread_time = next((r['total_time'] for r in results if r['threads'] == 1), None)
    if single_thread_time:
        print("Scenario             Threads  Speedup")
        print("-" * 40)
        for result in results:
            speedup = single_thread_time / result['total_time']
            print(f"{result['scenario']:20} {result['threads']:7d} {speedup:7.2f}x")

def save_results(results: list[dict]):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'benchmark_results_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'python_version': sys.version,
            'platform': sys.platform,
            'GIL': sys._is_gil_enabled(),
            'cpu_count': os.cpu_count(),
            'tasks': NB_TASKS,
            'results': results
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: {filename}")

def main():
    print("🧪 Simple GIL Benchmark Tool")
    print(f"Testing with {NB_TASKS} tasks of {NB_ITERATIONS} iterations each")

    results = []
    
    # Test scenarios
    scenarios = [
        (1, "Single Thread"),
        (2, "2 Threads"), 
        (4, "4 Threads"),
        (8, "8 Threads"),
    ]
    
    for num_threads, scenario_name in scenarios:
        try:
            result = run_benchmark(num_threads, scenario_name)
            results.append(result)
            time.sleep(1)  # Brief pause between tests
        except Exception as e:
            print(f"Error in {scenario_name}: {e}")
    
    if results:
        create_simple_chart(results)
        save_results(results)
        print(f"\n✅ Completed {len(results)} benchmark scenarios")

    else:
        print("❌ No benchmarks completed successfully")

if __name__ == "__main__":
    main()