# comparison of performance of kruskal vEB Tree with constant tree size(u); u =1024
import time


def timeit_kruskal_list_sort(V, E, edges):
    x_start = time.process_time()

    g = kruskal_list_sort.Graph(V)
    for edge in edges:
        u, v, w = edge
        g.insert_edge(u, v, w)

    g.kruskal()
    x_end = time.process_time()
    print("List sort impl", x_end - x_start)
    return x_end - x_start


def timeit_kruskal_veb(V, E, edges):
    g = kruskal_veb.Graph(V)

    x_start = time.process_time()
    for edge in edges:
        u, v, w = edge
        g.insert_edge(u, v, w)

    g.kruskal()
    x_end = time.process_time()
    print("vEB Tree impl", x_end - x_start)
    return x_end - x_start


def timeit_kruskal_fib_heap(V, E, edges):
    x_start = time.perf_counter()

    g = kruskal_fib_heap.Graph(V)
    for edge in edges:
        u, v, w = edge
        g.insert_edge(u, v, w)

    g.kruskal()

    x_end = time.perf_counter()
    print("Fib heap", x_end - x_start)
    return x_end - x_start


def plotter(num_list, x_list, y_list, z_list):
    import matplotlib.pyplot as plt

    plt.plot(num_list, x_list, label="Kruskal implemented by sorting edges")
    plt.plot(num_list, y_list, label="Kruskal implemented using vEB Tree of universe size 1024")
    plt.plot(num_list, z_list, label="Kruskal implemented using Fibonacci heap")
    plt.legend(loc=0)
    plt.title("Comparison of various kruskal implementations")
    plt.xlabel("Input size (number of edges)")
    plt.ylabel("Time taken (in seconds)")
    plt.show()


if __name__ == "__main__":
    from kruskal_impl import kruskal_veb, kruskal_list_sort, kruskal_fib_heap

    # setup code
    num_list = []
    x_list, y_list, z_list = [], [], []
    NUM_TEST_CASES = 11

    for i in range(1, NUM_TEST_CASES + 1):
        fp = open("tests/input/" + str(i))
        V, E = map(int, fp.readline().split())
        edges = []
        num_list.append(E)
        for _ in range(E):
            u, v, w = map(int, fp.readline().split())
            edges.append((u, v, w))
        fp.close()

        print("\nTest case: ", i)
        x_list.append(timeit_kruskal_list_sort(V, E, edges))
        y_list.append(timeit_kruskal_veb(V, E, edges))
        z_list.append(timeit_kruskal_fib_heap(V, E, edges))

    plotter(num_list, x_list, y_list, z_list)
else:
    from .kruskal_impl import kruskal_veb, kruskal_list_sort, kruskal_fib_heap
