def test(x, g):
    i = 0
    while True:
        # print(g)
        if abs(x/g - x) < 0.001:
            return g
        else:
            g = (g + x / g) / 2
        i += 1


if __name__ == '__main__':
    x = 2
    result = test(x * x, 1)

    print(x)
    print(result)
    print(x == result)
