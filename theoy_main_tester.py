import random

from AVLTree import AVLTree

import random


def generate_sorted(n):
    return list(range(n))


def generate_reverse_sorted(n):
    return list(range(n - 1, -1, -1))


def generate_random(n):
    arr = list(range(n))
    random.shuffle(arr)
    return arr


def generate_almost_sorted(n):
    arr = list(range(n))
    for i in range(n - 1):
        if random.random() < 0.5:
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return arr


def run_single_experiment(arr):
    tree = AVLTree()
    total_edges = 0
    total_promotes = 0

    for key in arr:
        _, edges, promotes = tree.finger_insert(key, str(key))
        total_edges += edges
        total_promotes += promotes

    return total_edges, total_promotes


def average_promotes(generator_func, n, runs=20):
    total = 0.0
    for _ in range(runs):
        arr = generator_func(n)
        _, promotes = run_single_experiment(arr)
        total += promotes
    return total / runs


def main():
    print("i | n | sorted | reversed | random | almost_sorted")
    print("-" * 65)

    for i in range(1, 11):
        n = 300 * (2 ** i)

        avg_sorted = average_promotes(generate_sorted, n)
        avg_reversed = average_promotes(generate_reverse_sorted, n)
        avg_random = average_promotes(generate_random, n)
        avg_almost = average_promotes(generate_almost_sorted, n)

        print(
            "{:2d} | {:5d} | {:6.1f} | {:8.1f} | {:6.1f} | {:6.1f}".format(
                i,
                n,
                avg_sorted,
                avg_reversed,
                avg_random,
                avg_almost,
            )
        )


if __name__ == "__main__":
    main()
