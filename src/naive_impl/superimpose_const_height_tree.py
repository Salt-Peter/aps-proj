# TODO: implement MEMBER, MAXIMUM, PREDECESSOR
from math import sqrt, floor

u = 16
CLUSTER_SIZE = int(sqrt(u))

arr = [0] * u
summary = [0] * floor(CLUSTER_SIZE)


# TC of INSERT, MEMBER = O(1) in all case
# TC of DELETE, MINIMUM, MAXIMUM, SUCCESSOR, PREDECESSOR = O(sqrt(u)) in Worst case

def cluster_id(x):
    return floor(x / CLUSTER_SIZE)


def cluster_start(id):
    return id * CLUSTER_SIZE


def cluster_end(id):
    return (id + 1) * CLUSTER_SIZE - 1


# TC = O(1)
def INSERT(x):
    arr[x] = 1
    summary[cluster_id(x)] = 1


# TC = sqrt(u) + sqrt(u) = O(sqrt(u))
def MINIMUM():
    for i, x in enumerate(summary):
        # find first set bit in summary array
        # i.e, find the first cluster which contains a one
        if x:
            # linear search in that cluster now
            # ith cluster points to element from arr[i sqrt(u) ... (i+1)sqrt(u) - 1 ]
            for index, element in enumerate(arr[i * CLUSTER_SIZE: (i + 1) * CLUSTER_SIZE]):
                if element:
                    return index


# TC = 3 * sqrt(u)
def SUCCESSOR(x):
    # first search to the right within this cluster
    # if we find a 1 then return it
    for i in range(x + 1, (cluster_id(x) + 1) * CLUSTER_SIZE):  # eg x=5 i=[5...8) 8 is non inclusive
        if arr[i]:
            return i

    # else search the summary array starting after this cluster id
    for i in range(cluster_id(x) + 1, CLUSTER_SIZE):
        # The first position that holds a one gives the index of a cluster
        if summary[i]:
            # search in that cluster
            for j in range(cluster_start(i), cluster_end(i) + 1):
                if arr[j]:
                    return j


# TC = O(sqrt(u))
def DELETE(x):
    arr[x] = 0  # delete element
    summary_bit = 0
    id = cluster_id(x)

    for i in arr[cluster_start(id): cluster_end(id) + 1]:  # +1 since range end is non inclusive
        # check whether any element in that cluster is 1
        summary_bit |= i

    summary[id] = summary_bit  # update summary bit


if __name__ == "__main__":
    INSERT(2)
    INSERT(3)
    INSERT(4)
    INSERT(5)
    INSERT(7)
    INSERT(14)
    INSERT(15)
    print(MINIMUM())

    print(SUCCESSOR(7))

    DELETE(14)
    print(SUCCESSOR(7))

    DELETE(15)
    print(SUCCESSOR(7))
