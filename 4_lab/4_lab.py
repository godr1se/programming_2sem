import math
import numpy as np
import random
import yfinance as yf
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import Combobox


def rand_delete(array, count):
    for i in range(count):
        while True:
            x = random.randint(0, len(array) - 1)
            if array[x] != None: break
        array[x] = None
    return array


def approx(arr1):
    result = transform(arr1)
    new = []
    new_x = []
    new_y = []
    print(np.array(result))
    print("\n")
    for i in result:
        new += i
    n = len(new)
    index = 0
    start_index = 0
    finish_index = 0
    while index < n:
        while index < n and new[index] == None:
            finish_index += 1
            index += 1
        if start_index != finish_index:
            recovery(new, start_index, finish_index, new_x, new_y)
        index += 1
        finish_index = index
        start_index = index
    print(np.array(new))


def recovery(array, start, finish, x, y):
    k = 0
    b = 0
    if finish == len(array):
        finish -= 1
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


def transform(array):
    x = []
    y = []
    n = len(array)
    for i in range(n * n):
        x.append(i)
    for i in array:
        y += i


def vinz(array):
    for i in range(len(array)): recover(i, array)
    return array


def corr(array):
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
    return res


def recover_correlation(row, data):
    deleten = []
    for i in range(len(row[0])):
        if row[0][i] == 0:
            deleten.append(i)
    #считывает наны
    for i in range(len(row[1])):
        for j in range(len(deleten)):
            if deleten[j] == None:
                continue
            row_index = row[1][i][1]
            element = data[row_index][0][deleten[j]]
            if element != 0:
                row[0][deleten[j]] = data[row[1][i][1]][0][deleten[j]]
                deleten[j] = None

def full_recover(data):
    for row in data:
        if 0 in row[0]: return True
    return False

def recover(index, array):
    dop_index = 0
    while array[index] == None:
        if index - dop_index > 0 and array[index - dop_index] != None: array[index] = array[index - dop_index]
        if index + dop_index < len(array) and array[index + dop_index] != None:  array[index] = array[index + dop_index]
        dop_index += 1


def smooth(array, k):
    res = []
    for i in range(len(array)):
        res.append(smooth_element(array[:i + 1], k)),

    return res


# сглаживание для 1 элемента
def smooth_element(window, k):
    while math.fabs(window[-1] - (sum(window) / len(window))) / window[-1] > k:
        window.pop(-1)
    return sum(window) / len(window)


# --------------------------------------------------------------------

def smooth_lite(array, k):
    res = []
    a = 1
    for i in range(len(array)):
        if i < k:
            a = k - i
            res.append(smooth_element_lite(array[0:i + a], k))
        else:
            res.append(smooth_element_lite(array[i - k:i + a], k))
    return res


# сглаживание для 1 элемента
def smooth_element_lite(window, k):
    return sum(window) / len(window)


def smoothingChoose(index, plot, k, c):
    if index == 5:
        plot = smooth(plot, k)
    if index == 4:
        plot = smooth_lite(plot, c)
    return plot


ticker_list = ['OGZPY', 'TATN.ME', 'SBER.ME', 'VTBR.ME', 'ALRS.ME', 'AFLT.ME', 'HYDR.ME',
               'MOEX.ME', 'NLMK.ME', 'CHMF.ME', 'DSKY.ME', 'POLY.ME', 'YNDX', 'AFKS.ME',
               'LSRG.ME', 'LSNG.ME', 'LKOH.ME', 'MTSS.ME', 'NVTK.ME', 'PIKK.ME']


def clicked():
    select1 = selected.get()
    select2 = selected2.get()
    select3 = selected3.get()

    array = {}
    plot = []
    ticker = combo_ticker.get()
    start = txt.get()
    end = txt2.get()
    data = yf.download(ticker, start=start, end=end, interval="1d")
    array[ticker] = data['Adj Close']
    for i in range(len(array[ticker])):
        plot.append(array[ticker][i])
    if select1 == 1:
        plot = vinz(rand_delete(plot, 450))
    if select2 == 2:
        plot = approx(rand_delete(plot, 20))
    if select3 == 3:
        plot2_ticker = ticker_list[1]
        if plot2_ticker == ticker:
            plot2_ticker = ticker_list[2]
        plot2 = []
        for i in range(len(array[plot2_ticker])):
            plot2.append(array[plot2_ticker][i])
        plot = corr(rand_delete(plot, 20), plot2)
    k = float(txtK.get())
    c = 5
    sm_plot = smoothingChoose(select2, plot, k, c)
    plt.plot(plot)
    plt.plot(sm_plot)
    plt.show()

w = Tk()
w.title("Kovalsky analysis")
lbl = Label(w, text="Выберите тикер")
lbl.grid(column=1, row=0)
w.geometry('625x250')
btn = Button(w, text="Клик!", command=clicked)
btn.grid(column=1, row=12)

combo_ticker = Combobox(w)
combo_ticker['values'] = tuple(ticker_list)
combo_ticker.current(0)
combo_ticker.grid(column=1, row=1)

selected = IntVar()
selected2 = IntVar()
selected3 = IntVar()

lblRecover = Label(w, text="Выберите метод восстановления")
lblRecover.grid(column=1, row=5)
rad1 = Radiobutton(w, text='Винзорирование', value=1, variable=selected)
rad2 = Radiobutton(w, text='Линейная аппроксимация', value=2, variable=selected)
rad3 = Radiobutton(w, text='Корреляция', value=3, variable=selected)
rad1.grid(column=0, row=6)
rad2.grid(column=1, row=6)
rad3.grid(column=2, row=6)

lblSmooth = Label(w, text="Выберите метод сглаживаиня")
lblSmooth.grid(column=1, row=10)
rad4 = Radiobutton(w, text='Скользящее среднее', value=4, variable=selected2)
rad5 = Radiobutton(w, text='Скользящее среднее с динамическим окном', value=5, variable=selected2)
rad4.grid(column=0, row=11)
rad5.grid(column=2, row=11)

lblDate = Label(w, text="Начальная дата")
lblDate.grid(column=0, row=3)
txt = Entry(w, width=20)
txt.grid(column=0, row=4)

lblDate = Label(w, text="Конечная дата")
lblDate.grid(column=2, row=3)
txt2 = Entry(w, width=20)
txt2.grid(column=2, row=4)

lbltxtK = Label(w, text="Введите K")
lbltxtK.grid(column=1, row=7)
txtK = Entry(w, width=20)
txtK.grid(column=1, row=8)

w.mainloop()
