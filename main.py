#! /usr/bin/env python

import re
import sys

side_pattern = '\d+(\.\d+)? \* (x|X)\^\d+( [\+\-] \d+(\.\d+)? \* (x|X)\^\d+)*'
expr_pattern = '^{0} = {0}$'.format(side_pattern)
elem_pattern = '((?P<sign>\+|-) )?(?P<var>\d+(\.\d+)?) \* (X|x)\^(?P<degree>\d+)'


def abs(x):
    return x if x >= 0 else -x


def sign(x):
    return '-' if x < 0 else '+'


def mysqrt(x):
    if x == 0:
        return float(0)
    if x > 0:
        if x == 1:
            return float(1)
        left = 1
        right = int(x / 2) + 1
        while left <= right:
            mid = int((left + right) / 2)
            square = mid * mid
            if square == x:
                return mid
            if square > x:
                right = mid - 1
            else:
                left = mid + 1
    else:
        pass


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
    if len(sides) != 2:
        print('No "=" sign')
        exit(0)
    left_side_elems = get_elements(sides[0].strip())
    right_side_elems = get_elements(sides[1].strip(), sign=-1)
    all_elems = left_side_elems + right_side_elems

    # sum all elements with similar degrees
    params = dict()
    for elem in all_elems:
        params[elem['degree']] = params.get(elem['degree'], 0) + elem['var']
    return params


def get_polynomial_degree(params):
    return max(params.keys())


def get_reduced_form(params):
    reduced_form = str()
    # при выводе параметры сортируются в порядке возростания
    for k in sorted(params.keys()):
        if params[k] != 0:
            if abs(params[k]) == 1:
                reduced_form += '{0} X^{1} '.format(sign(params[k]), k)
            else:
                reduced_form += '{0} {1} * X^{2} '.format(sign(params[k]), abs(params[k]), k)
    if not reduced_form:
        reduced_form += '0'
    # убирает '+ ' вначале
    reduced_form = reduced_form.strip('+ ') + ' = 0'
    # убирает .0
    reduced_form = reduced_form.replace('.0 ', ' ')
    return reduced_form


def solve(a, b=0, c=0):
    if a != 0:
        d = b * b - 4 * a * c
        print('d = {}'.format(d))
        if d < 0:
            x = (-b + d ** 0.5) / (2 * a)
            return {'message': 'Square equation, discriminant less than zero, complex solution',
                    'x': ['{0.real:.2f} + {0.imag:.2f}i'.format(x),
                          '{0.real:.2f} - {0.imag:.2f}i'.format(x)]
                    }
        if d == 0:
            return {'message': 'Square equation, one solution', 'x': [-b / (2 * a)]}

        return {'message': 'discriminant is strictly positive, the two solutions are:',
                'x': ['{0:0.3f}'.format((-b - d ** 0.5) / (2 * a)),
                      '{0:0.3f}'.format((-b + d ** 0.5) / (2 * a))]}

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
    # при решении параметры сортируются в порядке спадания степени
    params = [params[x] for x in sorted(params.keys(), reverse=True)]
    res = solve(*params[:3])
    print(res['message'])
    if len(res['x']) == 1:
        print('x = {0}'.format(res['x'][0]))
    if len(res['x']) == 2:
        print('x1 = {0}, x2 = {1}'.format(res['x'][0], res['x'][1]))


from math import sqrt
if __name__ == '__main__':
    # main()
    a = 9348570292345236
    res = mysqrt(a * a)
    print(a)
    print(res)
    if res == a:
        print('zaebis')
    b = 1
    print(sqrt(b))
    print(mysqrt(b))
