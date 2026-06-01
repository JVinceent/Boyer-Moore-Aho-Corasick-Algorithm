# =============================================================================
# benchmark.py
# Hybrid Toxic Language Detection Pipeline
# Component 5 — Performance Benchmarking
# =============================================================================

import os
import sys
import time
import tracemalloc
import csv

# Ensure the parent directory is in the path to import pipeline components
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from normalizer import normalize
from boyer_moore import boyer_moore_full_scan
from aho_corasick import aho_corasick_scan
from hybrid import HybridPipeline
from test_cases import test_cases

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("WARNING: pandas not found. Please run 'pip install pandas openpyxl'")

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("WARNING: matplotlib not found. Graphs will not be generated.")

# =============================================================================
# CONFIGURATION & PATH SETUP
# =============================================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATASET_PATH = os.path.join(BASE_DIR, 'data', 'toxic_word_dataset_final.xlsx')

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results')
TABLES_DIR  = os.path.join(RESULTS_DIR, 'tables')
GRAPHS_DIR  = os.path.join(RESULTS_DIR, 'graphs')

os.makedirs(TABLES_DIR, exist_ok=True)
os.makedirs(GRAPHS_DIR, exist_ok=True)

# =============================================================================
# LOAD REAL DATASET
# =============================================================================
def load_dictionary(filepath: str) -> list:
    """Loads the toxic word dictionary from the Excel dataset."""
    if not PANDAS_AVAILABLE:
        print("Falling back to a small hardcoded dictionary due to missing pandas.")
        return ["gago", "bobo", "tanga", "ulol", "puta", "idiot", "trash"]
        
    try:
        # Assuming the words are in the first column or a column named 'Word'/'Keyword'
        df = pd.read_excel(filepath)
        
        # If your column is named differently (e.g., 'Toxic Term'), change 'Word' below:
        col_name = df.columns[0] # automatically picks the first column
        words = df[col_name].dropna().astype(str).tolist()
        return [w.lower().strip() for w in words if w.strip()]
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return []

# =============================================================================
# BENCHMARKING FUNCTIONS
# =============================================================================
def benchmark_approach(name: str, func, *args) -> dict:
    tracemalloc.start()
    start_time = time.perf_counter()
    
    func(*args)
    
    end_time = time.perf_counter()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "Approach": name,
        "Time_us": (end_time - start_time) * 1_000_000,
        "Memory_KB": peak_memory / 1024
    }

def run_benchmarks(cases: list, dictionary: list) -> list:
    results = []
    pipeline = HybridPipeline(dictionary)

    print("Running benchmarks...")
    
    for idx, tc in enumerate(cases):
        raw_msg = tc["message"]
        msg_type = tc["type"]
        is_toxic = tc["label"] == "toxic"
        
        normalized_msg = normalize(raw_msg)
        
        bm_res = benchmark_approach("Boyer-Moore", boyer_moore_full_scan, normalized_msg, dictionary)
        ac_res = benchmark_approach("Aho-Corasick", aho_corasick_scan, normalized_msg, dictionary)
        hybrid_res = benchmark_approach("Hybrid", pipeline.process, raw_msg)
        
        for res in [bm_res, ac_res, hybrid_res]:
            res["Test_ID"] = idx + 1
            res["Message_Type"] = msg_type
            res["Is_Toxic"] = is_toxic
            results.append(res)
            
    return results

# =============================================================================
# EXPORT & VISUALIZATION
# =============================================================================
def save_to_csv(results: list, filepath: str) -> None:
    keys = ["Test_ID", "Message_Type", "Is_Toxic", "Approach", "Time_us", "Memory_KB"]
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    print(f"Results saved to: {filepath}")

def generate_graphs(results: list) -> None:
    if not MATPLOTLIB_AVAILABLE:
        return

    approaches = ["Boyer-Moore", "Aho-Corasick", "Hybrid"]
    
    avg_times = []
    for approach in approaches:
        times = [r["Time_us"] for r in results if r["Approach"] == approach]
        avg_times.append(sum(times) / len(times))

    plt.figure(figsize=(8, 5))
    bars = plt.bar(approaches, avg_times, color=['#FF9999', '#66B2FF', '#99FF99'])
    
    plt.title('Average Execution Time per Algorithm (µs)')
    plt.ylabel('Execution Time (Microseconds)')
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + (yval * 0.02), 
                 f"{round(yval, 2)}", ha='center', va='bottom')

    graph_path = os.path.join(GRAPHS_DIR, 'average_execution_time.png')
    plt.savefig(graph_path)
    plt.close()
    print(f"Graphs generated in: {GRAPHS_DIR}")

# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    full_dictionary = load_dictionary(DATASET_PATH)

    print("=" * 65)
    print("HYBRID PIPELINE PERFORMANCE BENCHMARK")
    print("=" * 65)
    print(f"Total Test Cases Loaded : {len(test_cases)}")
    print(f"Dictionary Size         : {len(full_dictionary)}")
    print("-" * 65)

    if not full_dictionary:
        print("ERROR: Dictionary is empty. Halting benchmark.")
        sys.exit(1)

    benchmark_data = run_benchmarks(test_cases, full_dictionary)
    
    print("-" * 65)
    print(f"{'Approach':<15} | {'Avg Time (µs)':<15} | {'Avg Peak Memory (KB)':<20}")
    print("-" * 65)
    
    for approach in ["Boyer-Moore", "Aho-Corasick", "Hybrid"]:
        times = [r["Time_us"] for r in benchmark_data if r["Approach"] == approach]
        mems  = [r["Memory_KB"] for r in benchmark_data if r["Approach"] == approach]
        avg_time = sum(times) / len(times)
        avg_mem  = sum(mems) / len(mems)
        print(f"{approach:<15} | {avg_time:<15.2f} | {avg_mem:<20.2f}")
    
    print("=" * 65)

    csv_path = os.path.join(TABLES_DIR, 'benchmark_results.csv')
    save_to_csv(benchmark_data, csv_path)
    generate_graphs(benchmark_data)