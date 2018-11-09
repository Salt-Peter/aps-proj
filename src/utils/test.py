import kruskal_list_sort as kruskal, kruskal_veb as kruskal_veb


def test():
    pass


def test_kruskal(V, E, edges):
    g = kruskal.Graph(V)
    for _ in range(E):
        for edge in edges:
            u, v, w = edge
            g.insert_edge(u, v, w)

    return g.kruskal()


def test_kruskal_veb(V, E, edges):
    g = kruskal_veb.Graph(V)
    for _ in range(E):
        for edge in edges:
            u, v, w = edge
            g.insert_edge(u, v, w)

    return g.kruskal()


if __name__ == "__main__":
    counter = 0
    while True:
        # counter += 1
        V = 100
        E = V * (V - 1) // 2
        edges = []

        # generate input
        for _ in range(E):
            import random

            w = random.randint(1, 1023)
            u = random.randint(0, V - 1)
            v = random.randint(0, V - 1)
            edges.append((u, v, w))

            with open("junk/" + str(counter), "wt") as fp:
                print(V, E, file=fp)
                for edge in edges:
                    u, v, w = edge
                    print(u, v, w, file=fp)

        r1 = r2 = 0
        try:
            r1 = test_kruskal(V, E, edges)
        except IndexError:
            continue

        try:
            r2 = test_kruskal_veb(V, E, edges)
            print(V, E)

        except IndexError:
            print(V, E)
            for edge in edges:
                print(edge)
            break

        if r1 != r2:
            print("Different")
            break
        else:
            print("same")
            break
