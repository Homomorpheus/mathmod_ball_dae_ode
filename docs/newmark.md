# The Newmark time stepper

This project uses the Newmark solver for both DAEs and ODEs.
In both cases we start out with an equation
\begin{equation*}
  F = M \ddot{x}.
\end{equation*}

If we now introduce a velocity-dependent damping factor $c$ and define a damping matrix
\begin{equation*}
  C :=
  \begin{pmatrix}
    c & 0 & 0\\
    0 & c & 0\\
	0 & 0 & 0
  \end{pmatrix}
\end{equation*}
we get
\begin{equation*}
  F = M \ddot{x} + C \dot{x}.
\end{equation*}

Now let $x_n, v_n := \dot{x}_n, a_n := \ddot{x}_n$ be position, velocity, and acceleration at
timestep $t_n$. To approximate their values at $t_{n+1} := t_n + h$ the Newmark-$\beta$ method
(where $\beta = \frac{1}{4}, \gamma = \frac{1}{2}$) gives us the following equations:
\begin{align*}
  F(x_{n+1}) &= M a_{n+1} + C v_{n+1}\\
  v_{n+1} &= v_n + \frac{h}{2} (a_n + a_{n+1})\\
  x_{n+1} &= x_n + h v_n + \frac{h^2}{4} (a_n + a_{n+1}).
\end{align*}

{cite}`miau`
