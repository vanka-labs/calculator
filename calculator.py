from decimal import *
from math import nan, inf, floor


def check_number(number):
    correct = '1234567890,.- '
    only_one = ',.-'
    dict_corr = {}
    if ' ' in number:
        index = number.index(' ')
    i, minus_count = 0, 0
    for symbol in number:
        if symbol not in correct:
            return False
        elif symbol == ' ':
            if abs(index - i) == 0 or abs(index - i) == 4:
                index = i
            else:
                return False
        elif symbol in only_one:
            if dict_corr.get(symbol) is None:
                dict_corr[symbol] = 1
            else:
                return False
        i += 1
    if dict_corr.get('.') == dict_corr.get(',') and dict_corr.get('.') is not None:
        print(dict_corr)
        return False
    if '-' in number:
        if number[0] != '-':
            return False
        else:
            return True
    else:
        return True


def format_number(number):
    if ',' in number:
        number = number.replace(',', '.')
    if ' ' in number:
        number = number.replace(' ', '')
    return Decimal(number)


def calculate(num1, num2, operation):
    max_value = Decimal('1000000000001')
    error_flag = False
    overflow_flag = False
    if operation == '/':
        if num1 == 0 and num2 == 0:
            error_flag = True
            return Decimal(nan), error_flag, overflow_flag
        elif num2 == 0:
            error_flag = True
            return Decimal(inf), error_flag, overflow_flag
        elif num1 == 0 and num2 == Decimal(inf):
            error_flag = True
            return Decimal(nan), error_flag, overflow_flag
        elif num1 == Decimal(inf) and num2 == Decimal(inf):
            error_flag = True
            return Decimal(nan), error_flag, overflow_flag
        res = num1 / num2
        if abs(res) >= max_value:
            overflow_flag = True
            return res, error_flag, overflow_flag
        else:
            return res, error_flag, overflow_flag
    elif operation == '*':
        if num1 == 0 and num2 == Decimal(inf):
            error_flag = True
            return Decimal(nan), error_flag, overflow_flag
        elif num2 == 0 and num1 == Decimal(inf):
            error_flag = True
            return Decimal(nan), error_flag, overflow_flag
        elif num2 == Decimal(inf) and num1 == Decimal(inf):
            error_flag = True
            return Decimal(nan), error_flag, overflow_flag
        res = num1 * num2
        if abs(res) >= max_value:
            overflow_flag = True
            return res, error_flag, overflow_flag
        else:
            return res, error_flag, overflow_flag
    elif operation == '+':
        res = num1 + num2
        if abs(res) >= max_value:
            overflow_flag = True
            return res, error_flag, overflow_flag
        else:
            return res, error_flag, overflow_flag
    elif operation == '-':
        res = num1 - num2
        if abs(res) >= max_value:
            overflow_flag = True
            return res, error_flag, overflow_flag
        else:
            return res, error_flag, overflow_flag


def set_precision(number, size):
    is_negative = False
    if number < 0:
        is_negative = True
    min_value = '1e-' + str(size)
    min_value = Decimal(min_value)
    if number != Decimal(nan) and number != Decimal(inf):
        float_part = number % 1

        int_part = number - float_part
        int_size = len(str(int_part).split('.')[0])
        if int_part == 0:
            int_size = 0
        getcontext().prec = size
        setcontext(Context(prec=size))
        # float_part = float_part.normalize()
        # float_part = float_part + Decimal('0.0')
        precision = size + int_size
        if is_negative:
            precision -= 1
        getcontext().prec = precision
        if abs(float_part) < min_value and float_part != 0:
            value = '1e-' + str(size)
            value = Decimal.normalize(Decimal(value))
            float_part = Decimal('0')
        if '.0' in str(float_part):
            nulls_count = 0
            fl_part = str(float_part).split('.')[1]
            i = 0
            while fl_part[i] == '0' and i < len(fl_part) - 1:
                nulls_count += 1
                i += 1

            getcontext().prec = size - nulls_count
            float_part = float_part + Decimal('0')
            getcontext().prec = precision
        number = int_part + float_part
        number = number.normalize()
        number = number + Decimal('0')
        getcontext().prec = 28
    return number


def add_spaces(number):
    number = number + Decimal('0.0')
    is_negative = False
    if number < 0:
        is_negative = True
    float_part = number % 1
    int_part = number - float_part
    float_part = str(number).split('.')[1]
    int_part, float_part = str(abs(int_part)), str(float_part)
    int_part = int_part.split('.')[0]
    spaces_num = floor(len(int_part) / 3)
    new_int_part = ''
    rev_int_part = int_part[::-1]
    for i in range(spaces_num):
        new_int_part += rev_int_part[i * 3] + rev_int_part[i * 3 + 1] + rev_int_part[i * 3 + 2] + ' '
    if len(int_part) % 3 != 0:
        add_length = len(int_part) % 3
        if add_length == 1:
            new_int_part += int_part[0]
        else:
            new_int_part += int_part[1] + int_part[0]
    if is_negative:
        new_int_part += '-'
    new_int_part = new_int_part[::-1]

    if float_part != '0' and float_part != '-0':
        new_int_part += '.' + float_part
    return new_int_part
