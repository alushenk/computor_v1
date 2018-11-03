import re

side_pattern = '\d+(\.\d+)? \* (x|X)\^\d+( [\+\-] \d+(\.\d+)? \* (x|X)\^\d+)*'
expr_pattern = '^{0} = {0}$'.format(side_pattern)
elem_pattern = '((?P<sign>\+|-) )?(?P<var>\d+(\.\d+)?) \* (X|x)\^(?P<degree>\d+)'

expr = "1 * X^2 = 2 * X^2"


def abs(x):
    return x if x >= 0 else -x


def sign(x):
    return '-' if x < 0 else '+'


def sqrt(x):
    return x ** 0.5


def get_elements(expression, sign=1):
    elements = list()
    for item in re.finditer(elem_pattern, expression):
        element = item.groupdict()
        if element['sign'] == '-':
            element['var'] = -float(element['var']) * sign
        else:
            element['var'] = float(element['var']) * sign
        if element['sign'] is None:
            element['sign'] = '+'
        element['degree'] = int(element['degree'])
        del element['sign']
        elements.append(element)
    return elements


def get_params(expr):
    print('Input expression:', expr)
    sides = expr.split('=')
    if len(sides) != 2:
        raise ValueError('No "=" sign')
    left_side_elems = get_elements(sides[0].strip())
    right_side_elems = get_elements(sides[1].strip(), sign=-1)
    all_elems = left_side_elems + right_side_elems

    params = dict()
    for elem in all_elems:
        params[elem['degree']] = params.get(elem['degree'], 0) + elem['var']
    return params


def get_polynomial_degree(params):
    return max(params.keys())


def get_reduced_form(params):
    reduced_form = str()
    for k in sorted(params.keys()):
        if params[k] != 0:
            if abs(params[k]) == 1:
                reduced_form += '{0}X^{1} '.format(sign(params[k]), k)
            else:
                reduced_form += '{0}{1} * X^{2} '.format(sign(params[k]), abs(params[k]), k)
    if not reduced_form:
        reduced_form += '0'
    reduced_form = reduced_form.strip('+ ') + ' = 0'
    return reduced_form


def solve(a, b, c):
    if a != 0:
        D = b * b - 4 * a * c
        if D < 0:
            return {'message': 'Square equation, discriminant less than zero, complex solution',
                    'x': [(-b - sqrt(D)) / (2 * a), (-b + sqrt(D)) / (2 * a)]}
        if D == 0:
            return {'message': 'Square equation, one solution', 'x': [-b / (2 * a)]}

        return {'message': 'Square equation, two solutions', 'x': [(-b - sqrt(D)) / (2 * a), (-b + sqrt(D)) / (2 * a)]}

    if b != 0:
        x = - c / b
        return {'message': 'Linear equation, one solution', 'x': [x]}

    if c != 0:
        return {'message': 'No solution', 'x': []}

    return {'message': 'All the real numbers are solution', 'x': []}


if __name__ == '__main__':
    if not re.match(expr_pattern, expr):
        print('Expression not valid')

    params = get_params(expr)
    print('Reduced Form: ', get_reduced_form(params))
    print('Polynomial degree: ', get_polynomial_degree(params))
    print(params)
    res = solve(params[:3])
    print(res['message'])
    if len(res['x']) == 1: print('x = {0}'.format(res['x'][0]))
    if len(res['x']) == 2: print('x1 = {0}, x2 = {1}'.format(res['x'][0], res['x'][1]))
