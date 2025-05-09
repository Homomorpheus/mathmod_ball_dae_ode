"""
This file contains DAE/ODE solvers for use throughout the project.
"""


import numpy as np
from scipy.optimize import root
import warnings
import sympy


def generalized_alpha(q0: np.ndarray, v0: np.ndarray, M: np.ndarray, C: np.ndarray, force, steps, t_end, callback=None, rhoinfty=0.8):
    """
    Generalized alpha method.
    For documentation on the algorithm, see:
        https://jschoeberl.github.io/IntroSC/ODEs/mechanical.html#generalized-alpha-method
        https://miaodi.github.io/finite%20element%20method/newmark-generalized/
    Input:
        q0 -- starting position
        v0 -- starting velocity
        M  -- mass matrix
        C  -- damping matrix
        force -- force, a function of q (position)
        steps -- amount of ODE/DAE solver iterations
        t_end -- end time
        callback -- function of step-index and current (q,v,a), gets called every step
        rhoinfty -- stability parameter, see links above
    Output:
        last (q,v,a), step-number calculated
    """
    
    h = t_end/steps
    dim = len(q0)
    #starting value for a
    a0 = np.zeros(dim)

    # accuracy/stability parameters, see links in docstring
    am = (2*rhoinfty - 1)/(rhoinfty + 1)
    af = rhoinfty/(rhoinfty + 1)
    beta = 0.25*(1 - am + af)**2
    gamma = 0.5 - am + af

    # state from before the timestep
    old = np.concatenate([q0, v0, a0]) # not as long as new!

    # implicit solver equations
    # new is qnew, vnew, anew, qmid, vmid; each of length dim
    def eqs(new: np.array):
        qold, vold, aold = np.split(old, len(old)/dim)
        qnew, vnew, anew, qmid, vmid, amid = np.split(new, len(new)/dim)

        eq_eval = np.concatenate([(M@amid.transpose()).transpose() + (C@vmid.transpose()).transpose() - force(qmid, vmid),
                                  qold - qnew + h*vold + h**2*((0.5 - beta)*aold + beta*anew),
                                  vold - vnew + h*((1 - gamma)*aold + gamma*anew),
                                  - qmid + (1 - af)*qnew + af*qold,
                                  - vmid + (1 - af)*vnew + af*vold,
                                  - amid + (1 - am)*anew + am*aold
                                  ])
        return eq_eval
        
    for step in range(1,steps+1):
        # solve the solver's equations
        sol = root(eqs, np.concatenate([old, old]))

        if not sol.success:
            if sol.status == 5:
                warnings.warn(sol.message, RuntimeWarning)
            else:
                callback(step, old, error=True)
                raise RuntimeError(F"fscipy.optimize.root did not converge (message: {sol.message})")
        
        old=sol.x[:3*dim]
        
        if callback != None:
            terminate = callback(step, old, error=False)

        if terminate == True:
            break
            
    return old, step


def newmark(q0: np.ndarray, v0: np.ndarray, M: np.ndarray, C: np.ndarray, force, steps, t_end, callback=None):
    """
    Newmark method.
    For documentation on the algorithm, see:
        https://jschoeberl.github.io/IntroSC/ODEs/mechanical.html#the-newmark-method
        https://miaodi.github.io/finite%20element%20method/newmark-generalized/
    Input:
        q0 -- starting position
        v0 -- starting velocity
        M  -- mass matrix
        C  -- damping matrix
        force -- force, a function of q (position)
        steps -- amount of ODE/DAE solver iterations
        t_end -- end time
        callback -- function of step-index and current (q,v,a), gets called every step
    Output:
        last (q,v,a), step-number calculated
    """
    
    h = t_end/steps
    dim = len(q0)
    #starting value for a
    a0 = np.zeros(dim)

    # state from before the timestep
    old = np.concatenate([q0, v0, a0])

    # implicit solver equations
    # new is qnew, vnew, anew; each of length dim
    def eqs(new: np.array):
        qnew, vnew, anew = np.split(new, len(new)/dim)

        eq_eval = np.concatenate([(M@anew.transpose()).transpose() + (C@vnew.transpose()).transpose() - force(qnew, vnew),
                                  vnew - vold - h/2*(anew + aold),
                                  qnew - qold - h*vold - h**2/4*(anew + aold)
                                  ])
        return eq_eval
        
    for step in range(1,steps+1):
        # solve the solver's equations
        qold, vold, aold = np.split(old, len(old)/dim)
        sol = root(eqs, old)

        if not sol.success:
            if sol.status == 5:
                warnings.warn(sol.message, RuntimeWarning)
            else:
                callback(step, old, error=True)
                raise RuntimeError(F"fscipy.optimize.root did not converge (message: {sol.message})")
        
        old=sol.x
        
        if callback != None:
            terminate = callback(step, old, error=False)

        if terminate == True:
            break
            
    return old, step
