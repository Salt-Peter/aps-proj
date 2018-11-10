import timeit

import kruskal_impl.kruskal_list_sort as kruskal_list_sort
import kruskal_impl.kruskal_veb as kruskal_veb
import kruskal_impl.kruskal_fib_heap as kruskal_fib_heap


def timeit_kruskal_list_sort(V, E, edges):
    g = kruskal_list_sort.Graph(V)
    for edge in edges:
        u, v, w = edge
        g.insert_edge(u, v, w)

    g.kruskal()


def timeit_kruskal_veb(V, E, edges):
    g = kruskal_veb.Graph(V)
    for edge in edges:
        u, v, w = edge
        g.insert_edge(u, v, w)

    g.kruskal()


def timeit_kruskal_fib_heap(V, E, edges):
    g = kruskal_fib_heap.Graph(V)
    for edge in edges:
        u, v, w = edge
        g.insert_edge(u, v, w)

    g.kruskal()


def plotter(num_list, x_list, y_list, z_list):
    import matplotlib.pyplot as plt

    plt.plot(num_list, x_list, label="Default")
    plt.plot(num_list, y_list, label="vEB Tree impl")
    plt.plot(num_list, z_list, label="Fibonacci heap impl")
    plt.legend(loc=0)
    plt.title("Comparison")
    plt.xlabel("Input size")
    plt.ylabel("Time taken")
    plt.show()


if __name__ == "__main__":
    # setup code
    files = [
        "tests/input/1",
        "tests/input/2",
        "tests/input/3",
        "tests/input/4",
        "tests/input/5",
        "tests/input/6",
        "tests/input/7",
        "tests/input/8",
        "tests/input/9",
        "tests/input/10",
    ]
    num_list = [10, 21, 55, 105, 153, 300, 630, 1225, 2556, 4950]
    x_list, y_list, z_list = [], [], []

    for filename in files:
        fp = open(filename)
        V, E = map(int, fp.readline().split())
        edges = []
        for _ in range(E):
            u, v, w = map(int, fp.readline().split())
            edges.append((u, v, w))
        fp.close()

        num = 100

        x = timeit.Timer('timeit_kruskal_list_sort(V,E,edges)',
                         setup="from __main__ import timeit_kruskal_list_sort",
                         globals=globals()).timeit(number=num)
        print(x)
        x_list.append(x)

        y = timeit.Timer('timeit_kruskal_veb(V,E,edges)',
                         setup="from __main__ import timeit_kruskal_veb",
                         globals=globals()).timeit(number=num)
        print(y)
        y_list.append(y)

        z = timeit.Timer('timeit_kruskal_fib_heap(V,E,edges)',
                         setup="from __main__ import timeit_kruskal_fib_heap",
                         globals=globals()).timeit(number=num)
        print(z)
        z_list.append(z)

        print()

    plotter(num_list, x_list, y_list, z_list)
