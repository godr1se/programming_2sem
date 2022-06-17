import gspread
from statsmodels.tsa.ar_model import AutoReg, ar_select_order


sa = gspread.service_account(filename="table-342917-3813bccd4ed6.json")
sh = sa.open('table')
wks = sh.worksheet('Лист2')


data_ex = wks.col_values(2)
data_ex = data_ex[1:]
data =[]
next_month = wks.acell('D2').value
mnth = float(next_month)
for i in range(len(data_ex)):
    data.append(float(data_ex[i]))


mod = ar_select_order(data, maxlag=3, old_names=False)
model = AutoReg(data, lags=mod.ar_lags, old_names=False).fit()
pred = model.predict(start=len(data), end=len(data)+2)

print('next month rate:', next_month)
print('prediction:', pred[0])
if mnth > pred[0]:
    print("Курс завышен на ", mnth-pred[0])
elif mnth == pred[0]:
    print("Курс в норме")
else:
    print("Курс занижен на ", pred[0]-mnth)