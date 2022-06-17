
def merge(L, R):
    n = len(L)
    m = len(R)
    i = 0
    j = 0

    sorted = []
    while i < n and j < m:
        if L[i] < R[j]:
            sorted.append(L[i])
            i += 1
        else:
            sorted.append(R[j])
            j += 1
    if i < n:
        sorted.extend(L[i:])
    else:
        sorted.extend(R[j:])

    return sorted


def sort(A):
    n = len(A)
    if n == 1:
        return A

    mid = n//2
    L = sort(A[:mid])
    R = sort(A[mid:])
    return merge(L, R)


if __name__ == '__main__':
    a = []
    for i in range(19):
        if i % 2 == 0:
            a.append(i)
        else:
            a.append(i**2)
    print(a)
    a = sort(a)
    print(a)
