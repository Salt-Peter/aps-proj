class Graph:

    def __init__(self, vertices):
        self.V = vertices  # vertices
        # List to store graph in the [u,v,w] form ,
        # which indicates a weighted edge incident to nodes u and v
        self.graph = []

    # This function inserts a new edge to the graph
    def insert_edge(self, u, v, w):
        self.graph.append([u, v, w])

        # Initialises each node with rank 0 and sets each node's parent as itself

    def make_set(self, parent, rank):
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

            # Find_set implementation using Path compression heuristic

    def find(self, parent, i):
        if parent[i] == i:
            return i
            # return self.find(parent, parent[i])
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
            print(i, parent[i], ",", end=" ")
        print()

    def kruskal(self):

        spanning_tree = []  # This will store the Spanning Tree

        # Sort the edges
        self.graph = sorted(self.graph, key=lambda item: item[2])

        parent = []
        rank = []
        g.make_set(parent, rank)
        index = 0
        mst_index = 0
        # We pick the V-1 edges from the sorted edges in graph
        while mst_index < self.V - 1:

            # Get the smallest edge from the graph
            u, v, w = self.graph[index]
            index = index + 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            g.print_parent(parent)

            # check if cycle will be formed by adding this node
            if x != y:
                mst_index = mst_index + 1
                spanning_tree.append([u, v, w])
                self.union(parent, rank, x, y)

                # Print the Minimum cost spanning tree
        print("The minimum spanning tree is as follows")
        for u, v, weight in spanning_tree:
            print("%d -- %d == %d" % (u, v, weight))

        g.print_parent(parent)


# Sample test cases
# g = graph(6) 
# g.Insert_edge(0, 1, 1) 
# g.Insert_edge(0, 2, 2)
# g.Insert_edge(0, 3, 1) 
# g.Insert_edge(1, 3, 1)
# g.Insert_edge(1, 2, 2) 
# g.Insert_edge(1, 4, 4) 
# g.Insert_edge(1, 5, 5)
# g.Insert_edge(2, 4, 4)
# g.Insert_edge(4, 5, 4) 

g = Graph(4)
g.insert_edge(0, 1, 1)
g.insert_edge(0, 2, 1)
g.insert_edge(1, 2, 1)
g.insert_edge(0, 3, 2)
g.insert_edge(3, 1, 2)

g.kruskal()
