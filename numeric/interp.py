"""
Interpolation methods
=====================
"""
from abc import ABCMeta, abstractmethod
from math import prod
import numpy as np


class _Lk():

    def __init__(self, x: np.ndarray, k: int):

        self.k = k
        self.nodes = x

    def __call__(self, x: np.ndarray) -> np.ndarray:
        nodes = self.nodes
        k = self.k
        return prod([(x - node) / (nodes[k] - node) for i, node in enumerate(nodes) if i != k])


class PolyInt():
    """Polynomial interpolation implementation using Lagrange polynomials.


    Attributes
    ----------
    nodes : (n, ) ndarray
        Grid nodes in which there are values of the interpolated function.
    values : (n, ) ndarray
        The values of the function in the nodes of the grid in which there are values of the interpolated function.

    Methods
    -------
    __call__(x)


    See Also
    --------
    LinearSplines1d : Linear splines interpolation implementation.
    CubicHermiteSplines1d : Cubic splines interpolation implementation using Hermite polynomials.
    """

    def __init__(self, nodes: np.ndarray, values: np.ndarray) -> None:

        self.nodes = nodes
        self.values = values

    def __call__(self, x: np.ndarray) -> np.ndarray:
        values = self.values
        nodes = self.nodes
        return sum([yk*_Lk(nodes, k)(x) for k, yk in enumerate(values)])


class _BaseSplines1d(metaclass=ABCMeta):

    def __init__(self, nodes: np.ndarray, values: np.ndarray):

        assert nodes.shape == values.shape, "Nodes and their values vectors must have equal lenghs."

        self.nodes = nodes
        self.values = values

    @abstractmethod
    def _spline_func(self, x, y, segment):
        pass

    @abstractmethod
    def __call__(self, x: np.ndarray) -> np.ndarray:
        pass


class LinearSplines1d(_BaseSplines1d):
    """Linear splines interpolation implementation.


    Attributes
    ----------
    nodes : (n, ) ndarray
        Grid nodes in which there are values of the interpolated function.
    values : (n, ) ndarray
        The values of the function in the nodes of the grid in which there are values of the interpolated function.

    Methods
    -------
    __call__(x)


    See Also
    --------
    PolyInt : Polynomial interpolation implementation using Lagrange polynomials.
    CubicHermiteSplines1d : Cubic splines interpolation implementation using Hermite polynomials.
    """

    def _spline_func(self, x, y, segment):
        node_0, node_1 = x
        val_0, val_1 = y
        slope = (segment - node_0) / (node_1 - node_0)
        return val_0 + slope * (val_1 - val_0)

    def __call__(self, x):

        nodes = self.nodes
        values = self.values

        solution = np.ones(x.shape, dtype=x.dtype) * np.nan

        for i, _ in enumerate(nodes[:-1]):

            nodes_segment =  nodes[[i, i+1]]
            values_segment = values[[i, i+1]]
            mapp = np.logical_and((nodes_segment[0] <= x), (x <= nodes_segment[1]))
            segment = x[mapp]
            solution[mapp] = self._spline_func(nodes_segment, values_segment, segment)

        return solution


class CubicHermiteSplines1d(_BaseSplines1d):
    """Cubic splines interpolation implementation using Hermite polynomials.


    Attributes
    ----------
    nodes : (n, ) ndarray
        Grid nodes in which there are values of the interpolated function.
    values : (n, ) ndarray
        The values of the function in the nodes of the grid in which there are values of the interpolated function.

    Methods
    -------
    __call__(x)


    See Also
    --------
    PolyInt : Polynomial interpolation implementation using Lagrange polynomials.
    LinearSplines1d : Linear splines interpolation implementation.
    """

    def _spline_func(self, x, y, dydx, segment):

        dt = x[1] - x[0]
        t = (segment - x[0]) / dt

        h00 = 2 * t**3 - 3 * t**2 + 1
        h10 = t**3 - 2 * t**2 + t
        h01 = -2 * t**3 + 3 * t**2
        h11 = t**3 - t**2

        return h00 * y[0] + h10 * dt * dydx[0] + h01 * y[1] + h11 * dt * dydx[1]

    def __call__(self, x):

        nodes = self.nodes
        values = self.values

        derivative = np.zeros_like(nodes)
        derivative[1:-1] = (values[2:] - values[:-2]) / (nodes[2:] - nodes[:-2])

        solution = np.ones(x.shape, dtype=x.dtype) * np.nan

        for i in range(len(nodes)-1):

            nodes_segment = nodes[i: i+2]
            values_segment = values[i: i+2]
            derivative_segment = derivative[i: i+2]

            mapp = np.logical_and((nodes_segment[0] <= x), (x <= nodes_segment[1]))
            segment = x[mapp]

            solution[mapp] = self._spline_func(nodes_segment, values_segment, derivative_segment, segment)

        return solution
