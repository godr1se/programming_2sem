from fpdf import FPDF
from tkinter import *




def simple_table(deg, fi, sec, thi, itog, a_raz, b_raz, c_raz):
    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()
    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    spacing = 1
    column = [["variables", "values"], ['a', str(fi) + a_raz], ['b', str(sec) + b_raz], ['c', str(thi) + c_raz]]
    if deg == 0:
        for row in column:
            for item in row:
                pdf.cell(col_width, row_height * spacing, txt=item, border=1)
            pdf.ln(row_height * spacing)
        pdf.cell(200, 10, txt="result = 0m", ln=1)
        pdf.output("simple_demo.pdf")
    else:
        for row in column:
            for item in row:
                pdf.cell(col_width, row_height * spacing, txt=item, border=1)
            pdf.ln(row_height * spacing)
        pdf.cell(200, 10, txt=("result = " + str(itog) + "m^"+ str(deg)), ln=1)
        pdf.output("simple_demo.pdf")


def clicked():
    deg = 3
    a_raz = ''
    b_raz = ''
    c_raz = ''
    if not txt1.get():
        a = 1
        deg -= 1
    else:
        a = int(txt1.get())
        a_raz = None
        if var1.get() == 1:
            a /= 1000
            a_raz = 'mm'
        if var1.get() == 2:
            a /= 100
            a_raz = 'sm'
        if a_raz != 'mm' and a_raz != 'sm':
            a_raz = 'm'
    if not txt2.get():
        b = 1
        deg -= 1
    else:
        b = int(txt2.get())
        b_raz = None
        if var2.get() == 1:
            b /= 1000
            b_raz = 'mm'
        if var2.get() == 2:
            b /= 100
            b_raz = 'sm'
        if b_raz != 'mm' and b_raz != 'sm':
            b_raz = 'm'
    if not txt3.get():
        c = 1
        deg -= 1
    else:
        c = int(txt3.get())
        c_raz = None
        if var3.get() == 1:
            c /= 1000
            c_raz = 'mm'
        if var3.get() == 2:
            c /= 100
            c_raz = 'sm'
        if c_raz != 'mm' and c_raz != 'sm':
            c_raz = 'm'
    itog = a*b*c
    a = txt1.get()
    b = txt2.get()
    c = txt3.get()
    simple_table(deg, a, b, c, itog, a_raz, b_raz, c_raz)


window = Tk()
window.geometry('250x125')
window.title("расчет")
lbl1 = Label(window, text="a = ", font=("Arial Bold", 15))
lbl1.grid(column=0, row=0)
txt1 = Entry(window,width=10)
txt1.grid(column=1, row=0)
lbl2 = Label(window, text="b = ", font=("Arial Bold", 15))
lbl2.grid(column=0, row=1)
txt2 = Entry(window,width=10)
txt2.grid(column=1, row=1)
lbl3 = Label(window, text="c = ", font=("Arial Bold", 15))
lbl3.grid(column=0, row=2)
txt3 = Entry(window,width=10)
txt3.grid(column=1, row=2)
var1 = IntVar()
var1.set(0)
var2 = IntVar()
var2.set(0)
var3 = IntVar()
var3.set(0)
rad1_1 = Radiobutton(window, text='mm', value=1, variable=var1)
rad1_2 = Radiobutton(window, text='sm', value=2, variable=var1)
rad1_3 = Radiobutton(window, text='m', value=3, variable=var1)
rad1_1.grid(column=3, row=0)
rad1_2.grid(column=4, row=0)
rad1_3.grid(column=5, row=0)
rad2_1 = Radiobutton(window, text='mm', value=1, variable=var2)
rad2_2 = Radiobutton(window, text='sm', value=2, variable=var2)
rad2_3 = Radiobutton(window, text='m', value=3, variable=var2)
rad2_1.grid(column=3, row=1)
rad2_2.grid(column=4, row=1)
rad2_3.grid(column=5, row=1)
rad3_1 = Radiobutton(window, text='mm', value=1, variable=var3)
rad3_2 = Radiobutton(window, text='sm', value=2, variable=var3)
rad3_3 = Radiobutton(window, text='m', value=3, variable=var3)
rad3_1.grid(column=3, row=2)
rad3_2.grid(column=4, row=2)
rad3_3.grid(column=5, row=2)


btn = Button(window, text="Клик!", command=clicked)
btn.grid(column=3, row=3)
window.mainloop()
