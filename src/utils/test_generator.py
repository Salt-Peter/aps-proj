import random


def generate(V, E):
    print(V, E)  # writes: V E
    count = 0
    while count < E:
        w = random.randint(1, 1023)  # generate weight
        u = random.randint(0, V - 1)
        v = random.randint(0, V - 1)
        print(u, v, w)
        count += 1


def generate_sparse(V):
    E = V - 1
    generate(V, E)


def generate_dense(V):
    E = V * (V - 1) // 2
    generate(V, E)


if __name__ == "__main__":
    import sys

    filename = input("Enter file name in which to write.")
    if filename:
        sys.stdout = open("tests/input/" + filename, 'wt')
        generate_dense(4)
