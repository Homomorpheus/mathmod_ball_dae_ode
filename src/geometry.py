"""
This module contains the helper classes CurveConstraint and Ball
for dealing with the algebraic constraint of the 2D DAE
and the mechanics of the ball, respectively.

"""


import functools
from typing import Literal

import sympy
from sympy import *
import numpy as np
import scipy
import matplotlib.patheffects

import solvers


class CurveConstraint:
    "holds an equation for a 2D curve"
    xlim: tuple[float]
    ypadding: float
    
    def __init__(self, equation_expression: sympy.core.expr.Expr, x: sympy.core.symbol.Symbol,
                 y: sympy.core.symbol.Symbol, inside: Literal["positive", "negative"], xlim, ypadding=0.3, tick_length=0.5):
        
        self._expression = equation_expression # sympy curve description expressed in x and y
        self._expression_gradient = [diff(equation_expression, x), diff(equation_expression, y)]
        self._expression_hessian = [[diff(equation_expression, var1, var2) for var1 in (x, y)] for var2 in (x, y)]
        
        self._x = x
        self._y = y
        
        assert inside in ("positive", "negative")
        self._inside = inside
        self.xlim = xlim
        self.ypadding = 0.3
        self.tick_length = tick_length

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
            # mask = np.logical_not(np.isclose(sol_vals.imag, 0))
                
            # self._xvals.append(np.ma.masked_array(xspace, mask))
            # self._yvals.append(np.ma.masked_array(np.real(sol_vals), mask))
            self._xvals.append(xspace[np.isclose(sol_vals.imag, 0)])
            self._yvals.append(np.real(sol_vals)[np.isclose(sol_vals.imag, 0)])

    @property
    @functools.cache
    def ylim(self):
        "returns appropriate ylim for matplotlib axis"
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

    def plot(self, ax, color="black"):
        "plot the curve represented by the class instance"
        for x, y in zip(self._xvals, self._yvals):
            if len(x) == 0:
                continue
                
            median_x = x[int(len(x)/2)]
            median_y = y[int(len(x)/2)]
            midpoint_normal = self.normal_vec(np.array([median_x, median_y]))

            # does outward normal vector look upward or downward? -> set tick angle
            # see https://matplotlib.org/stable/api/patheffects_api.html#matplotlib.patheffects.withTickedStroke
            if midpoint_normal[1] > 0:
                tick_angle = 45.0
            else:
                tick_angle = -45.0
                
            ax.plot(x, y, color=color, path_effects=[matplotlib.patheffects.withTickedStroke(angle=tick_angle, length=self.tick_length)])

    def fulfills_constraint(self, q, atol=1e-1)->np.ndarray:
        error = self._expression.evalf(subs={self._x: q[0], self._y: q[1]})
        return np.isclose(error, 0, atol=atol)

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
        "normal vector of length 1, at point q, looking outside"
        assert self.fulfills_constraint(q)

        # see https://math.stackexchange.com/a/4283563
        grad = self.eval_gradient(q)

        # make it look outward
        if self._inside == "positive":
            grad *= -1
        
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

    def project_to_curve(self, q: np.ndarray)->np.ndarray:
        "for any point q, search the point on the curve that is closest to it"
        projection = scipy.optimize.minimize(lambda x: np.linalg.norm(x - q), q, method="COBYQA",
                                             constraints=[{"type": "eq", "fun": lambdify([(self._x, self._y)], self._expression)}],
                                             options = {"initial_tr_radius": 5}
                                            )
        if not projection.success and projection.maxcv >= 1e-4:
            print(projection)
            # raise RuntimeError(F"projection from {q} to curve unsuccessful")
        return projection.x

    def start_projection(self, q: tuple, v_up: float) -> tuple[np.ndarray]:
        "for any point q, give the closest point on the constraint curve and an 'upward-looking' velocity vector of length v_up"

        # find the nearest point on the curve
        q = np.array(q)

        q_compliant = self.project_to_curve(q)
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
            final_force = np.concatenate([original_force(q, v) + q[2]*self.eval_gradient(q),
                                          np.array([self._expression.evalf(subs={self._x: q[0], self._y: q[1]})], dtype=np.float64)])
            return final_force
        return constraint_force

    def curvature(self, q):
        "curvature at point q"
        assert self.fulfills_constraint(q)

        # (inward) normal and tangent vector of the constraint curve, in q
        normal = -self.normal_vec(q)
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

    def centrifugal_force(self, mass: float, q: np.ndarray, v: np.ndarray)->float:
        """
        evaluates the centrifugal force formula; 
        note that the curvature is the inverse of radius of the circle in that point
        """
        return mass * np.linalg.norm(v[:2])**2 * self.curvature(q)

    def is_inside(self, q)->bool:
        "using the inside argument of __init__, determine if q is inside the (closed) curve"
        constraint_func_eval = self._expression.evalf(subs={self._x: q[0], self._y: q[1]})
        if self._inside == "positive":
            return (constraint_func_eval > 0)
        elif self._inside == "negative":
            return (constraint_func_eval < 0)


class Ball:
    "data storage and helper functions for an idealized ball; this class is time-independent"
    
    def __init__(self, curve: CurveConstraint, mass: float, gravity,
                 curve_friction: float=0.0, normal_cor: float=0.5, tangential_cor: float=1.0, bounce_threshold=0.1, name=""):
        self._curve = curve
        self._mass = mass
        self._curve_friction = curve_friction
        # COR = coefficient of restitution
        self.normal_cor = normal_cor
        self.tangential_cor = tangential_cor
        self.bounce_threshold = bounce_threshold
        self.name = name

        # mass matrix for DAE with generalized alpha
        self.mass_mat_dae = np.array([[mass, 0, 0],
                                      [0, mass, 0],
                                      [0, 0, 0]
                                     ])
        # mass matrix for ODE with generalized alpha
        self.mass_mat_ode = np.array([[mass, 0],
                                      [0, mass]
                                     ])

        # damping matrix for ODE with generalized alpha
        self.damping_mat = np.array([[curve_friction, 0, 0],
                                     [0, curve_friction, 0],
                                     [0, 0, 0]
                                    ])

        self._gravity = gravity
        # see https://jschoeberl.github.io/IntroSC/ODEs/mechanical.html#systems-with-constraints
        self.force = curve.force_to_constraint_force(lambda q, v: mass*gravity(q, v))

    def total_physical_normal_force(self, q: np.ndarray, v: np.ndarray)->float:
        "for position q and velocity v, compute the forces acting on the ball, without those from lagrange parameters"
        normal = self._curve.normal_vec(q) # outward normal vector
    
        normal_force_outward = np.dot(self._gravity(q,v), normal) + self._curve.centrifugal_force(self._mass, q, v)
        return normal_force_outward

    def determine_liftoff(self, q: np.ndarray, v: np.ndarray)->bool:
        "for position q and velocity v, determine whether or not the ball should leave the ground"
        normal_force_outward = self.total_physical_normal_force(q, v)
    
        if normal_force_outward >= 0:
            return False
        else:
            return True

    def ode_data_to_dae_data(self, old: np.ndarray)->tuple[np.ndarray]:
        "handles data storage when ball lands on curve (without rebound)"

        qold = self._curve.project_to_curve(old[0:2])
        vold = old[2:4]

        tangent = self._curve.tangent_vec(qold)
        v_project_tangent = np.dot(vold, tangent) * tangent

        q = np.pad(qold, (0,1), "constant")
        v = np.pad(v_project_tangent, (0,1), "constant")

        return q, v

    def simulate(self, steps: int, t_end: float, q0: tuple, v_up:float, callback):
        "simulates ball movement using DAE+ODE"

        # ensure consistent starting values
        q0, v0 = self._curve.start_projection(q0, v_up)

        step = 0

        def callback_dae(current_step, new, error)->bool:
            "wrapper of callback for the DAE case"
            qnew = new[0:2]
            vnew = new[3:5]

            terminate = callback(current_step + step, qnew, vnew, error, mode="dae")

            if self.determine_liftoff(qnew, vnew):
                return True

            return terminate

        def callback_ode(current_step, new, error)->bool:
            "wrapper of callback for the ODE case"
            qnew = new[0:2]
            vnew = new[2:4]

            terminate = callback(current_step+step, qnew, vnew, error, mode="ode")

            # if the ball hits the wall
            if not self._curve.is_inside(qnew):
                # ensure the position is valid
                qnew[:] = self._curve.project_to_curve(qnew)
                
                normal = self._curve.normal_vec(qnew)
                tangent = self._curve.tangent_vec(qnew)
                # normal velocity **after** bounce
                normal_vel = - self.normal_cor*np.dot(normal, vnew)
                
                if np.abs(normal_vel) <= self.bounce_threshold and not self.determine_liftoff(qnew, np.zeros(2)):
                    return True
                else:
                    vnew[:] = self.tangential_cor*np.dot(vnew, tangent)*tangent + normal_vel*normal

            return terminate

        qold = q0
        vold = v0

        # if we start airborne
        if self.determine_liftoff(qold, vold):
            qold = qold[0:2]
            vold = vold[0:2]

            old, step_out = solvers.newmark(qold, vold, self.mass_mat_ode, np.zeros((2,2)),
                                            lambda q, v: self._mass*self._gravity(q, v), steps-step,
                                            t_end * (steps - step)/steps, callback_ode
                                            )
            qold, vold = self.ode_data_to_dae_data(old)
            step += step_out
        
        while step < steps:
            old, step_out = solvers.newmark(qold, vold, self.mass_mat_dae, self.damping_mat, self.force, steps - step,
                                            t_end * (steps - step)/steps, callback_dae
                                            )
            qold = old[0:2]
            vold = old[3:5]
            step += step_out

            if step >= steps:
                break

            old, step_out = solvers.newmark(qold, vold, self.mass_mat_ode, np.zeros((2,2)),
                                            lambda q, v: self._mass*self._gravity(q, v), steps-step,
                                            t_end * (steps - step)/steps, callback_ode
                                            )
            qold, vold = self.ode_data_to_dae_data(old)
            step += step_out
            