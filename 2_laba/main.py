import random
import matplotlib.pyplot as plt
import numpy as np
import matrix


matrix1 = [[2, 3, 5, 5], [4, -3, -1, 1], [2, 5, 1, 3], [0, 7, 2, -2]]
matrix2 = [[-3, -1, 1, 4], [5, 1, 3, 6], [7, 2, 5, -2], [7, 2, -2, -2]]


def first():
    print('own multiply: ', *matrix.multiply_matrix(matrix1, matrix2), sep='\n')
    print('\n')
    print('numpy multiply: ', '\n', *matrix.checking_with_numpy(matrix1, matrix2))
    print('\n')
    print('transpose matrix: ', *matrix.trans(matrix1), sep='\n')
    print('\n')
    print('determinant of matrix: ', matrix.determinant(matrix2))
    print('\n')
    print('numpy det: ', np.linalg.det(matrix2))
    print('\n')
    print('matrix in power 2: ', *matrix.pow_matrix(matrix1), sep='\n')
    print('\n')
    print('numpy pow: ', *np.array(matrix1) @ matrix1, sep='\n')
    print('\n')
    return '---------------------------'


# рандомное заполнение
def rand(length):
    result = []

    for i in range(length):
        result.append([])
        for j in range(length):
            a = random.randint(1, 30)
            result[-1].append(a)

    return result


# рандомное удаление
def rand_delete(array, value):
    delete_x = []
    delete_y = []
    for i in range(10):
        while True:
            x = random.randint(0, len(array) - 1)
            y = random.randint(0, len(array) - 1)
            if array[y][x] != value: break
        delete_x.append(len(array) * y + x)
        delete_y.append(array[y][x])
        array[y][x] = value
    return (delete_x, delete_y)


# восстановление путем линейной аппроксимации
def recovery_points(length):
    result = rand(length)
    transform(result)
    new = []
    delete_x, delete_y = rand_delete(result, None)
    new_x = []
    new_y = []
    print(np.array(result))
    print("\n")
    plt.scatter(delete_x, delete_y, color="red")
    for i in result: new += i
    n = len(new)

    index = 0
    start_index = 0
    finish_index = 0
    while index < n:
        while index < n and new[index] == None:
            finish_index += 1
            index += 1
        if start_index != finish_index:
            recover(new, start_index, finish_index, new_x, new_y)
        index += 1
        finish_index = index
        start_index = index

    plt.scatter(new_x, new_y, color="green", marker="^", s=100)
    print(np.array(new))
    plt.show()


def recover(array, start, finish, x, y):
    k = 0
    b = 0
    if finish == len(array): finish -= 1
    if array[finish] == None:
        k = array[start - 1] - array[start - 2]
        b = array[start - 1] - k * (start - 1)

    elif array[start] == None:
        if start == 0:
            k = array[finish] / finish
            b = array[finish] - k * finish
        else:
            k = (array[start - 1] - array[finish]) / (finish - start)
            b = array[start - 1] - k * (start - 1)

        for i in range(start, finish):
            array[i] = k * i + b
            x.append(i)
            y.append(array[i])

# восстановление путем корреляции
def correlation(array):
    print("MATRIX WITH DELETED VALUES: \n")
    rand_delete(array, 0)
    print(np.array(array))
    print("\n")
    data = []
    while len(array) > 0:
        data.append([array.pop(), []])

    for i in range(len(data)):
        for j in range(len(data)):
            if i != j:
                a = np.array(data[i][0])
                b = np.array(data[j][0])
                if sum(data[j][0]) == 0:
                    data[i][1].append([0, j])
                else:
                    data[i][1].append([np.corrcoef(a, b).min(), j])
        data[i][1].sort()

    while full_recover(data):
        for i in data: recover_correlation(i, data)
    for i in range(len(data)):  data[i] = data[i][0]
    d = np.array(data)
    res = d[::-1]
    print(res)
    return "------------"


def recover_correlation(row, data):
    deleten = []
    for i in range(len(row[0])):
        if row[0][i] == 0:
            deleten.append(i)

    for i in range(len(row[1])):
        for j in range(len(deleten)):
            if deleten[j] == None: continue
            row_index = row[1][i][1]
            element = data[row_index][0][deleten[j]]
            if element != 0:
                row[0][deleten[j]] = data[row[1][i][1]][0][deleten[j]]
                deleten[j] = None


def full_recover(data):
    for row in data:
        if 0 in row[0]: return True
    return False


# трансформация данных
def transform(array):
    x = []
    y = []
    n = len(array)
    for i in range(n * n):
        x.append(i)
    for i in array:
        y += i
    plt.scatter(x, y, s=5)


def third(n):
    numbers = rand(n)
    print("\n")
    mx = 0
    mx2 = 0
    print(np.array(numbers))
    for i in range(len(numbers)):
        for j in range(len(numbers[i])):
            mx += numbers[i][j]/(len(numbers[i]))
            mx2 += numbers[i][j]**2/(len(numbers[i]))
            disp = mx2-mx**2
        print('Table number: ', i, ' Expected value: ', mx, ' Variance: ', disp)
        mx = 0
        mx2 = 0



print(first())
print(correlation(rand(10)))
print(recovery_points(15))
print(third(10))