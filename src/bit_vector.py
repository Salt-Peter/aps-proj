u = 100  # numbers in universe. [0,99] inclusive
arr = [0] * u  # maintain an array of u bits


# arr[i] holds: 1 if element exists in our set else 0
# TC of INSERT, DELETE, MEMBER = O(1) in all case
# TC of MINIMUM, MAXIMUM, SUCCESSOR, PREDECESSOR = O(u) in Worst case
def INSERT(x):
    arr[x] = 1


def DELETE(x):
    arr[x] = 0


def MEMBER(x):
    return arr[x] == 1


def MINIMUM():
    for i in range(u):
        if arr[i]:
            return i


def MAXIMUM():
    for i in reversed(range(u)):
        if arr[i]:
            return i


def SUCCESSOR(x):
    for i in range(x + 1, u):
        if arr[i]:
            return i


def PREDECESSOR(x):
    for i in reversed(range(0, x)):  # runs from x-1 to 0
        if arr[i]:
            return i


if __name__ == "__main__":
    INSERT(95)
    INSERT(2)
    INSERT(50)

    print(MEMBER(4))
    print(MEMBER(2))
    print(SUCCESSOR(50))
    print(PREDECESSOR(50))
    print(SUCCESSOR(95))
