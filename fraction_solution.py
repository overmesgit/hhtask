"""Solution for Second Test Task of HeadHunter's School

Python3.4

author: Артем Безукладичный
mail: overmes@gmail.com
"""
import argparse
from fractions import gcd


parser = argparse.ArgumentParser(description='Division in different number systems')
parser.add_argument('file', metavar='F', type=open, help='file')
args = parser.parse_args()


def primes_sieve2(limit):
    """Get primes http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    """
    a = [True] * limit                          # Initialize the primality list
    a[0] = a[1] = False

    for (i, isprime) in enumerate(a):
        if isprime:
            yield i
            for n in range(i*i, limit, i):     # Mark factors non-prime
                a[n] = False


def base_10_to_custom_base(number, base):
    """Convert number to custom base
    """
    result = []
    next_remainder = number
    while next_remainder != 0:
        result.insert(0, next_remainder % base)
        next_remainder = next_remainder // base
    return result or [0]


def get_reduced_numbers(dividend, divisor):
    """Reduce numbers by divisor while they have common divisor
    """
    current_dividend = dividend
    current_divisor = divisor

    current_gcd = gcd(current_dividend, current_divisor)
    while current_gcd != 1:
        current_dividend /= current_gcd
        current_divisor /= current_gcd
        current_gcd = gcd(current_dividend, current_divisor)
    return int(current_dividend), int(current_divisor)


class NumeralSystem:
    """Class for representation numeral system

    """
    prime_factors = None

    def __init__(self, base):
        if base < 2:
            raise ValueError("Wrong base")
        self.base = base

    def get_prime_factors(self):
        """Find numeral system prime factors if not found before
        """
        if self.prime_factors is None:
            self.prime_factors = []
            for prime in primes_sieve2(int(self.base/2 + 1)):
                if not self.base % prime:
                    self.prime_factors.append(prime)
        return self.prime_factors

    def get_not_cyclic_part_for_divisor(self, divisor):
        """Find max a in
        divisor = n0 * (prime_divisor**a) where (n0, base) = 1
        or
        divisor = n0 * (base**a) where (n0, base) = 1

        more info http://mathworld.wolfram.com/DecimalExpansion.html
        """
        max_power = 0

        for prime_factor in self.get_prime_factors() or [self.base]:
            powered_prime = prime_factor
            current_power = 1
            while powered_prime <= self.base:
                if not (divisor % powered_prime) and max_power < current_power:
                    max_power = current_power
                current_power += 1
                powered_prime = prime_factor ** current_power
        return max_power

    def get_cyclic_part_for_divisor(self, divisor):
        """find s and t in
        10**s = 10**(s + t) (mod divisor)

        more info http://mathworld.wolfram.com/DecimalExpansion.html
        """
        mod_results = {}

        current_power = 0
        while True:
            mod_result = self.base**current_power % divisor
            if mod_result == 0:
                return 0
            if mod_result in mod_results:
                return current_power - mod_results[mod_result]
            else:
                mod_results[mod_result] = current_power
                current_power += 1


class DivisionResult:
    def __init__(self, dividend, divisor, base, whole_part, not_cyclic_part, cyclic_part):
        self.dividend = dividend
        self.divisor = divisor
        self.whole_part = whole_part
        self.fraction_not_cyclic_part = not_cyclic_part
        self.fraction_cyclic_part = cyclic_part
        self.base = base
        self.delimiter = '' if base <= 10 else ' '

    def number_list_to_str(self, numbers):
        return self.delimiter.join(map(str, numbers)) if numbers else ''

    def __str__(self):
        str_resutl = self.number_list_to_str(self.whole_part)
        if self.fraction_not_cyclic_part or self.fraction_cyclic_part:
            str_resutl += '.'
            str_resutl += '{}'.format(self.number_list_to_str(self.fraction_not_cyclic_part))
            if self.fraction_cyclic_part:
                str_resutl += '({})'.format(self.number_list_to_str(self.fraction_cyclic_part))
        return str_resutl


class NumeralSystemNumber:
    """Class for representation number in custom numeral system

    """
    def __init__(self, number, base):
        self.number = number
        self.base = base

    def is_proper_divisor(self, other):
        same_ns = self.base.base == other.base.base
        return isinstance(other, NumeralSystemNumber) and same_ns

    def divide(self, divisor):
        if not self.is_proper_divisor(divisor):
            raise ValueError('Wrong divisor')

        reduced_dividend, reduced_divisor = get_reduced_numbers(self.number, divisor.number)
        not_cyclic_part, cyclic_part = self.get_fractional_part(reduced_dividend, reduced_divisor)
        whole_part = self.get_whole_part(reduced_dividend, reduced_divisor)

        return DivisionResult(self.number, divisor.number, self.base.base, whole_part, not_cyclic_part, cyclic_part)

    def get_fractional_part(self, dividend, divisor):
        """Find fraction part in custom base
        """
        next_dividend = dividend % divisor
        not_cyclic_part_len = self.base.get_not_cyclic_part_for_divisor(divisor)
        cyclic_part_len = self.base.get_cyclic_part_for_divisor(divisor)

        result_list = []
        for i in range(0, not_cyclic_part_len+cyclic_part_len):
            next_dividend *= self.base.base
            result_list.append(next_dividend // divisor)
            next_dividend = next_dividend % divisor

        if not cyclic_part_len:
            result_list = self.remove_end_zeros(result_list)
            not_cyclic_part_len = len(result_list)

        return result_list[0:not_cyclic_part_len], result_list[not_cyclic_part_len:]

    def remove_end_zeros(self, result_list):
        count = 0
        for num in reversed(result_list):
            if num == 0:
                count += 1
            else:
                break
        if count:
            return result_list[:-count]
        else:
            return result_list

    def get_whole_part(self, dividend, divisor):
        """find a/b in current base
        """
        return base_10_to_custom_base(dividend // divisor, self.base.base)


for row in args.file:
    dividend, divisor, base = [int(n) for n in row.split()]
    ns = NumeralSystem(base)
    n1 = NumeralSystemNumber(dividend, ns)
    n2 = NumeralSystemNumber(divisor, ns)

    res = n1.divide(n2)
    print(res)