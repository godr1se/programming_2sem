import yfinance as yf
import matplotlib.pyplot as plt

def delete_nans(array):  # Удаляем nan в листах
    fixed_array = []
    for i in range(len(array)):
        if array[i] > 0:
            fixed_array.append(array[i])
    return fixed_array

def digit_check(string):  # Проверка на число
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False

def correlation(only_first, only_second):
    all_kor = []
    sredn_znach1, sredn_znach2 = sum(only_first) / len(only_first), sum(only_second) / len(only_second)
    mat_ozhid1, mat_ozhid2 = 0, 0
    for g in range(len(only_first)):
        mat_ozhid1 += (float(only_first[g]) - sredn_znach1) ** 2
        mat_ozhid2 += (float(only_second[g]) - sredn_znach2) ** 2
    srednee_kvad_otkl1 = (mat_ozhid1 / (len(only_first))) ** (1 / 2)
    srednee_kvad_otkl2 = (mat_ozhid2 / (len(only_second))) ** (1 / 2)
    umnozh = 0
    for l in range(len(only_first)):
        umnozh += (float(only_first[l]) * float(only_second[l]))
    kor = ((umnozh / len(only_first)) - (sredn_znach1 * sredn_znach2)) / (
            srednee_kvad_otkl1 * srednee_kvad_otkl2)
    all_kor.append([kor])
    all_kor = sorted(all_kor)
    return all_kor[0][0]

ticker_list = ['OGZPY', 'TATN.ME', 'SBER.ME', 'VTBR.ME', 'ALRS.ME', 'AFLT.ME', 'HYDR.ME',
               'MOEX.ME', 'NLMK.ME', 'CHMF.ME', 'DSKY.ME', 'POLY.ME', 'YNDX', 'AFKS.ME',
               'LSRG.ME', 'LSNG.ME', 'LKOH.ME', 'MTSS.ME', 'NVTK.ME', 'PIKK.ME']
st = 120
array = {}
volume = {}

anatoliy_start = 10000000
anatoliy = {}
anatoliy_history = []

boris_start = 10000000
boris = {}
boris_history = []

evgeniy_start = 10000000
evgeniy = {}
evgeniy_history = []

for ticker in ticker_list:
    anatoliy[ticker] = 0
    boris[ticker] = 0
    evgeniy[ticker] = 0
    data = yf.download(ticker, start="2017-01-01", end="2019-12-31", interval="1d")
    volume[ticker] = data['Adj Close']
    array[ticker] = data['Adj Close']
    array[ticker] = delete_nans(array[ticker])
    print(ticker)


for month in range(6):  # Для всех лет
    results1 = {}
    results0 = {}
    start = st * month
    end = start + 120

    for ticker in ticker_list:
        anatoliy_start += anatoliy[ticker] * array[ticker][end]
        anatoliy[ticker] = 0
        boris_start += boris[ticker] * array[ticker][end]
        boris[ticker] = 0
        evgeniy_start += evgeniy[ticker] * array[ticker][end]
        evgeniy[ticker] = 0
    evgeniy_history.append(evgeniy_start)

    for i in range(0, len(ticker_list) - 1):  # Берем первый элемент списка тикеров
        temp_arr1 = []
        for h in range(start, end):
            temp_arr1.append(array[ticker_list[i]][h])
        for j in range(i + 1, len(ticker_list)):  # Находим корр первого с каждым следующим
            temp_arr2 = []
            for h in range(start, end):
                temp_arr2.append(array[ticker_list[j]][h])
            r = correlation(temp_arr1, temp_arr2)
            results1[r] = (ticker_list[i], ticker_list[j])
            results0[abs(r)] = (ticker_list[i], ticker_list[j])

    # Сортировка r
    sorted_results1 = list(results1)
    sorted_results1 = sorted(sorted_results1)
    sorted_results1.reverse()
    sorted_results0 = list(results0)
    sorted_results0 = sorted(sorted_results0)
    anatoliy_history.append(anatoliy_start)
    boris_history.append(boris_start)

    # Этап вложения
    for i in range(3):
        anatoliy[results0[sorted_results0[i]][0]] += (anatoliy_start / 6) / array[results0[sorted_results0[i]][0]][end]
        anatoliy[results0[sorted_results0[i]][1]] += (anatoliy_start / 6) / array[results0[sorted_results0[i]][1]][end]
        boris[results1[sorted_results1[i]][0]] += (boris_start / 6) / array[results1[sorted_results1[i]][0]][end]
        boris[results1[sorted_results1[i]][1]] += (boris_start / 6) / array[results1[sorted_results1[i]][1]][end]
    anatoliy_start = 0
    boris_start = 0

    total_value_sum = 0
    for ticker in ticker_list:
        total_value_sum += volume[ticker][end]
    for ticker in ticker_list:
        evgeniy[ticker] = (evgeniy_start * (volume[ticker][end] / total_value_sum)) / volume[ticker][end]
    evgeniy_start = 0

# Убираем оставшиеся акции
for ticker in ticker_list:
    anatoliy_start += anatoliy[ticker] * array[ticker][-1]
    anatoliy[ticker] = 0
    boris_start += boris[ticker] * array[ticker][-1]
    boris[ticker] = 0
    evgeniy_start += evgeniy[ticker] * volume[ticker][-1]
    evgeniy[ticker] = 0

print('Anatoliy: ' + str(anatoliy_start) + '\n' + 'Boris: ' + str(boris_start) +'\n' +\
      'Evgeniy: ' + str(evgeniy_start))
fig, ax = plt.subplots()
ax.plot(anatoliy_history)
ax.plot(boris_history)
ax.plot(evgeniy_history)
plt.xlabel("Период")
plt.ylabel("Баланс")
plt.show()