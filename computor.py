#! /usr/bin/env python

import re
import sys

"""
Знак (может быть, а может не быть)
((?P<sign>\+|-) )?

(
Число * X в степени или без степени
((?P<var>\d+(\.\d+)?) \* (X|x)(\^(?P<degree>\d+)?)?)
|
Без числа Х в степени или без
((X|x)(\^(?P<degree2>\d+)?)?)
|
Просто число
(?P<var2>\d+(\.\d+)?)
)
"""
side_pattern = '([\+\-] )?\d+(\.\d+)? \* (x|X)\^\d+( [\+-] \d+(\.\d+)? \* (x|X)\^\d+)*'
# side_pattern = '([\+|-] )?' \
#                '(' \
#                '((\d+(\.\d+)?) \* (X|x)(\^(\d+)?)?)' \
#                '|' \
#                '([X|x](\^\d+?)?)' \
#                '|' \
#                '(\d+(\.\d+)?)' \
#                ')'
expr_pattern = '^{0} = {0}$'.format(side_pattern)
elem_pattern = '((?P<sign>\+|-) )?(?P<var>\d+(\.\d+)?) \* (X|x)\^(?P<degree>\d+)'


# elem_pattern = '((?P<sign>\+|-) )?' \
#                '(' \
#                '((?P<var>\d+(\.\d+)?) \* (X|x)(\^(?P<degree>\d+)?)?)' \
#                '|' \
#                '((X|x)(\^(?P<degree2>\d+)?)?)' \
#                '|' \
#                '(?P<var2>\d+(\.\d+)?)' \
#                ')'


def abs(x):
    return x if x >= 0 else -x


def sign(x):
    return '-' if x < 0 else '+'


def sqrt(n):
    sign = 0
    if n < 0:
        sign = -1
        n = -n
    val = n
    while True:
        last = val
        val = (val + n / val) / 2
        # 1 ^ -9 == 0.000000001
        if abs(val - last) < 1e-9:
            break
    if sign < 0:
        return complex(0, val)
    return val


def get_elements(expression, sign=1):
    elements = list()
    for item in re.finditer(elem_pattern, expression):
        element = item.groupdict()
        if element['sign'] == '-':
            element['var'] = -float(element['var']) * sign
        else:
            element['var'] = float(element['var']) * sign
        element['degree'] = int(element['degree'])
        del element['sign']
        elements.append(element)
    return elements


def get_params(expr):
    sides = expr.split('=')
    left_side_elems = get_elements(sides[0].strip())
    right_side_elems = get_elements(sides[1].strip(), sign=-1)
    all_elems = left_side_elems + right_side_elems

    # sum all elements with similar degrees
    params = dict()
    for elem in all_elems:
        params[elem['degree']] = params.get(elem['degree'], 0) + elem['var']
    return params


def get_polynomial_degree(params):
    params = [x for x in params.keys() if params[x] != 0]
    return max(params)


def get_reduced_form(params):
    reduced_form = str()
    # при выводе параметры сортируются в порядке возростания
    for k in sorted(params.keys()):
        if params[k] != 0:
            # если параметр 1 то его можно не писать
            if abs(params[k]) == 1:
                # если степень 1 выводим Х
                if k == 1:
                    reduced_form += '{} X '.format(sign(params[k]))
                # если степень 0 то выводим 1
                elif k == 0:
                    reduced_form += '{} 1 '.format(sign(params[k]))
                else:
                    reduced_form += '{} X^{} '.format(sign(params[k]), k)
            else:
                # если степень 1 выводим Х
                if k == 1:
                    reduced_form += '{} {} * X '.format(sign(params[k]), abs(params[k]))
                # если степень 0 выводим само число
                elif k == 0:
                    reduced_form += '{} {} '.format(sign(params[k]), abs(params[k]))
                else:
                    reduced_form += '{} {} * X^{} '.format(sign(params[k]), abs(params[k]), k)

    if not reduced_form:
        reduced_form = '0'
    # убирает '+ ' вначале
    reduced_form = reduced_form.lstrip('+ ')
    # убирает .0
    reduced_form = reduced_form.replace('.0 ', ' ')
    return reduced_form + '= 0'


def solve(a, b=0, c=0):
    # print('a={} b={} c={}'.format(a, b, c))
    if a != 0:
        d = b * b - 4 * a * c
        # print('d = {}'.format(d))
        if d < 0:
            x = (-b + sqrt(d)) / (2 * a)
            return {'message': 'Square equation, discriminant less than zero, complex solution',
                    'x': ['{0.real:.2f} + {0.imag:.2f}i'.format(x),
                          '{0.real:.2f} - {0.imag:.2f}i'.format(x)]
                    }
        if d == 0:
            return {'message': 'Square equation, one solution', 'x': [-b / (2 * a)]}

        return {'message': 'discriminant is strictly positive, the two solutions are:',
                'x': ['{0:0.3f}'.format((-b - sqrt(d)) / (2 * a)),
                      '{0:0.3f}'.format((-b + sqrt(d)) / (2 * a))]}

    if b != 0:
        x = - c / b
        return {'message': 'Linear equation, one solution', 'x': [x]}

    if c != 0:
        return {'message': 'No solution', 'x': []}

    return {'message': 'All the real numbers are solution', 'x': []}


def main():
    if len(sys.argv) != 2:
        exit('Wrong arguments')

    expr = sys.argv[1]

    if not re.match(expr_pattern, expr):
        exit('Expression not valid')

    print('Input expression:', expr)

    params = get_params(expr)
    print('Reduced Form: ', get_reduced_form(params))

    polynomial_degree = get_polynomial_degree(params)
    print('Polynomial degree: ', polynomial_degree)

    if polynomial_degree > 2:
        exit('The polynomial degree is stricly greater than 2, I can\'t solve.')

    a = params.get(2, 0)
    b = params.get(1, 0)
    c = params.get(0, 0)

    res = solve(a, b, c)

    print(res['message'])
    if len(res['x']) == 1:
        print('x = {0:0.3f}'.format(res['x'][0]))
    if len(res['x']) == 2:
        print('x1 = {0}, x2 = {1}'.format(res['x'][0], res['x'][1]))


if __name__ == '__main__':
    main()

# "15 * x^0 - 2 * x^1 - 1 * x^2 = 0 * x^3"
# 3 -5

# "1 * x^2 - 2 * x^1 - 3 * x^0 = 0 * x^8"
# -1 3

# "1 * x^2 + 12 * x^1 + 36 * x^0 = 0 * x^4"
# -6

# "5 * x^0 + 4 * X^1 + 1 * X^2 = 1 * X^2"
# -1.25
