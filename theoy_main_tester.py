import random
from datetime import datetime
from AVLTree import AVLTree


# -------------------- input generators --------------------

def generate_sorted(n):
    return list(range(n))


def generate_reverse_sorted(n):
    return list(range(n - 1, -1, -1))


def generate_random(n):
    arr = list(range(n))
    random.shuffle(arr)
    return arr


def generate_almost_sorted(n):
    """
    Start sorted. For each j=0..n-2, swap A[j] and A[j+1] with prob 1/2.
    Note: an element can be swapped multiple times (as required).
    """
    arr = list(range(n))
    for j in range(n - 1):
        if random.random() < 0.5:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# -------------------- AVL experiment --------------------

def run_single_experiment(arr):
    """
    Returns:
      total_edges    = sum of e returned by finger_insert
      total_promotes = sum of h returned by finger_insert
    """
    tree = AVLTree()
    total_edges = 0
    total_promotes = 0

    for key in arr:
        _, edges, promotes = tree.finger_insert(key, str(key))
        total_edges += edges
        total_promotes += promotes

    return total_edges, total_promotes


def average_edges_promotes(generator_func, n, runs):
    total_edges = 0.0
    total_promotes = 0.0
    for _ in range(runs):
        arr = generator_func(n)
        edges, promotes = run_single_experiment(arr)
        total_edges += edges
        total_promotes += promotes
    return total_edges / runs, total_promotes / runs


# -------------------- inversion counting (merge sort) --------------------

def count_inversions(arr):
    _, inv = _sort_and_count(arr)
    return inv


def _sort_and_count(a):
    n = len(a)
    if n <= 1:
        return a[:], 0
    mid = n // 2
    left, invL = _sort_and_count(a[:mid])
    right, invR = _sort_and_count(a[mid:])
    merged, invM = _merge_and_count(left, right)
    return merged, invL + invR + invM


def _merge_and_count(left, right):
    i = j = 0
    merged = []
    inv = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inv += (len(left) - i)
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inv


def average_inversions(generator_func, n, runs):
    total = 0.0
    for _ in range(runs):
        arr = generator_func(n)
        total += count_inversions(arr)
    return total / runs


# -------------------- output helpers --------------------

def write_results(output_path="results.txt", seed=None):
    """
    Writes results to output_path (OVERWRITES each run).
    Also prints to console.
    If seed is not None, uses deterministic randomness.
    """
    if seed is not None:
        random.seed(seed)

    RUNS_DET = 1
    RUNS_RAND = 20

    def header(title, out):
        out("")
        out(title)
        out("=" * len(title))

    def print_row(i, n, a, b, c, d, out, fmt="{:,.1f}"):
        out(
            f"{i:2d} | {n:6d} | "
            f"{fmt.format(a):>12} | {fmt.format(b):>12} | "
            f"{fmt.format(c):>12} | {fmt.format(d):>12}"
        )

    # "w" overwrites the file each time
    with open(output_path, "w", encoding="utf-8") as f:

        def out(line=""):
            print(line)
            f.write(line + "\n")

        out(f"RUN @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            + (f" | seed={seed}" if seed is not None else ""))

        promotes_results = {}
        edges_results = {}

        # ---------- Table 1: total balancing cost ----------
        header("Table 1: Total balancing cost (Σ promotes h)  [avg over runs]", out)
        out(" i |      n |       sorted |     reversed |       random | almost_sorted")
        out("-" * 79)

        for i in range(1, 11):
            n = 300 * (2 ** i)

            avg_edges_s, avg_prom_s = average_edges_promotes(generate_sorted, n, RUNS_DET)
            avg_edges_r, avg_prom_r = average_edges_promotes(generate_reverse_sorted, n, RUNS_DET)
            avg_edges_rand, avg_prom_rand = average_edges_promotes(generate_random, n, RUNS_RAND)
            avg_edges_al, avg_prom_al = average_edges_promotes(generate_almost_sorted, n, RUNS_RAND)

            promotes_results[n] = (avg_prom_s, avg_prom_r, avg_prom_rand, avg_prom_al)
            edges_results[n] = (avg_edges_s, avg_edges_r, avg_edges_rand, avg_edges_al)

            print_row(i, n, avg_prom_s, avg_prom_r, avg_prom_rand, avg_prom_al, out, fmt="{:,.1f}")

        # ---------- Table 2: inversions (up to i=5) ----------
        header("Table 2: Number of inversions (INV)  [avg over runs]", out)
        out(" i |      n |       sorted |     reversed |       random | almost_sorted")
        out("-" * 79)

        for i in range(1, 6):
            n = 300 * (2 ** i)

            inv_sorted = average_inversions(generate_sorted, n, RUNS_DET)
            inv_rev = average_inversions(generate_reverse_sorted, n, RUNS_DET)
            inv_rand = average_inversions(generate_random, n, RUNS_RAND)
            inv_almost = average_inversions(generate_almost_sorted, n, RUNS_RAND)

            print_row(i, n, inv_sorted, inv_rev, inv_rand, inv_almost, out, fmt="{:,.1f}")

        # ---------- Table 3: total search cost ----------
        header("Table 3: Total search cost (Σ edges e)  [avg over runs]", out)
        out(" i |      n |       sorted |     reversed |       random | almost_sorted")
        out("-" * 79)

        for i in range(1, 11):
            n = 300 * (2 ** i)
            avg_edges_s, avg_edges_r, avg_edges_rand, avg_edges_al = edges_results[n]
            print_row(i, n, avg_edges_s, avg_edges_r, avg_edges_rand, avg_edges_al, out, fmt="{:,.1f}")


def main():
    write_results(output_path="results.txt", seed=None)
    # For reproducible randomness:
    # write_results(output_path="results.txt", seed=12345)


if __name__ == "__main__":
    main()
