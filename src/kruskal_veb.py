from vEB_with_dups_n_satellite import VEBTree, INSERT, MINIMUM, GET_SATELLITE, DELETE
import math


# In order to implement Kruskal using vEB tree we need to know the range of keys beforehand
# for implementing Kruskal we will use the edge weights as the keys.
# So we need to know thw maximum possible edge weight beforehand
# Let us assume that the maximum possible weight is 1023 (2^10 - 1)
# so the vEB Tree which could accommodate keys till 1023 should be of size 1024


class Graph:
    def __init__(self, vertices, UNIVERSE_SIZE=1024):
        self.V = vertices  # vertices
        # A vEB Tree (u,v,weight) form where weight is the key and (u,v,weight) is the satellite data,
        # which indicates a weighted edge incident to nodes u and v
        self.edges = VEBTree(2 ** math.ceil(math.log2(UNIVERSE_SIZE)))

    # This function inserts a new edge to the graph
    def insert_edge(self, u, v, w):
        INSERT(self.edges, w, [(u, v, w)])

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
            w = MINIMUM(self.edges)
            u, v, w = GET_SATELLITE(self.edges, w)[-1]  # get last edge with specified key
            DELETE(self.edges, w)  # delete that edge

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

    g = Graph(V, UNIVERSE_SIZE=2 ** math.ceil(math.log2(E)))
    for _ in range(E):
        u, v, w = map(int, input().split())
        g.insert_edge(u, v, w)

    print(g.kruskal())
