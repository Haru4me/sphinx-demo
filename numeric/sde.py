import numpy as np


class ConvectionDiffusionEquationSolver1d:

    def __init__(self,
                 u0: Callable,
                 ua: Callable,
                 time_step: float = None,
                 space_step: float = None,
                 grid_constr: Callable = None):

        self.u0 = u0
        self.ua = ua
        self.tau = time_step
        self.h = space_step

        if grid_constr is not None:
            self.time_grid_constr = grid_constr
            self.space_grid_constr = grid_constr
        elif grid_constr is None and time_step is not None and space_step is not None:
            self.time_grid_constr = self._grid_step_size(time_step)
            self.space_grid_constr = self._grid_step_size(space_step)
        elif grid_constr is None and time_step is None and space_step is None:
            self.time_grid_constr = lambda val: val
            self.space_grid_constr = lambda val: val
        else:
            raise ValueError("step_size and grid_constr are mutually exclusive arguments.")

    @staticmethod
    def _grid_step_size(step_size: float) -> np.ndarray:

        def _grid_constr(val):
            start = val[0]
            end = val[-1]
            niters = int(np.ceil(np.abs(end - start) / step_size + 1))
            return np.linspace(start, end, niters)

        return _grid_constr

    @staticmethod
    def _coef_matrix(i, sigma, lam, u):

        n = u.shape[1] - 2
        #A = -lam * sigma * np.eye(n, k=1)
        #A += (1 + 2 * lam * sigma) * np.eye(n)
        #A -= lam * sigma * np.eye(n, k=-1)

        return A

    @staticmethod
    def _ordinate_values(i, sigma, lam, u):

        #b = (1 - 2 * sigma) * lam * u[i-1, 2:]
        #b += 2 * (1 - lam * (1 - 2 * sigma)) * u[i-1, 1:-1]
        #b += (1 - 2 * sigma) * lam * u[i-1, :-2]
        #b += sigma * lam * u[i-2, 2:]
        #b -= (1 + 2 * lam * sigma) * u[i-2, 1:-1]
        #b += lam * sigma * u[i-2, :-2]

        return b

    def __call__(self, t, x, sigma=1.):

        u0 = self.u0
        ua = self.ua

        time_grid = self.time_grid_constr(t)
        space_grid = self.space_grid_constr(x)

        tau, h = (self.tau, self.h) if self.tau is not None and self.tau is not None \
                         else (time_grid[1] - time_grid[0], space_grid[1] - space_grid[0])
        lam = tau / h

        assert time_grid[0] == t[0] and time_grid[-1] == t[-1], "grid and real edge points must be equal."
        assert space_grid[0] == x[0] and space_grid[-1] == x[-1], "grid and real edge points must be equal."

        solution = np.empty((*time_grid.shape, *space_grid.shape), dtype=x.dtype)

        solution[0] = u0(space_grid)
        solution[:, 0] = ua(time_grid)

        for i in range(2, len(time_grid)):

            A = self._coef_matrix(i, sigma, lam, solution)
            b = self._ordinate_values(i, sigma, lam, solution)

            solution[i, 1:-1] = np.linalg.solve(A,b)

        return solution


class WaveEquationSolver1d:

    def __init__(self,
                 u0: Callable,
                 ut0: Callable,
                 ua: Callable,
                 ub: Callable,
                 time_step: float = None,
                 space_step: float = None,
                 grid_constr: Callable = None):

        self.u0 = u0
        self.ut0 = ut0
        self.ua = ua
        self.ub = ub
        self.tau = time_step
        self.h = space_step

        if grid_constr is not None:
            self.time_grid_constr = grid_constr
            self.space_grid_constr = grid_constr
        elif grid_constr is None and time_step is not None and space_step is not None:
            self.time_grid_constr = self._grid_step_size(time_step)
            self.space_grid_constr = self._grid_step_size(space_step)
        elif grid_constr is None and time_step is None and space_step is None:
            self.time_grid_constr = lambda val: val
            self.space_grid_constr = lambda val: val
        else:
            raise ValueError("step_size and grid_constr are mutually exclusive arguments.")

    @staticmethod
    def _grid_step_size(step_size: float) -> np.ndarray:

        def _grid_constr(val):
            start = val[0]
            end = val[-1]
            niters = int(np.ceil(np.abs(end - start) / step_size + 1))
            return np.linspace(start, end, niters)

        return _grid_constr

    @staticmethod
    def _coef_matrix(i, sigma, lam, u):

        n = u.shape[1] - 2
        A = -lam * sigma * np.eye(n, k=1)
        A += (1 + 2 * lam * sigma) * np.eye(n)
        A -= lam * sigma * np.eye(n, k=-1)

        return A

    @staticmethod
    def _ordinate_values(i, sigma, lam, u):

        b = (1 - 2 * sigma) * lam * u[i-1, 2:]
        b += 2 * (1 - lam * (1 - 2 * sigma)) * u[i-1, 1:-1]
        b += (1 - 2 * sigma) * lam * u[i-1, :-2]
        b += sigma * lam * u[i-2, 2:]
        b -= (1 + 2 * lam * sigma) * u[i-2, 1:-1]
        b += lam * sigma * u[i-2, :-2]

        return b

    def __call__(self, t, x, sigma=1.):

        u0 = self.u0
        ut0 = self.ut0
        ua = self.ua
        ub = self.ub

        time_grid = self.time_grid_constr(t)
        space_grid = self.space_grid_constr(x)

        tau, h = (self.tau, self.h) if self.tau is not None and self.tau is not None \
                         else (time_grid[1] - time_grid[0], space_grid[1] - space_grid[0])
        lam = tau * tau / h / h

        assert time_grid[0] == t[0] and time_grid[-1] == t[-1], "grid and real edge points must be equal."
        assert space_grid[0] == x[0] and space_grid[-1] == x[-1], "grid and real edge points must be equal."

        solution = np.empty((*time_grid.shape, *space_grid.shape), dtype=x.dtype)

        solution[0] = u0(space_grid)
        solution[1] = u0(space_grid) + (t[1]-t[0])*ut0(space_grid)
        solution[:, 0] = ua(time_grid)
        solution[:, -1] = ub(time_grid)

        for i in range(2, len(time_grid)):

            A = self._coef_matrix(i, sigma, lam, solution)
            b = self._ordinate_values(i, sigma, lam, solution)

            solution[i, 1:-1] = np.linalg.solve(A,b)

        return solution


class DiffusionEquationSolver1d:

    def __init__(self, u0, ua, ub, time_step: float = None, space_step: float = None, grid_constr = None):

        self.u0 = u0
        self.ua = ua
        self.ub = ub
        self.tau = time_step
        self.h = space_step

        if grid_constr is not None:
            self.time_grid_constr = grid_constr
            self.space_grid_constr = grid_constr
        elif grid_constr is None and time_step is not None and space_step is not None:
            self.time_grid_constr = self._grid_step_size(time_step)
            self.space_grid_constr = self._grid_step_size(space_step)
        elif grid_constr is None and time_step is None and space_step is None:
            self.time_grid_constr = lambda val: val
            self.space_grid_constr = lambda val: val
        else:
            raise ValueError("step_size and grid_constr are mutually exclusive arguments.")

    @staticmethod
    def _grid_step_size(step_size: float) -> np.ndarray:

        def _grid_constr(val):
            start = val[0]
            end = val[-1]
            niters = int(np.ceil(np.abs(end - start) / step_size + 1))
            return np.linspace(start, end, niters)

        return _grid_constr

    @staticmethod
    def _coef_matrix(i, sigma, lam, u):

        n = u.shape[1] - 2
        A = -sigma*lam * sigma * np.eye(n, k=1) + (1+2*lam*sigma) * np.eye(n)  - lam * sigma * np.eye(n, k=-1)

        return A

    @staticmethod
    def _ordinate_values(i, sigma, lam, u):

        b = (1 - sigma) * lam * u[i-1, 2:]
        b += (1 - 2 * (1 - sigma) * lam) * u[i-1,1:-1]
        b += (1 - sigma) * lam * u[i-1, :-2]

        return b

    def __call__(self, t, x, sigma=1.):

        u0 = self.u0
        ua = self.ua
        ub = self.ub

        time_grid = self.time_grid_constr(t)
        space_grid = self.space_grid_constr(x)

        tau, h = (self.tau, self.h) if self.tau is not None and self.tau is not None \
                         else (time_grid[1] - time_grid[0], space_grid[1] - space_grid[0])
        lam = tau / h / h

        assert tau <= h * h / 2 / (1 - sigma) if sigma < 1 else True, "The scheme diverges, choose other sizes of grid steps."

        assert time_grid[0] == t[0] and time_grid[-1] == t[-1], "grid and real edge points must be equal."
        assert space_grid[0] == x[0] and space_grid[-1] == x[-1], "grid and real edge points must be equal."

        solution = np.empty((*time_grid.shape, *space_grid.shape), dtype=x.dtype)

        solution[0] = u0(space_grid)
        solution[:, 0] = ua(time_grid)
        solution[:, -1] = ub(time_grid)

        for i in range(1, len(time_grid)):

            A = self._coef_matrix(i, sigma, lam, solution)
            b = self._ordinate_values(i, sigma, lam, solution)

            solution[i, 1:-1] = np.linalg.solve(A,b)

        return solution
