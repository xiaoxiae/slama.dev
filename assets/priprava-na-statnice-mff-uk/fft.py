from typing import *
from math import pi, e

i = complex(0, 1)


def even(l): return [x for i, x in enumerate(l) if i % 2 == 0]


def odd(l): return [x for i, x in enumerate(l) if i % 2 == 1]


def round_complex(c, d=5):
    """A complex numbers rounding function for prettier outputs."""
    a = round(c.real, d)
    b = round(c.imag, d) * 1j

    return a if c.imag < (1/10 ** d) else a + b


def _fft(w: complex, p: List[int]) -> List[int]:
    """The recursive FFT implementation using complex numbers."""
    n = len(p)

    if n == 1:
        return p

    # we'll recursively get n/2 points from each of the two sub-polynomials
    e = _fft(w ** 2, even(p))
    o = _fft(w ** 2, odd(p))

    # we're using the fact that the polynomial is in the form P(x) = P_e(x^2) ± x·P_o(x^2)
    # another fact that we're using is that w^{n/2 + j} = -w^j
    y = [0] * n
    for j in range(n // 2):
        y[j] = e[j] + w ** j * o[j]
        y[j + n // 2] = e[j] - w ** j * o[j]

    return y


def fft(p: List[int]) -> List[int]:
    """Evaluates a polynomial given by coefficients p in len(p) complex points."""
    n = len(p)
    return _fft(e ** (2 * i * pi / n), p)


def inverse_fft(p: List[int]) -> List[int]:
    """Calculates the polynomial of degree len(p) that passes through the p complex points."""
    n = len(p)
    return [x / n for x in _fft(-(e ** (2 * i * pi / n)), p)]


def multiply_polynomials(p: List[int], q: List[int]):
    """Multiply two polynomials, given their coefficients (rising)."""
    deg = len(p) + len(q) - 1

    n = 1
    while n <= deg:
        n *= 2

    py = fft(p + [0] * (n - len(p)))
    qy = fft(q + [0] * (n - len(q)))

    y = [0] * n
    for i in range(n):
        y[i] = py[i] * qy[i]

    return list(map(round_complex, inverse_fft(y)))


print(multiply_polynomials([-5, 1], [-6, 4, 1]))
print(multiply_polynomials([3, 8, -4, 1], [-3, 7, 2]))
