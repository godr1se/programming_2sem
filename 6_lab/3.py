from tkinter import *
from tkinter.ttk import Combobox
import os

def clicked():
    choose = combo_ticker.get()
    nameFile = dirs[choose]
    os.startfile('C:/Users/Home/PycharmProjects/1/ИТМО/ПРОГРАММИРОВАНИЕ/2 сем/6 лаба/pdf/' + nameFile)


dir_name = 'pdf'
files = os.listdir(dir_name)
dirs = {}
for file in files:
    dirs[" - ".join(file.split('-')[3:])[:-4]] = file

window = Tk()
window.geometry('200x50')
window.title("выбор")
lbl = Label(window, text="Выберите тикер")
combo_ticker = Combobox(window)
combo_ticker['values'] = list(dirs.keys())
combo_ticker.current(0)
combo_ticker.grid(column=1, row=1)

btn = Button(window, text="Клик!", command=clicked)
btn.grid(column=1, row=3)
window.mainloop()