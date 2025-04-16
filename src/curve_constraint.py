"""
This module contains the helper class CurveConstraint for dealing with the algebraic constraint of the 2D DAE.
"""


import sympy
from sympy import *
import numpy as np
import scipy


class CurveConstraint:
    "holds an equation for a 2D curve"
    
    def __init__(self, equation_expression: sympy.core.expr.Expr, x: sympy.core.symbol.Symbol, y: sympy.core.symbol.Symbol, xlim=(-1.5,1.5)):
        self._expression = equation_expression # sympy curve description expressed in x and y
        self._expression_deriv = [diff(equation_expression, x), diff(equation_expression, y)]
        self._x = x
        self._y = y
        self._xlim = xlim

        self.generate_plotcurves()

    def generate_plotcurves(self):
        "generates plottable numpy arrays from equation_expression"
        self._solutions = sympy.solve(self._expression, self._y)
        self._solution_lambdas = [lambdify(self._x,s) for s in self._solutions]
        
        xspace = np.linspace(self._xlim[0], self._xlim[1], int(1e4), dtype=np.complex128)

        self._xvals = []
        self._yvals = []

        for sol_lambda in self._solution_lambdas:
            sol_vals = sol_lambda(xspace)
            mask = np.logical_not(np.isclose(sol_vals.imag, 0))
            self._xvals.append(np.ma.masked_array(xspace, mask))
            self._yvals.append(np.ma.masked_array(sol_vals, mask))

    def plot(self, ax):
        "plot the curve represented by the class instance"
        for x, y in zip(self._xvals, self._yvals):
            ax.plot(x, y, color="black")

    def eval_gradient(self, q)->np.ndarray:
        "evaluate the gradient of the constraint function at a point q"
        gradient = (self._expression_deriv[0].evalf(subs={self._x: q[0], self._y: q[1]}),
                    self._expression_deriv[1].evalf(subs={self._x: q[0], self._y: q[1]}))
        return np.array(gradient, dtype=np.float64)

    def tangent_velocity(self, q, v_up):
        "for a point q fulfilling the constraint, give a valid velocity vector of length v_up, looking 'upward' if possible"
        # derive normal vector to manifold defined by constraint
        normal_vec = self.eval_gradient(q)

        # calculate normalized tangent vector from normal vector
        tangent_vec = np.array([ - normal_vec[1], normal_vec[0]], dtype=np.float64)
        tangent_vec /= np.linalg.norm(tangent_vec)

        # make tangent vector look upward, if possible
        if tangent_vec[1] < 0:
            tangent_vec *= (-1)

        return v_up*tangent_vec

    def start_projection(self, q: tuple, v_up: float) -> tuple[np.ndarray]:
        "for any point q, give the closest point on the constraint curve and an 'upward-looking' velocity vector of length v_up"

        # find the nearest point on the curve
        q = np.array(q)
        projection = scipy.optimize.minimize(lambda x: np.linalg.norm(x - q), q, method="COBYQA",
                                             constraints=[{"type": "eq", "fun": lambdify([(self._x, self._y)], self._expression)}])
        q_compliant = projection.x
        v_compliant = self.tangent_velocity(q, v_up)

        # add zeros for lagrange parameter
        q_long = np.pad(q_compliant, (0,1), "constant")
        v_long = np.pad(v_compliant, (0,1), "constant")
        return q_long, v_long

    def force_to_constraint_force(self, original_force):
        "takes a force original_force (as a function dependent of q) and adds the forces from the constraints"
        def constraint_force(q: np.ndarray)->np.ndarray:
            final_force = np.concatenate([original_force(q) + q[2]*self.eval_gradient(q),
                                          np.array([self._expression.evalf(subs={self._x: q[0], self._y: q[1]})], dtype=np.float64)])
            return final_force
        return constraint_force
