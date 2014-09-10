import math
import itertools
from fraction_solution import NumeralSystem, NumeralSystemNumber


def convert_base(x, base=3, precision=None):
    length_of_int = int(math.log(x, base))
    iexps = range(length_of_int, -1, -1)
    if precision == None: fexps = itertools.count(-1, -1)
    else: fexps = range(-1, -int(precision + 1), -1)

    def cbgen(x, base, exponents):
        for e in exponents:
            d = int(x // (base ** e))
            x -= d * (base ** e)
            yield d
            if x == 0 and e < 0: break

    return cbgen(int(x), base, iexps), cbgen(x - int(x), base, fexps)

for dividend in range(1, 1000):
    for divisor in range(1, 100):
        for base in range(2, 10):
            ns = NumeralSystem(base)
            n1 = NumeralSystemNumber(dividend, ns)
            n2 = NumeralSystemNumber(divisor, ns)
            res = str(n1.divide(n2))
            res = res.replace('(', '')
            res = res.replace(')', '')[:16]

            first, second = convert_base(dividend / divisor, base=base, precision=15)
            first = ''.join(map(str, first))
            second = ''.join(map(str, second))
            answer = '{}.{}'.format(first or '0', second)[:len(res)]

            if res != answer:
                print('{}/{} {}'.format(dividend, divisor, base))
                print(res)
                print(answer)