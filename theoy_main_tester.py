import random

from AVLTree import AVLTree

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


def main():
    print("i | n | sorted | reversed | random | almost_sorted")
    print("-" * 65)

    for i in range(1, 11):
        n = 300 * (2 ** i)

        # 1. sorted
        sorted_arr = generate_sorted(n)
        _, promotes_sorted = run_single_experiment(sorted_arr)

        # 2. reverse sorted
        reversed_arr = generate_reverse_sorted(n)
        _, promotes_reversed = run_single_experiment(reversed_arr)

        # 3. random (avg of 20)
        promotes_random_sum = 0
        for _ in range(20):
            arr = generate_random(n)
            _, promotes = run_single_experiment(arr)
            promotes_random_sum += promotes
        promotes_random_avg = promotes_random_sum / 20.0

        # 4. almost sorted (avg of 20)
        promotes_almost_sum = 0
        for _ in range(20):
            arr = generate_almost_sorted(n)
            _, promotes = run_single_experiment(arr)
            promotes_almost_sum += promotes
        promotes_almost_avg = promotes_almost_sum / 20.0

        print(
            "{:2d} | {:5d} | {:6d} | {:8d} | {:6.1f} | {:6.1f}".format(
                i,
                n,
                promotes_sorted,
                promotes_reversed,
                promotes_random_avg,
                promotes_almost_avg,
            )
        )


if __name__ == "__main__":
    main()
