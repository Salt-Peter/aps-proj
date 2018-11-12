from math import floor, ceil, log2


class VEBTree:
    def __init__(self, u):
        self.u = u  # eg 8
        self.upper_root = 2 ** ceil(log2(u) / 2)  # eg 4
        self.lower_root = 2 ** floor(log2(u) / 2)  # eg 2
        self.min = None
        self.max = None

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


def INSERT_EMPTY(V, x):
    V.min = V.max = x


def INSERT(V, x):
    # V is an empty vEB Tree (Base case)
    if V.min is None:
        INSERT_EMPTY(V, x)
        return

    # else V is non empty
    else:
        if x < V.min:
            # If x < min, then x needs to become the new min.
            # But we don't want to lose the original min.
            # So we need to insert it into one of V's clusters.

            # exchange x and V.min
            x, V.min = V.min, x
            # now insert the original min (now x) into one of the V's clusters

        if V.u > 2:
            # Non base case

            # check whether the cluster that x will go into is currently empty
            # checking MINIMUM or MAXIMUM is sufficient to check for empty cluster
            if MINIMUM(V.cluster[V.high(x)]) is None:
                # insert x's cluster number into summary
                INSERT(V.summary, V.high(x))
                # insert x into the empty cluster
                INSERT_EMPTY(V.cluster[V.high(x)], V.low(x))

            else:
                # x's cluster is not empty
                # so we do not need to update the summary, since x's cluster number is already a member of the summary.

                # insert x into its cluster
                INSERT(V.cluster[V.high(x)], V.low(x))

        # update max
        if x > V.max:
            V.max = x


# assumes that x is currently an element in the set
# represented by the vEB tree V.
# this means if the tree contains only one key
# then no matter what value of x you pass to delete,
# the existing tree element will be deleted
def DELETE(V, x):
    # exactly one element in the tree
    if V.min == V.max:
        V.min = V.max = None

    # Base case: set min and max to the one remaining element.
    elif V.u == 2:
        # if exactly 2 elements exist
        if x == 0:  # and the key to be deleted is 0
            # then set min and max to key 1
            V.max = V.min = 1
        else:  # else key to be deleted is 1
            # so set min and max to key 0
            V.max = V.min = 0

    else:
        # we will have to delete an element from a cluster

        if x == V.min:  # we need to delete the min element
            # but before that we need to find the new min which is some other element within one of V's clusters

            # first_cluster = the cluster id that contains the lowest element other than min
            first_cluster = MINIMUM(V.summary)  # cluster id of cluster containing new min

            # x = lowest element in the found cluster
            x = V.index(first_cluster, MINIMUM(V.cluster[first_cluster]))

            # x becomes new min
            V.min = x

            # now x will be deleted from its cluster

        # Now we need to delete element x from its cluster,
        # whether x was the value originally passed to DELETE()
        # or x is the element becoming the new minimum.
        DELETE(V.cluster[V.high(x)], V.low(x))  # delete x from its cluster

        # That cluster might now become empty
        if MINIMUM(V.cluster[V.high(x)]) is None:
            # if it does, then we need to remove x's cluster number from the summary,
            DELETE(V.summary, V.high(x))

            # After updating the summary, we might need to update max if x is max
            if x == V.max:  # check whether we are deleting max element of V

                # summary_max = the number of the highest numbered nonempty cluster.
                # This works bcoz we have already recursively called DELETE on V.summary
                # and so V.summary.max has already been updated.
                summary_max = MAXIMUM(V.summary)

                if summary_max is None:
                    # If all of V's clusters are empty, then the only remaining element in V is min
                    V.max = V.min  # update max accordingly

                else:
                    # else set max to the maximum element in the highest numbered cluster
                    V.max = V.index(summary_max, MAXIMUM(V.cluster[summary_max]))

        # else if the cluster did not become empty (there is at least one element in x's cluster even after deleting x.)
        # then although we do not have to update the summary in this case, we might have to update max.
        elif x == V.max:  # if max element was deleted, update max
            V.max = V.index(V.high(x), MAXIMUM(V.cluster[V.high(x)]))


if __name__ == "__main__":
    V = VEBTree(u=16)
    INSERT(V, 2)
    INSERT(V, 3)
    INSERT(V, 4)
    INSERT(V, 5)
    INSERT(V, 7)
    INSERT(V, 14)
    INSERT(V, 15)

    for i in range(16):
        print(MEMBER(V, i), end=" ")

    print()

    for i in range(16):
        print(SUCCESSOR(V, i), end=' ')

    print()

    DELETE(V, 15)
    DELETE(V, 14)
    print(MAXIMUM(V))
    DELETE(V, 2)
    print(MINIMUM(V))
