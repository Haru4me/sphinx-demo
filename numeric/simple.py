"""
Simple operations
=================

Определение производной первого порядка функции одной переменной определяется как

.. math::
    \dfrac{df}{dx} = \lim\limits_{h \\to 0}\dfrac{f(x+h) - f(x)}{h}

численно может быть рассчитана при фиксированной :math:`h`

.. math::
    f'(x) \\approx \dfrac{f(x+h) - f(x)}{h}

.. math::
    f'(x) \\approx \dfrac{f(x) - f(x-h)}{h}

.. math::
    f'(x) \\approx \dfrac{f(x+h) - f(x-h)}{2h}

Можно показать точность данных приближений через многочлен тейлора

.. math::

    f(x) = f(a+h) = f(a) + f'(a)h + O(h) \Rightarrow f'(a) = \dfrac{f(a+h) - f(a)}{h} + O(h)

Аналогично

.. math::
    f(x) = f(a-h) = f(a) - f'(a)h + O(h) \Rightarrow f'(a) = \dfrac{f(a) - f(a-h)}{h} + O(h)

Последнее приближение получено из двух многочленов Тейлора

.. math::
    f(x) = f(a+h) = f(a) + f'(a)h + \dfrac{f''(a)}{2}h^2 + O(h^2)

    f(x) = f(a-h) = f(a) - f'(a)h + \dfrac{f''(a)}{2}h^2 + O(h^2)

Вычтем одно из другого и получим

.. math::
    f(a+h) - f(a-h) = 2f'(a)h + O(h^2) \Rightarrow f'(a) = \dfrac{f(a+h) - f(a-h)}{2h} + O(h^2)

Вторая производная может быть рассчитана как (тоже через Тейлора и подстановку приближения первой производной)

.. math::
    f''(a) = \dfrac{f(a+h) - 2f(a) + f(a+h)}{h^2}

.. math::
    f(a+h) + f(a+h) = 2f(a) + f''(a)h^2 + O(h^2) \Rightarrow

    \Rightarrow f''(a) = \dfrac{f(a+h) + f(a+h) - 2f(a)}{h^2} + O(h^2)
"""

from typing import Callable
import numpy as np

def derivative(func: Callable, start: float, end: float, h: float = 0.1, type: str = 'central') -> np.ndarray:
    """First derivative for function of one variable.

    Parameters
    ----------
    func : Callable[np.ndarray] -> np.ndarray
        The function that will be differentiated.
        The function must be one-dimensional.
    start : float
        The initial value of the segment on
        which the derivative is calculated.
    end : float
        The final value of the segment on
        which the derivative is considered.
    h : float, default: `0.1`
        Differentiation step.
    type : str {'left', 'right', 'central'}, default: `central`
        Type of difference approximation of the first derivative.

    Returns
    -------
    x : (n, ) ndarray
        Nodes of the grid on which differentiation is carried out.
    f'(x) : (n, ) ndarray
        Numerical values of the derivative in the grid nodes.

    See Also
    --------
    second_derivative : Second derivative for function of one variable.

    Notes
    -----
    The difference schemes look like this:
        - left: :math:`f'(x) \\approx \dfrac{f(x+h) - f(x)}{h}`
        - right: :math:`f'(x) \\approx \dfrac{f(x+h) - f(x)}{h}`
        - central :math:`f'(x) \\approx \dfrac{f(x+h) - f(x-h)}{2h}`

    References
    ----------
    For more information folow the `link <https://en.wikipedia.org/wiki/Numerical_differentiation>`_.

    Examples
    --------

    >>> h, start, end = 0.1, -2*np.pi, 2*np.pi
    >>> x = np.arange(start, end+h, h)
    >>> func = lambda x: np.sin(x)/np.cosh(x)*x**2
    >>> df = derivative(func, h=h, start=start, end=end)
    """
    schemes = {
        'left': lambda f, x, h: (f(x+h) - f(x)) / h,
        'right': lambda f, x, h: (f(x) - f(x-h)) / h,
        'central': lambda f, x, h: (f(x+h) - f(x-h)) / 2 / h
    }

    scheme = schemes[type]
    x = np.arange(start, end+h, h)

    return x, scheme(func, x, h)

def second_derivative(func: Callable, start: np.ndarray, end: np.ndarray, h: float = 0.1) -> np.ndarray:
    """Second derivative for function of one variable.

    Parameters
    ----------
    func : Callable[np.ndarray] -> np.ndarray
        The function that will be differentiated.
        The function must be one-dimensional.
    start : float
        The initial value of the segment on
        which the derivative is calculated.
    end : float
        The final value of the segment on
        which the derivative is considered.
    h : float, default: `0.1`
        Differentiation step.

    Returns
    -------
    x : (n, ) ndarray
        Nodes of the grid on which differentiation is carried out.
    f''(x) : (n, ) ndarray
        Numerical values of the derivative in the grid nodes.

    See Also
    --------
    derivative : First derivative for function of one variable.

    Notes
    -----
    The difference scheme look like this:
        - :math:`f''(a) \\approx \dfrac{f(x+h) + f(x+h) - 2f(x)}{h^2}`

    References
    ----------
    For more information folow the `link <https://en.wikipedia.org/wiki/Numerical_differentiation>`_.

    Examples
    --------

    >>> h, start, end = 0.1, -2*np.pi, 2*np.pi
    >>> x = np.arange(start, end+h, h)
    >>> func = lambda x: np.sin(x)/np.cosh(x)*x**2
    >>> ddf = second_derivative(func, h=h, start=start, end=end)
    """
    x = np.arange(start, end+h, h)
    return x, (func(x+h) + func(x-h) - 2*func(x)) / h / h


def cheb_poly_1(x: np.ndarray, n: int) -> np.ndarray:
    """Chebyshev polynomials of the first kind.

    Parameters
    ----------
    x : (n, ) ndarrray
        Array of values of the Chebyshev function argument.
    n : int
        Chebyshev polynomial degree.

    Returns
    -------
    Tn(x) : (n, ) ndarray
        Array of Chebyshev function values of order `n` in nodes `x`.

    See Also
    --------
    cheb_poly_2 : Chebyshev polynomials of the second kind.

    Notes
    -----


    References
    ----------
    For more information folow the `link <https://en.wikipedia.org/wiki/Chebyshev_polynomials>`_.

    Examples
    --------

    >>> x = np.linspace(-1,1,100)
    >>> y = cheb_poly_1(x, 3)
    """
    i0 = np.ones_like(x)
    i1 = x

    if n == 0:
        res = i0
    elif n == 1:
        res = i1
    else:
        for i in range(2, n+1):
            res = 2*x*i1 - i0
            i0 = i1
            i1 = res

    return res


def cheb_poly_2(x: np.ndarray, n: int) -> np.ndarray:
    """Chebyshev polynomials of the secoond kind.

    Parameters
    ----------
    x : (n, ) ndarrray
        Array of values of the Chebyshev function argument.
    n : int
        Chebyshev polynomial degree.

    Returns
    -------
    Un(x) : (n, ) ndarray
        Array of Chebyshev function values of order `n` in nodes `x`.

    See Also
    --------
    cheb_poly_1 : Chebyshev polynomials of the first kind.

    Notes
    -----


    References
    ----------
    For more information folow the `link <https://en.wikipedia.org/wiki/Chebyshev_polynomials>`_.

    Examples
    --------

    >>> x = np.linspace(-1,1,100)
    >>> y = cheb_poly_2(x, 3)
    """

    i0 = np.ones_like(x)
    i1 = 2*x

    if n == 0:
        res = i0
    elif n == 1:
        res = i1
    else:
        for _ in range(2, n+1):
            res = 2*x*i1 - i0
            i0 = i1
            i1 = res

    return res
