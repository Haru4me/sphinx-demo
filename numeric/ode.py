"""
ODE solving methods
===================

Ordinary differential equation (ODE) solving methods implementation.

Главная идея решения задачи Коши ОДУ заключается в апроксимации интеграла аналитического решения.

Положим, у нас есть задача Коши первого порядка ОДУ

.. math::
        \dfrac{dy}{dx} = f(y,x),~y(x_0) = y_0

Возьмем произвольную точку :math:`x_1` так, что :math:`x_1 = x_0 + \\varepsilon`. Тогда выпишем интеграл

.. math::
    dy = f(y,x)dx \Rightarrow \int\limits_{y_0}^{y_1}dy = \int\limits_{x_0}^{x_1}f(y,x)dx \Rightarrow

    \Rightarrow y_1 - y_0 = \int\limits_{x_0}^{x_1}f(y,x)dx \Rightarrow y_1 =  y_0 + \int\limits_{x_0}^{x_1}f(y,x)dx
"""
from abc import ABCMeta, abstractmethod
from typing import Callable
import numpy as np


class _BasedODE(metaclass=ABCMeta):
    """Base class for all ODE solvers.
    """

    def __init__(self, func: Callable, y0: np.ndarray, step_size: float = None, grid_constr: Callable = None, interp: str = 'linear'):

        self.func = func
        self.y0 = y0
        self.interp = interp

        if grid_constr is not None:
            self.grid_constr = grid_constr
        elif grid_constr is None and step_size is not None:
            print(self._grid_step_size(0.01))
            self.grid_constr = self._grid_step_size(step_size)
        elif grid_constr is None and step_size is None:
            self.grid_constr = lambda f, y0, t: t
        else:
            raise ValueError("step_size and grid_constr are mutually exclusive arguments.")

    @abstractmethod
    def _step(self, func, t0, dt, t1, y):
        pass

    @staticmethod
    def _grid_step_size(step_size: float) -> np.ndarray:

        def _grid_constr(func, y0, t):
            start_time = t[0]
            end_time = t[-1]
            niters = int(np.ceil(np.abs(end_time - start_time) / step_size + 1))
            return np.linspace(start_time, end_time, niters)

        return _grid_constr

    def _linear_interp(self, t0, t1, y0, y1, t):
        slope = (t - t0) / (t1 - t0)
        return y0 + slope * (y1 - y0)

    def _cubic_hermite_interp(self, t0, y0, f0, t1, y1, f1, t):
        pass

    def __call__(self, t):
        """Calculate solution for `t`
        
        Parameters
        ----------
        t : (n, ) np.ndarray
            Values of time.

        Returns
        -------
        y(t) : (n, ) ndarray
            Solving of equation.

        """
        y0 = self.y0

        time_grid = self.grid_constr(self.func, y0, t)
        assert time_grid[0] == t[0] and time_grid[-1] == t[-1], "grid and real edge points must be equal."

        solution = np.empty((t.shape[0], *y0.shape), dtype=y0.dtype)
        solution[0] = y0

        i = 1
        for t0, t1 in zip(time_grid[:-1], time_grid[1:]):

            dt = t1 - t0
            dy = self._step(self.func, t0, dt, t1, y0)
            y1 = y0 + dy

            while i < t.shape[0] and t1 >= t[i]:

                if self.interp == 'linear':
                    solution[i] = self._linear_interp(t0, t1, y0, y1, t[i])
                elif self.interp == 'cubic':
                    pass
                else:
                    try:

                        f0 = self.func(t0, y0)
                        f1 = self.func(t1, y1)

                        self.interp(t0, y0, f0, t1, y1, f1, t[i])

                    except TypeError:
                        raise TypeError(f"interp must be 'linear', 'cubic' or Callable not {self.interp}.")
                i += 1

            y0 = y1

        return solution


class EulerSolver(_BasedODE):
    """Euler ODE solver implementation.


    Attributes
    ----------
    func : Callable
        Функция первой производной func(t, y).
    y0 : float or (n, ) ndarray
        Начальное значение задачи Коши.
    step_size : float or None, optional, default: None
        Шаг сетки, на которой решается задача.
    grid_constr : Callable, optional, default: None
        Функция, строящая сетку, на которой будет решаться задача Коши.
    interp : {`linear`, `cubic`} or Callable, optional, default: `linear`
        Функция интерполяции для проекции решения с сетки в моменты времени `t`.

    See Also
    --------
    SimpsonSolver : ODE solver implementation with Smipson integrate approximation.
    RK4Solver : Runge-Kutta ODE solver implementation.

    Notes
    -----
    Интеграл аппроксимируется методом прямоугольника:
        - :math:`\int\limits_{x_0}^{x_0 + h}f(y,x)dx \\approx hf(y_0, x_0)`
    """
    def _step(self, func, t0, dt, t1, y):
        return dt*func(t0, y)


class SimpsonSolver(_BasedODE):
    """ODE solver implementation with Smipson integrate approximation.


    Attributes
    ----------
    func : Callable
        Функция первой производной func(t, y).
    y0 : float or (n, ) ndarray
        Начальное значение задачи Коши.
    step_size : float or None, optional, default: None
        Шаг сетки, на которой решается задача.
    grid_constr : Callable, optional, default: None
        Функция, строящая сетку, на которой будет решаться задача Коши.
    interp : {`linear`, `cubic`} or Callable, optional, default: `linear`
        Функция интерполяции для проекции решения с сетки в моменты времени `t`.

    See Also
    --------
    EulerSolver : Euler ODE solver implementation.
    RK4Solver : Runge-Kutta ODE solver implementation.
    """

    def _step(self, func, t0, dt, t1, y):

        q1 = self.func(t0, y)
        q2 = self.func(t0+0.5*dt, y+0.5*q1*dt)
        q3 = self.func(t0+dt, y+0.5*q1*dt+0.5*q2*dt)

        return dt*(q1+4*q2+q3)/6


class RK4Solver(_BasedODE):
    """Runge-Kutta ODE solver implementation.


    Attributes
    ----------
    func : Callable
        Функция первой производной func(t, y).
    y0 : float or (n, ) ndarray
        Начальное значение задачи Коши.
    step_size : float or None, optional, default: None
        Шаг сетки, на которой решается задача.
    grid_constr : Callable, optional, default: None
        Функция, строящая сетку, на которой будет решаться задача Коши.
    interp : {`linear`, `cubic`} or Callable, optional, default: `linear`
        Функция интерполяции для проекции решения с сетки в моменты времени `t`.

    See Also
    --------
    EulerSolver : Euler ODE solver implementation.
    SimpsonSolver : ODE solver implementation with Smipson integrate approximation.
    """

    def _step(self, func, t0, dt, t1, y):

        q1 = self.func(t0, y)
        q2 = self.func(t0+0.5*dt, y+0.5*q1*dt)
        q3 = self.func(t0+0.5*dt, y+0.5*q2*dt)
        q4 = self.func(t0+dt, y+q3*dt)

        return dt*(q1+2*q2+2*q3+q4)/6
