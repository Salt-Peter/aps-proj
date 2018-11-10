from math import sqrt, floor


class ProtovEB:
    def __init__(self, u):
        if u == 2:
            self.u = 2
            self.arr = [0, 0]
        else:  # u > 2
            root_u = floor(sqrt(u))
            self.u = u  # set V.u = u
            self.summary = ProtovEB(root_u)
            self.cluster = [ProtovEB(root_u) for _ in range(root_u)]

    def high(self, x):
        """
        :param x:
        :return: most significant (log(u)/2) bits of x which is basically the cluster id
        eg
        x = 14 = 1110
        u = 16
        logu = 4
        clusterid= MSBits  = 11 = 3
        """
        return floor(x / sqrt(self.u))

    def low(self, x):
        """
        :param x:
        :return: LS logu/2 bits of x which is the x's position within its cluster
        """
        return x % int(sqrt(self.u))

    def index(self, x, y):
        """
        Builds an element number from x and y
        x=index(high(x),low(x))
        :param x:
        :param y:
        :return:
        """
        return x * int(sqrt(self.u)) + y


# T(u) = T(sqrt(u)) + O(1)
# TC = O(loglogu)
def MEMBER(V, x):
    # Base case
    if V.u == 2:
        return V.arr[x]

    # Recursively go down to the correct cluster
    return MEMBER(V.cluster[V.high(x)], V.low(x))


# T(u) = 2T(sqrt(u)) + O(1)
# TC = O(log u)
def MINIMUM(V):
    # Base case
    if V.u == 2:
        if V.arr[0] == 1:
            return 0
        elif V.arr[1] == 1:
            return 1
        else:
            return None

    min_cluster = MINIMUM(V.summary)  # find id of first cluster containing a 1
    if min_cluster is None:
        return None
    else:
        # the minimum element of the set is somewhere in cluster number min_cluster
        offset = MINIMUM(V.cluster[min_cluster])  # find first 1 within the cluster min_cluster
        return V.index(min_cluster, offset)


# T(u) = 2T(sqrt(u)) + O(1)
# => TC = O(log(u)
def INSERT(V, x):
    if V.u == 2:
        V.arr[x] = 1
    else:
        INSERT(V.cluster[V.high(x)], V.low(x))
        INSERT(V.summary, V.high(x))


def SUCCESSOR(V, x):
    if V.u == 2:
        # the only way that x
        # can have a successor within a proto-vEB(2) structure is when x = 0 and arr[1] is 1
        if x == 0 and V.arr[1] == 1:
            return 1
        else:
            return None
    else:
        offset = SUCCESSOR(V.cluster[V.high(x)], V.low(x))
        if offset is not None:
            return V.index(V.high(x), offset)
        else:
            succ_cluster = SUCCESSOR(V.summary, V.high(x))
            if succ_cluster is None:
                return None
            else:
                offset = MINIMUM(V.cluster[succ_cluster])
                return V.index(succ_cluster, offset)


if __name__ == "__main__":
    V = ProtovEB(u=16)
    INSERT(V, 2)
    INSERT(V, 3)
    INSERT(V, 4)
    INSERT(V, 5)
    INSERT(V, 7)
    INSERT(V, 14)
    INSERT(V, 15)

    print(MINIMUM(V))
    print(SUCCESSOR(V, 7))
