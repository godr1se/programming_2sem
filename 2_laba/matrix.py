import numpy as np
import time

matrix1 = [[2, 3, 0, 5], [4, -3, -1, 1], [2, 5, 1, 3], [2, 7, 2, -2]]
matrix2 = [[-3, -1, 1, 4], [5, 1, 3, 6], [7, 2, -2, -2], [7, 2, -2, -2]]


def checking_with_numpy(a, b) -> np.array:
    """multiplying matrices with numpy"""
    start_time = time.time()
    x = np.array(a) @ b
    end_time = time.time()
    return x, (start_time-end_time)


def multiply_matrix(a, b) -> list:
    """multiply matrices"""
    start_time = time.time()
    m = len(a)  # strings from 1 matrix
    n = len(a[0])  # columns from 1 matrix
    x = len(b)  # strings from 2 matrix
    y = len(b[0])  # columns from 2 matrix

    if n == x:
        # create the list with empty objects in size m*y(m - strings from 1 matrix, y - columns from 2 matrix)
        result = [[None for j in range(y)] for i in range(m)]

        # fill the result with sum of multiplying numbers from 1 matrix with 2 matrix
        for i in range(m):
            for j in range(y):
                result[i][j] = sum(a[i][h] * b[h][j] for h in range(n))

        end_time = time.time()
        return result, (start_time-end_time)

    return ['oops, your data is wrong']


def pow_matrix(a) -> list:
    """matrices ** 2"""
    # start_time = time.time()
    m = len(a)  # strings from 1 matrix
    n = len(a[0])  # columns from 1 matrix

    if m == n:
        # create the list with empty objects in size m*y(m - strings from 1 matrix, y - columns from 2 matrix)
        result = [[None for j in range(n)] for i in range(m)]

        # fill the result with sum of multiplying numbers from 1 matrix with 2 matrix
        for i in range(m):
            for j in range(n):
                result[i][j] = sum(a[i][h] * a[h][j] for h in range(n))

        # end_time = time.time()
        return result

    return ['oops, your data is wrong']

def square_matrix_2(a) -> list:
    """matrices ** 2"""
    # start_time = time.time()
    m = len(a)  # strings from 1 matrix
    n = len(a[0])  # columns from 1 matrix

    if m == n:
        # create the list with empty objects in size m*y(m - strings from 1 matrix, y - columns from 2 matrix)
        result = [[None for j in range(n)] for i in range(m)]

        # fill the result with sum of multiplying numbers from 1 matrix with 2 matrix
        for i in range(m):
            for j in range(n):
                result[i][j] = sum(a[i][h] * a[h][j] for h in range(n))

        # end_time = time.time()
        return result

    return ['oops, your data is wrong']

def trans(a) -> list:
    """Transposing the matrix"""
    m = len(a)  # strings in the matrix
    n = len(a[0])  # columns in the matrix

    # create the list with empty objects in size n*m
    result = [[None for j in range(m)] for i in range(n)]

    # fill the result with numbers from the matrix
    for i in range(m):
        for j in range(n):
            result[i][j] = a[j][i]

    return result


def small_determinant(a) -> int:
    """find a determinant if matrix in size 2*2"""
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def minor(a, x, y) -> list:
    """find a minor of an element"""
    m = len(a)  # strings in the matrix
    n = len(a[0])  # columns in the matrix
    result = []
    # checking if elements are on strings and columns which we are deleting, and if elements are not add them to result
    for i in range(m):
        for j in range(n):
            if j == y or i == x:
                continue
            else:
                result.append(a[i][j])
    result = [[result.pop(0) for j in range(m-1)] for i in range(n-1)]

    return result


def determinant(a) -> int:
    """find a determinant"""
    m = len(a)  # strings in the matrix
    n = len(a[0])  # columns in the matrix
    if m != n:
        return 'your data is wrong'
    else:
        # finding determinant of the minor and than multiply it with an active element
        result = 0
        for i in range(1):
            for j in range(n):
                # if minor is more than 2*2 find this minor with recursion
                x = minor(a, i, j)
                if len(x) > 2:
                    x = determinant(x)
                    # example: a11 * determinant(minor11) * (-1) ** (1+1)
                    result += (a[i][j] * x) * (-1) ** (i + j)
                else:
                    result += (a[i][j] * small_determinant(x)) * (-1) ** (i + j)
        return result