import re
import sys
import cmath

side_pattern = '\d+(\.\d+)? \* (x|X)\^\d+( [\+\-] \d+(\.\d+)? \* (x|X)\^\d+)*'
expr_pattern = '^{0} = {0}$'.format(side_pattern)
elem_pattern = '((?P<sign>\+|-) )?(?P<var>\d+(\.\d+)?) \* (X|x)\^(?P<degree>\d+)'

expr = "1 * x^2 - 8 * x^1 + 12 * x^0 = 0"
expr = "1 * x^2 + 3 * x^1 + 3 * x^0 = 0"


def abs(x):
    return x if x >= 0 else -x


def sign(x):
    return '-' if x < 0 else '+'


from math import sqrt


#
# def sqrt(x):
#     return x ** 0.5


# def sqrt(x):
#     x = float(x)
#     root = x / 2
#     for i in range(1000):
#         if root is 0:
#             return root
#         root = (root + x / root) / 2
#         print(root)
#     return root


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
    print('a={} b={} c={}'.format(a, b, c))
    if a != 0:
        D = b * b - 4 * a * c
        print('D = {}'.format(D))
        if D < 0:
            return {'message': 'Square equation, discriminant less than zero, complex solution',
                    # можно сделать решение с комплексными числами
                    'x': [(-b - cmath.sqrt(D)) / (2 * a),
                          (-b + cmath.sqrt(D)) / (2 * a)]
                    }
        if D == 0:
            return {'message': 'Square equation, one solution', 'x': [-b / (2 * a)]}

        return {'message': 'Discriminant is strictly positive, the two solutions are:',
                'x': [(-b - sqrt(D)) / (2 * a),
                      (-b + sqrt(D)) / (2 * a)]}

    if b != 0:
        x = - c / b
        return {'message': 'Linear equation, one solution', 'x': [x]}

    if c != 0:
        return {'message': 'No solution', 'x': []}

    return {'message': 'All the real numbers are solution', 'x': []}


def main():
    if not re.match(expr_pattern, expr):
        print('Expression not valid')

    print('Input expression:', expr)
    params = get_params(expr)
    print('Reduced Form: ', get_reduced_form(params))
    polynomial_degree = get_polynomial_degree(params)
    print('Polynomial degree: ', polynomial_degree)
    if polynomial_degree > 2:
        exit(0)
    # при решении параметры сортируются в порядке спадания степени
    params = [params[x] for x in sorted(params.keys(), reverse=True)]
    res = solve(*params[:3])
    print(res['message'])
    if len(res['x']) == 1: print('x = {0}'.format(res['x'][0]))
    if len(res['x']) == 2: print('x1 = {0}, x2 = {1}'.format(res['x'][0], res['x'][1]))


if __name__ == '__main__':
    main()
    # sqrt(4345820390043958938279048578029358 * 4345820390043958938279048578029358)
