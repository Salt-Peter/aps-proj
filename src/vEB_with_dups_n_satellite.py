from copy import copy
from math import floor, ceil, log2


class VEBTree:
    def __init__(self, u):
        self.u = u  # eg 8
        self.upper_root = 2 ** ceil(log2(u) / 2)  # eg 4
        self.lower_root = 2 ** floor(log2(u) / 2)  # eg 2
        self.min = None
        self.max = None
        self.min_cnt = 0
        self.max_cnt = 0
        self.min_data = None
        self.max_data = None

        if u == 2:
            pass
        else:
            # unless u equals base size 2,
            # attribute summary points to a veb tree of size upper_root
            # and each cluster in cluster [0 ... upper_root -1 ] points to vEB Trees of size lower_root.
            # eg u = 8, upper_root = 4, lower_root = 2
            # summary point to a veb tree of size 4
            # cluster is an array of size 4
            # each element of cluster points to a veb tree of size 2
            # so cluster points to 4 veb(2) tree
            self.summary = VEBTree(self.upper_root)
            self.cluster = [VEBTree(self.lower_root) for _ in range(self.upper_root)]

    def high(self, x):
        return floor(x / self.lower_root)

    def low(self, x):
        return x % self.lower_root

    def index(self, x, y):
        return x * self.lower_root + y


def MINIMUM(V):
    return V.min


def MAXIMUM(V):
    return V.max


# TC = O(loglogu)
def MEMBER(V, x):
    if x == V.min or x == V.max:  # best case
        return True
    elif V.u == 2:  # base case, no further nested structure
        return False

    # else recursively go down into the vEB structure of smaller size(sqrt(u))
    return MEMBER(V.cluster[V.high(x)], V.low(x))


def SUCCESSOR(V, x):
    # Base case
    if V.u == 2:
        # the only way that x can have a successor
        # within a vEB(2) structure is when x = 0 and arr[1] is 1. (arr[1] is our max field)
        if x == 0 and V.max == 1:
            return 1
        else:
            return None

    elif V.min is not None and x < V.min:
        # if x is strictly less than the minimum element in our set
        # then min would be the successor
        # eg if x=0 and min in our set is 2 then obviously 2 is the successor of 0 (as well as 1)
        return V.min

    else:
        max_low = MAXIMUM(V.cluster[V.high(x)])  # find the maximum element in x's cluster
        if max_low is not None and V.low(x) < max_low:
            # If x's cluster contains some element that is greater than x,
            # then we know that x's successor lies somewhere within x's cluster.
            # max_low is actually the offset (position) of max element within that cluster
            # so we compare max_low with the offset (position) of x in its cluster
            # eg: let x=4(0100), maximum  element in that cluster is 7(0111), so max_low will be 3(11)
            # low(x=4) = 0(00)

            offset = SUCCESSOR(V.cluster[V.high(x)], V.low(x))
            return V.index(V.high(x), offset)
        else:
            succ_cluster = SUCCESSOR(V.summary, V.high(x))
            if succ_cluster is None:
                return None
            else:
                offset = MINIMUM(V.cluster[succ_cluster])
                return V.index(succ_cluster, offset)


def GET_SATELLITE(V, x):
    if x == V.min:
        return V.min_data
    if x == V.max:
        return V.max_data
    if V.u == 2:
        return None

    return GET_SATELLITE(V.cluster[V.high(x)], V.low(x))


def INSERT_EMPTY(V, x, data, n):
    V.min = V.max = x
    V.min_cnt = V.max_cnt = n
    V.min_data = copy(data)
    V.max_data = copy(data)


def INSERT(V, x, data, n=1):
    # V is an empty vEB Tree (Base case)
    if V.min is None:
        INSERT_EMPTY(V, x, data, n)
        return

    if x == V.max:
        V.max_cnt += n
        V.max_data.extend(data)
    if x == V.min:
        V.min_cnt += n
        V.min_data.extend(data)
        return

    if x < V.min:
        x, V.min = V.min, x
        n, V.min_cnt = V.min_cnt, n
        data, V.min_data = copy(V.min_data), copy(data)

    if V.u > 2:
        if MINIMUM(V.cluster[V.high(x)]) is None:
            INSERT(V.summary, V.high(x), copy(data))
            INSERT_EMPTY(V.cluster[V.high(x)], V.low(x), copy(data), n)

        else:
            INSERT(V.cluster[V.high(x)], V.low(x), copy(data), n)

    if x > V.max:
        V.max = x
        V.max_cnt = n
        V.max_data = copy(data)


def DELETE(V, x, n=1):
    # unique key in tree
    if V.min == V.max:
        if V.min is None or V.min_cnt == n:
            V.min = V.max = None
            V.min_data = V.max_data = None
            V.min_cnt = 0
            V.max_cnt = 0
        else:
            # more copies of the element than is to be removed
            V.min_cnt -= n
            V.max_cnt -= n
            del V.min_data[:n]  # pops n elements from front of the list
            del V.max_data[:n]  # pops n elements from front of the list

        return

    if V.u == 2:
        if x == 0:  # element to be removed is the min element
            V.min_cnt -= n
            del V.min_data[:n]

            if V.min_cnt == 0:  # all elements of min key removed
                V.min = 1
                V.min_cnt = V.max_cnt
                V.min_data = V.max_data
        else:
            V.max_cnt -= n
            del V.max_data[:n]

            if V.max_cnt == 0:
                V.max = 0
                V.max_cnt = V.min_cnt
                V.max_data = V.min_data
        return
    next_n = n

    if x == V.min:
        if V.min_cnt > n:
            V.min_cnt -= n
            del V.min_data[:n]
            return

        first_cluster = MINIMUM(V.summary)
        x = V.index(first_cluster,
                    MINIMUM(V.cluster[first_cluster]))
        V.min = x
        V.min_cnt = V.cluster[first_cluster].min_cnt
        V.min_data = V.cluster[first_cluster].min_data

        next_n = V.cluster[first_cluster].min_cnt

    DELETE(V.cluster[V.high(x)], V.low(x), next_n)

    if MINIMUM(V.cluster[V.high(x)]) is None:
        DELETE(V.summary, V.high(x))
        if x == V.max:
            if V.max == V.min:
                V.max_cnt = V.min_cnt
                V.max_data = V.min_data
                return
            V.max_cnt -= n
            del V.max_data[:n]

            if V.max_cnt == 0:
                summary_max = MAXIMUM(V.summary)

                if summary_max is None:
                    V.max = V.min
                    V.max_cnt = V.min_cnt
                    V.max_data = V.min_data
                else:
                    V.max = V.index(summary_max,
                                    MAXIMUM(V.cluster[summary_max]))
                    V.max_cnt = V.cluster[summary_max].max_cnt
                    V.max_data = V.cluster[summary_max].max_data

    elif x == V.max:
        if V.max == V.min:
            V.max_cnt = V.min_cnt
            V.max_data = V.min_data
            return
        V.max_cnt -= n
        del V.max_data[:n]

        if V.max_cnt == 0:
            V.max = V.index(V.high(x),
                            MAXIMUM(V.cluster[V.high(x)]))
            V.max_cnt = V.cluster[V.high(x)].max_cnt
            V.max_data = V.cluster[V.high(x)].max_data


if __name__ == "__main__":
    V = VEBTree(u=16)
    INSERT(V, 2, [(0, 1, 2)])
    INSERT(V, 3, [(2, 1, 3)])
    INSERT(V, 4, [(0, 1, 4)])
    INSERT(V, 4, [(1, 2, 4)])
    INSERT(V, 4, [(1, 3, 4)])

    for i in range(16):
        print(MEMBER(V, i), end=" ")

    print()

    for i in range(16):
        print(SUCCESSOR(V, i), end=' ')

    print()

    print("Object with key =2", GET_SATELLITE(V, 2))
    print("Object with key =3", GET_SATELLITE(V, 3))
    print("Object with key =4", GET_SATELLITE(V, 4))

    DELETE(V, 4)
    print(MAXIMUM(V))
    print("Object with key =4", GET_SATELLITE(V, 4))

    DELETE(V, 4)
    print(MAXIMUM(V))
    print("Object with key =4", GET_SATELLITE(V, 4))

    DELETE(V, 4)
    print(MAXIMUM(V))
    print("Object with key =4", GET_SATELLITE(V, 4))

    DELETE(V, 2)
    print(MINIMUM(V))
