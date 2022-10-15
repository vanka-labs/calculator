from decimal import *
from functools import partial
from math import trunc
from tkinter import Tk, Entry, Button, Label, messagebox
from tkinter.ttk import Combobox

from calculator import check_number, format_number, calculate, set_precision, add_spaces


def enter(o1, o2, o3, n1, n2, n3, n4, window):
    operation1 = o1.get()
    operation2 = o2.get()
    operation3 = o3.get()
    num1 = n1.get()
    num2 = n2.get()
    num3 = n3.get()
    num4 = n4.get()
    error_flag, error_flags = False, []
    overflow_flag, overflow_flags = False, []
    if check_number(num1) and check_number(num2) and check_number(num3) and check_number(num4):
        num1 = format_number(num1)
        num2 = format_number(num2)
        num3 = format_number(num3)
        num4 = format_number(num4)
        res, error_flag, overflow_flag = calculate(num2, num3, operation2)
        res = set_precision(res, 10)
        error_flags.append(error_flag)
        if operation3 != '*' and operation3 != '/':
            res, error_flag, overflow_flag = calculate(num1, res, operation1)
            res = set_precision(res, 10)
            error_flags.append(error_flag)
            overflow_flags.append(overflow_flag)
            res, error_flag, overflow_flag = calculate(res, num4, operation3)
            res = set_precision(res, 10)
            error_flags.append(error_flag)
            overflow_flags.append(overflow_flag)
        elif (operation1 == '*' or operation1 == '/') and (operation3 == '*' or operation3 == '/'):
            res, error_flag, overflow_flag = calculate(num1, res, operation1)
            res = set_precision(res, 10)
            error_flags.append(error_flag)
            overflow_flags.append(overflow_flag)
            res, error_flag, overflow_flag = calculate(res, num4, operation3)
            res = set_precision(res, 10)
            error_flags.append(error_flag)
            overflow_flags.append(overflow_flag)
        else:
            res, error_flag, overflow_flag = calculate(res, num4, operation3)
            res = set_precision(res, 10)
            error_flags.append(error_flag)
            overflow_flags.append(overflow_flag)
            res, error_flag, overflow_flag = calculate(num1, res, operation1)
            res = set_precision(res, 10)
            error_flags.append(error_flag)
            overflow_flags.append(overflow_flag)
        if True in error_flags:
            error_flag = True
            messagebox.showerror("Ошибка", "Попробуйте еще раз")
        elif True in overflow_flags:
            overflow_flag = True
            messagebox.showerror("Ошибка", "Выход за диапaзон")
        if not error_flag and not overflow_flag:
            res = set_precision(res, 6)
            n = res
            if abs(res) >= 1000:
                res = add_spaces(res)
            result = Label(window, text=res, width=30, anchor="w")
            result.grid(column=100, row=0)
            round_type = Label(window, text="Выбор вида округления", width=20)
            round_type.grid(column=0, row=10)
            round_type1 = Button(window, text="математическое", command=partial(round1, n, window), width=15)
            round_type1.update()
            round_type1.grid(column=0, row=20)
            round_type2 = Button(window, text="бухгалтерское", command=partial(round2, n, window), width=15)
            round_type2.grid(column=0, row=30)
            round_type3 = Button(window, text="усечение", command=partial(round3, n, window), width=15)
            round_type3.grid(column=0, row=40)
    else:
        messagebox.showerror("Ошибка", "Попробуйте еще раз")
    print(num1, operation1, num2, operation2, num3, operation3, num4)


def round1(n, window):
    round_res = Label(window, text="Результат округления:", width=20)
    round_res.grid(column=50, row=20)
    n = n.quantize(Decimal('1.'), ROUND_HALF_UP)
    if abs(n) >= 1000:
        n = add_spaces(n)
    else:
        n = str(n)
    if n == '-0':
        n = '0'
    result = Label(window, text=n, width=20)
    result.grid(column=50, row=30)


def round2(n, window):
    round_res = Label(window, text="Результат округления:", width=20)
    round_res.grid(column=50, row=20)
    n = round(n)
    if abs(n) >= 1000:
        n = add_spaces(n)
    else:
        n = str(n)
    result = Label(window, text=n, width=20)
    result.grid(column=50, row=30)


def round3(n, window):
    round_res = Label(window, text="Результат округления:", width=20)
    round_res.grid(column=50, row=20)
    n = trunc(n)
    if abs(n) >= 1000:
        n = add_spaces(n)
    else:
        n = str(n)
    result = Label(window, text=n, width=20)
    result.grid(column=50, row=30)


def GUI():
    window = Tk()
    window.title('Калькулятор')
    window.geometry('1200x200')
    txt1 = Entry(window, width=35)
    txt1.insert(0, '0')
    txt1.grid(column=0, row=0)
    combo1, combo2, combo3 = Combobox(window, width=1), Combobox(window, width=1), Combobox(window, width=1)
    combo1['values'] = ('+', '-', '/', '*')
    combo2['values'] = ('+', '-', '/', '*')
    combo3['values'] = ('+', '-', '/', '*')
    combo1.grid(column=10, row=0)
    combo1.set('+')
    lbl1 = Label(window, text="(")
    lbl1.grid(column=20, row=0)
    txt2 = Entry(window, width=35)
    txt2.grid(column=30, row=0)
    txt2.insert(0, '0')
    combo2.grid(column=40, row=0)
    combo2.set('+')
    txt3 = Entry(window, width=35)
    txt3.grid(column=50, row=0)
    txt3.insert(0, '0')
    lbl2 = Label(window, text=")")
    lbl2.grid(column=60, row=0)
    combo3.grid(column=70, row=0)
    combo3.set('+')
    txt4 = Entry(window, width=35)
    txt4.grid(column=80, row=0)
    txt4.insert(0, '0')

    btn = Button(window, text="=",
                 command=partial(enter, combo1, combo2, combo3, txt1, txt2, txt3,
                                 txt4, window), width=1)
    btn.grid(column=90, row=0)
    name = Label(window, text="Ковалёв Иван Романович, 4 к. 4 гр., 2022", width=31)
    name.grid(column=0, row=50)
    window.mainloop()


GUI()
