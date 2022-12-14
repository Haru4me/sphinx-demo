# Quick Start

This page will contain examples with frequent cases of using our library.

## Some pics

### Pic №1

![waves](imgs/waves.gif "waves plot")

### Pic №2

![diffusion](imgs/diffusion.gif "diffusion plot")

## Some code

### First

`poetry add --dev matplotlib`

### Second 

`solver = DiffusionEquationSolver1d()`

### Third

```python

def wave1d(t, x, u0, ut0, ua, ub):

    lam = ((t[1]-t[0])/(x[1]-x[0]))**2

    u = np.empty((*t.shape, *x.shape))

    u[0] = u0(x)
    u[1] = u0(x) + (t[1]-t[0])*ut0(x)
    u[:, 0] = ua(t)
    u[:, -1] = ub(t)
        
    for i in range(2, len(t)):
        n = u.shape[1] - 2
        A = -lam * np.eye(n, k=1) + (1+lam) * np.eye(n)
        b = 2 * u[i-1, 1:-1] - (1 + lam) * u[i-2, 1:-1] + lam * u[i-2, :-2]
        u[i, 1:-1] = np.linalg.solve(A,b)
        
    return u
```
