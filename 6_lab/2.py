import gspread
from tkinter import *
from datetime import datetime
from fpdf import FPDF


def table(m, v, e, filename):
    sa = gspread.service_account(filename="table-342917-3813bccd4ed6.json")
    sh = sa.open("table")
    wks = sh.worksheet("Лист1")
    wks.update('A1', filename)
    wks.update('B1', datetime.today().strftime('%Y-%m-%d'))
    wks.update('B2', '')
    wks.update('B3', e)
    wks.update('B4', m)
    wks.update('B5', v)
    create_pdf(wks.get_all_values(), datetime.today().strftime('%Y-%m-%d') + '-' + filename)


def create_pdf(text, filename):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=14)
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.add_page()
    for line in text:
        pdf.cell(0, 15,  '  '.join(line), ln=1)
    pdf.output('pdf/' + filename + '.pdf', 'F')


def clicked():
    filename = txt1.get()
    m = txt2.get()
    v = txt3.get()
    e = (int(m)*int(v)**2)/2
    return table(m, v, e, filename)

window = Tk()
window.geometry('250x125')
window.title("расчет")
lbl1 = Label(window, text="filename", font=("Arial Bold", 15))
lbl1.grid(column=0, row=0)
txt1 = Entry(window,width=10)
txt1.grid(column=1, row=0)
lbl2_1 = Label(window, text="m = ", font=("Arial Bold", 15))
lbl2_1.grid(column=0, row=1)
txt2 = Entry(window,width=10)
txt2.grid(column=1, row=1)
lbl2_2 = Label(window, text="кг", font=("Arial Bold", 15))
lbl2_2.grid(column=3, row=1)
lbl3_1 = Label(window, text="V = ", font=("Arial Bold", 15))
lbl3_1.grid(column=0, row=2)
txt3 = Entry(window,width=10)
txt3.grid(column=1, row=2)
lbl3_2 = Label(window, text="м/с", font=("Arial Bold", 15))
lbl3_2.grid(column=3, row=2)

btn = Button(window, text="Клик!", command=clicked)
btn.grid(column=1, row=3)
window.mainloop()