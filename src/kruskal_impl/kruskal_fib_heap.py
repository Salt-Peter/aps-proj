from datastructures.fibonacci_heap import FibonacciHeap


class Graph:
    def __init__(self, vertices):
        self.V = vertices  # vertices
        # List to store graph in the (u,v,w) form ,
        # which indicates a weighted edge incident to nodes u and v
        self.edges = FibonacciHeap()

    # This function inserts a new edge to the graph
    def insert_edge(self, u, v, w):
        self.edges.insert((w, u, v))

    # Find_set implementation using Path compression heuristic
    def find(self, parent, i):
        """Returns parent of current node."""
        if parent[i] == i:
            return i

        parent[i] = self.find(parent, parent[i])  # Recursively updates the parent of each node hence path compression.
        return parent[i]

    # Application of Union by rank heuristic
    def union(self, parent, rank, x, y):
        x_parent = self.find(parent, x)
        y_parent = self.find(parent, y)

        # If sets have same rank then increment the rank of the set by 1
        if rank[x_parent] == rank[y_parent]:
            parent[y_parent] = x_parent
            rank[x_parent] += 1

        # Smaller ranked set is added with larger ranked set ,no need to increase the rank as the height remains same
        if rank[x_parent] < rank[y_parent]:
            parent[x_parent] = y_parent
        elif rank[x_parent] > rank[y_parent]:
            parent[y_parent] = x_parent

    def print_parent(self, parent):
        for i in range(len(parent)):
            print(parent[i], ",", end=" ")
        print()

    def kruskal(self):
        mst = []  # This will store the resulting Minimum Spanning Tree

        rank = [0] * self.V  # Initialize each node's rank as 0
        parent = [i for i in range(self.V)]  # set each node's parent as itself

        index = 0  # an index to iterate over sorted edges of the graph
        mst_index = 0  # an index to write data into mst

        # We pick the V-1 edges from the sorted edges in graph
        while mst_index < self.V - 1:

            # Pick the smallest edge and increment index for next iteration
            w, u, v, = self.edges.extract_min().data
            index += 1
            u_parent = self.find(parent, u)
            v_parent = self.find(parent, v)

            # g.print_parent(parent)

            # If including this edge does not form a cycle
            if u_parent != v_parent:
                # include it in result
                mst.append((u, v, w))
                mst_index += 1  # increment index for next iteration
                self.union(parent, rank, u_parent, v_parent)

            # else discard this edge

        # Print the Minimum cost spanning tree
        # print("The minimum spanning tree is as follows")
        cost = 0
        for u, v, weight in mst:
            # print("%d -- %d == %d" % (u, v, weight))
            cost += weight

        return cost
        # g.print_parent(parent)


if __name__ == "__main__":
    V, E = map(int, input().split())
    g = Graph(V)
    for _ in range(E):
        u, v, w = map(int, input().split())
        g.insert_edge(u, v, w)

    print(g.kruskal())
