import math
import numpy as np
import pandas as pd
import matrix
import matplotlib.pyplot  as plt

def calculate_funcs_values(start, end, step):
    first_func_values = []
    second_func_values = []
    third_func_values = []
    while start < end:
        radian_value = (start*np.pi)/180
        first_func = np.sin(radian_value) + 0.1*np.sin(radian_value**5)
        second_func = np.cos(radian_value**2) - 0.1*np.sin(radian_value**3) / np.cos(radian_value**3)
        third_func = 0.5*start + start**5 - start**3

        first_func_values.append(first_func)
        second_func_values.append(second_func)
        third_func_values.append(third_func)
        start += step
    return first_func_values, second_func_values, third_func_values


def dynamic_smoothing(arr, k):
    result = []
    for i in range(len(arr)):
        if i == 0:
            result.append(arr[i])
        else:
            win = arr[:i + 1]
            while math.fabs((arr[i] - (sum(win) / len(win))) / arr[i]) > k:
                if len(win) > 1:
                    win.pop(0)
                else:
                    break
            result.append(sum(win) / len(win))
    return result


def mnk(x, y):
    sum_x = 0
    sum_sq_x = 0
    sum_y = 0
    sum_x_y = 0

    for i in range(0, len(x) - 1):
        sum_x += x[i]
        sum_sq_x += x[i] ** 2
        sum_y += y[i]
        sum_x_y += y[i] * x[i]
    default_matrix = matrix.build_matrix(2, 2, [sum_sq_x, sum_x, sum_x, len(x)])
    a_matrix = matrix.build_matrix(2, 2, [sum_x_y, sum_x, sum_y, len(x)])
    b_matrix = matrix.build_matrix(2, 2, [sum_sq_x, sum_x_y, sum_x, sum_y])
    default_det = matrix.determinant(default_matrix)
    a_det = matrix.determinant(a_matrix)
    b_det = matrix.determinant(b_matrix)
    a = a_det / default_det
    b = b_det / default_det
    print("y = ", a, "*x + ", b)
    return "\n"


def prediction(arr1, arr2, step):
    first_approx = (arr1[-1] + arr1[-2]) / 2
    second_approx = (arr2[-1] + arr2[-2]) / 2
    first_next_value = first_approx
    second_next_value = second_approx
    return first_next_value, second_next_value


start = int(input())
end = int(input())
step = int(input())

first, second, third = calculate_funcs_values(start, end, step)
first_smoothed, second_smoothed, third_smoothed = dynamic_smoothing(first, 0.5), dynamic_smoothing(second, 0.5), dynamic_smoothing(third, 0.5)
data = pd.DataFrame([first])
data.to_excel("data.xlsx")

amount_of_steps = (end - start)/step
steps = []
for i in range(int(amount_of_steps)):
    steps.append(i)


print(mnk(first_smoothed, steps))
print(mnk(second_smoothed, steps))
print(mnk(third_smoothed, steps))
first_func_predict, first_func_smoothed_predict = prediction(first, first_smoothed, step)
second_func_predict, second_func_smoothed_predict = prediction(second, second_smoothed, step)
third_func_predict, third_func_smoothed_predict = prediction(third, third_smoothed, step)

data = pd.DataFrame([first])
data.to_excel("data.xlsx")

print("Значения 1-ой функции:", *first, "\n", "Сглаженные значения 1-ой функции:", *first_smoothed, "\n", \
      "Прогнозируемое значение 1-ой функции:", first_func_predict, "\n", \
      "Прогнозируемое значение сглаженного 1-ой функции:", first_func_smoothed_predict, "\n")

print("Значения 2-ой функции:", *second, "\n", "Сглаженные значения 2-ой функции:", *second_smoothed, "\n", \
      "Прогнозируемое значение 2-ой функции:", second_func_predict, "\n", \
      "Прогнозируемое значение сглаженного 2-ой функции:", second_func_smoothed_predict, "\n")

print("Значения 3-ей функции:", *third, "\n", "Сглаженные значения 3-ей функции:", *third_smoothed, "\n", \
      "Прогнозируемое значение 3-ей функции:", third_func_predict, "\n",\
      "Прогнозируемое значение сглаженного 3-ей функции:", third_func_smoothed_predict)

x = np.array(first)
default1 = np.array(first)
smoothed1 = np.array(first_smoothed)
fig1, ax_1 = plt.subplots()
ax1 = ax_1.twinx()
ax_1.plot(x, default1, color="r")
ax1.plot(x, smoothed1, color="b")

y = np.array(second)
default2 = np.array(second)
smoothed2 = np.array(second_smoothed)
fig2, ax_2 = plt.subplots()
ax2 = ax_2.twinx()
ax2.plot(y, default2, color="g")
ax_2.plot(y, smoothed2, color="b")

z = np.array(third)
default3 = np.array(third)
smoothed3 = np.array(third_smoothed)
fig3, ax_3 = plt.subplots()
ax3 = ax_3.twinx()
ax3.plot(z, default3, color="y")
ax_3.plot(z, smoothed3, color="b")
plt.show()