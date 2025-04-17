"""
This module contains the helper class CurveConstraint for dealing with the algebraic constraint of the 2D DAE.
"""


import functools

import sympy
from sympy import *
import numpy as np
import scipy


class CurveConstraint:
    "holds an equation for a 2D curve"
    xlim: tuple[float]
    ypadding: float
    
    def __init__(self, equation_expression: sympy.core.expr.Expr, x: sympy.core.symbol.Symbol, y: sympy.core.symbol.Symbol, xlim, ypadding=0.3):
        self._expression = equation_expression # sympy curve description expressed in x and y
        self._expression_gradient = [diff(equation_expression, x), diff(equation_expression, y)]
        self._expression_hessian = [[diff(equation_expression, var1, var2) for var1 in (x, y)] for var2 in (x, y)]
        self._x = x
        self._y = y
        self.xlim = xlim
        self.ypadding = 0.3

        self.generate_plotcurves()

    def generate_plotcurves(self):
        "generates plottable numpy arrays from equation_expression"
        self._solutions = sympy.solve(self._expression, self._y)
        self._solution_lambdas = [lambdify(self._x,s) for s in self._solutions]
        
        xspace = np.linspace(self.xlim[0], self.xlim[1], int(1e4), dtype=np.complex128)

        self._xvals = []
        self._yvals = []

        for sol_lambda in self._solution_lambdas:
            sol_vals = sol_lambda(xspace)
            mask = np.logical_not(np.isclose(sol_vals.imag, 0))
                
            self._xvals.append(np.ma.masked_array(xspace, mask))
            self._yvals.append(np.ma.masked_array(sol_vals.real, mask))

    @property
    @functools.cache
    def ylim(self):
        "returns appropriate ylim for matplotlib"
        ymax = -np.inf
        ymin = np.inf
        
        for yval in self._yvals:
            for y in yval:
                if type(y) == np.ma.core.MaskedConstant:
                    continue
                else:
                    if y >= ymax:
                        ymax = y
                    if y <= ymin:
                        ymin = y

        return (ymin, ymax)

    @property
    def ylim_padded(self):
        "ylim for matplotplotlib such that there is space around the curve"
        ylim = np.array(self.ylim)
        return ylim + np.array([-self.ypadding, self.ypadding])

    def plot(self, ax):
        "plot the curve represented by the class instance"
        for x, y in zip(self._xvals, self._yvals):
            ax.plot(x, y, color="black")

    def fulfills_constraint(self, q)->np.ndarray:
        error = self._expression.evalf(subs={self._x: q[0], self._y: q[1]})
        return np.isclose(error, 0)

    def eval_gradient(self, q)->np.ndarray:
        "evaluate the gradient of the constraint function at a point q"
        gradient = (self._expression_gradient[0].evalf(subs={self._x: q[0], self._y: q[1]}),
                    self._expression_gradient[1].evalf(subs={self._x: q[0], self._y: q[1]}))
        
        return np.array(gradient, dtype=np.float64)

    def eval_hessian(self, q)->np.ndarray:
        "evaluate the hessian matrix of the constraint function at a point q"
        exphess = self._expression_hessian
        hessian = [[exphess[0][0].evalf(subs={self._x: q[0], self._y: q[1]}), exphess[0][1].evalf(subs={self._x: q[0], self._y: q[1]})],
                   [exphess[1][0].evalf(subs={self._x: q[0], self._y: q[1]}), exphess[1][1].evalf(subs={self._x: q[0], self._y: q[1]})]
                  ]
        return np.array(hessian, dtype=np.float64)

    def normal_vec(self, q)->np.ndarray:
        "normal vector of length 1, at point q"
        assert self.fulfills_constraint(q)

        TODO: make consistently look outwards or inwards
        
        grad = self.eval_gradient(q)
        return grad/np.linalg.norm(grad)

    def tangent_vec(self, q)->np.ndarray:
        "tangent vector of length 1, at point q"
        assert self.fulfills_constraint(q)
        
        normal = self.normal_vec(q)
        tangent = np.array([ - normal[1], normal[0]], dtype=np.float64)
        return tangent

    def tangent_velocity(self, q, v_up):
        "for a point q fulfilling the constraint, give a valid velocity vector of length v_up, looking 'upward' if possible"
        assert self.fulfills_constraint(q)
        
        tangent = self.tangent_vec(q)

        # make tangent vector look upward, if possible
        if tangent[1] < 0:
            tangent *= (-1)

        return v_up*tangent

    def start_projection(self, q: tuple, v_up: float) -> tuple[np.ndarray]:
        "for any point q, give the closest point on the constraint curve and an 'upward-looking' velocity vector of length v_up"

        # find the nearest point on the curve
        q = np.array(q)
        projection = scipy.optimize.minimize(lambda x: np.linalg.norm(x - q), q, method="COBYQA",
                                             constraints=[{"type": "eq", "fun": lambdify([(self._x, self._y)], self._expression)}])
        q_compliant = projection.x
        v_compliant = self.tangent_velocity(q_compliant, v_up)

        # add zeros for lagrange parameter
        q_long = np.pad(q_compliant, (0,1), "constant")
        v_long = np.pad(v_compliant, (0,1), "constant")
        return q_long, v_long

    def force_to_constraint_force(self, original_force):
        """
        takes a force original_force (as a function dependent of q) and adds the forces from the constraints,
        see https://jschoeberl.github.io/IntroSC/ODEs/mechanical.html#systems-with-constraints
        """
        def constraint_force(q: np.ndarray, v: np.ndarray)->np.ndarray:
            final_force = np.concatenate([original_force(q) + q[2]*self.eval_gradient(q),
                                          np.array([self._expression.evalf(subs={self._x: q[0], self._y: q[1]})], dtype=np.float64)])
            return final_force
        return constraint_force

    def curvature(self, q):
        "curvature at point q"
        assert self.fulfills_constraint(q)

        # normal and tangent vector of the constraint curve, in q
        normal = self.normal_vec(q)
        tangent = self.tangent_vec(q)

        # gradient and hessian matrix of the constraint function, in q
        gradient = self.eval_gradient(q)
        hessian = self.eval_hessian(q)

        # derivative of constraint function in (tangent, normal)-coordinates; fund. thm. of implicit fcts.
        local_g_diff = - np.dot(gradient, tangent)/np.dot(gradient, normal)

        # second derivate of constraint function in (tangent, normal)-coordinates
        c = (tangent + local_g_diff*normal).transpose() # helper variable
        local_g_diffdiff = - (tangent@hessian@c * np.dot(gradient, normal) - np.dot(gradient, tangent) * normal@hessian@c) / (np.dot(gradient, normal)**2)

        # curvature as per curvature formula
        kappa = local_g_diffdiff / (1 + local_g_diff**2)**(3/2)

        return kappa
