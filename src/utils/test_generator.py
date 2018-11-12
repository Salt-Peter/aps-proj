import random


def generate(V, E, max_weight=None):
    print(V, E)  # writes: V E
    count = 0
    while count < E:
        w = random.randint(1, max_weight or E - 1)  # generate random weight in the range [1 ... E-1]
        u = random.randint(0, V - 1)
        v = random.randint(0, V - 1)
        print(u, v, w)
        count += 1


def generate_sparse(V):
    E = V - 1
    generate(V, E)


def generate_dense(V, max_weight):
    E = V * (V - 1) // 2
    generate(V, E, max_weight)


if __name__ == "__main__":
    import sys

    filename = input("Enter file name in which to write: ")
    V = int(input("Enter number of vertices of graph: "))
    max_weight = int(input("Enter maximum edge weight: "))
    if filename:
        sys.stdout = open(filename, 'wt')
        generate_dense(V, max_weight)
