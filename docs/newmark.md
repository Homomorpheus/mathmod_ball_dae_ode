# The Newmark time stepper

This project uses the Newmark solver for both DAEs and ODEs.
In general we start out with an equation
\begin{equation*}
  F = M \ddot{x} + C \dot{x} + Kx
\end{equation*}
where $x(t) \in \mathbb{R}^{m}$ is the (generalized) position vector and $M, C, K \in \mathbb{R}^{m \times m}$
denote mass, damping and stiffness matrix.

Now let $x_n, v_n := \dot{x}_n, a_n := \ddot{x}_n$ be position, velocity, and acceleration at
timestep $t_n$. To approximate their values at $t_{n+1} := t_n + h$ the Newmark-$\beta$ method
gives us the following equations:

\begin{align*}
  F_{n+1} &= M a_{n+1} + C v_{n+1} + K q_{n+1}\\
  v_{n+1} &= v_{n} + h\left({\left(1 - \gamma\right) a_{n} + \gamma{a_{n+1}}}\right)\\
  x_{n+1} &= x_{n} + h v_{n} + \frac{h^2}{2} \left({\left(1 - 2\beta\right) a_{n} + 2\beta a_{n+1}}\right)
\end{align*}
{cite}`newmark_analysis{page 2}`

<!-- This family of solvers is non-canonically symplectic and preserves a non-standard momentum. {cite}`newmark_sympl{page 3}` -->
We will use the specific case $\beta = \frac{1}{4}, \gamma = \frac{1}{2}$.
In this case, the solver has quadratic accuracy. {cite}`newmark_analysis{page 2}`
$K$ is not required for the project, we choose $K = \mathbf{0} \in \mathbb{R}^{m \times m}$.

We end up with
\begin{align*}
  F(x_{n+1}) &= M a_{n+1} + C v_{n+1}\\
  v_{n+1} &= v_n + \frac{h}{2} (a_n + a_{n+1})\\
  x_{n+1} &= x_n + h v_n + \frac{h^2}{4} (a_n + a_{n+1}).
\end{align*}

## Setup for the ODE
Let us first consider the flying phase, meaning the current position of the ball is not on the
curve and we need to solve an ODE.
Here we set $C = \mathbf{0} \in \mathbb{R}^{2 \times 2}$, as well as
\begin{equation*}
M =
\begin{pmatrix}
    m & 0 \\
    0 & m
  \end{pmatrix}
  ~~~\text{ and }~~~
  F = mg
\end{equation*}
for mass $m \in \mathbb{R}$ and gravitational acceleration $g \in \mathbb{R}^{2}$.

As initial values $x_0, v_0$ and $a_0$ the algorithm simply receives the current position,
velocity and acceleration of the ball.

## Setup for the DAE
On the other hand, if the ball is currently in the rolling phase, we are dealing with a
constrained system and need to solve a DAE.
In this case we set $M = \tilde{M}$ and $F = \tilde{F}$ as defined in [](eq:dae_eq). If we want
to add a velocity-dependent damping factor $c \in \mathbb{R}$, we define a damping matrix
\begin{equation*}
  C :=
  \begin{pmatrix}
    c & 0 & 0\\
    0 & c & 0\\
	0 & 0 & 0
  \end{pmatrix},
\end{equation*}
otherwise we set $C = \mathbf{0} \in \mathbb{R}^{3 \times 3}$.

Here the initial values are going to be a bit more complicated.
First, we devide the vector $x_n$ into
\begin{equation*}
  x_n =
  \begin{pmatrix}
  q_n\\
  \lambda_n
  \end{pmatrix}
\end{equation*}
where $q_n \in \mathbb{R}^{2}$ and $\lambda_n \in \mathbb{R}$.
The value for $q_0$ will be the current position of the ball on the curve.

If we now split our Newmark equations in the same mannner, we get:

```{math}
:label: eq:dae_sys
  mg + \lambda_{n+1} \nabla G(q_{n+1})
  &=
  \begin{pmatrix}
    m & 0 \\
    0 & m
  \end{pmatrix}
  \ddot{q}_{n+1}
  +
  \begin{pmatrix}
    c & 0 \\
    0 & c
  \end{pmatrix}
  \dot{q}_{n+1}\\
  G(q) &= 0\\
```
\begin{align*}
  \dot{q}_{n+1} &= \dot{q}_n + \frac{h}{2} (\ddot{q}_n + \ddot{q}_{n+1})\\
  \dot{\lambda}_{n+1} &= \dot{\lambda}_n + \frac{h}{2} (\ddot{\lambda}_n + \ddot{\lambda}_{n+1})\\
  \\
  q_{n+1} &= q_n + h \dot{q}_n + \frac{h^2}{4} (\ddot{q}_n + \ddot{q}_{n+1})\\
  \lambda_{n+1} &= \lambda_n + h \dot{\lambda}_n + \frac{h^2}{4} (\ddot{\lambda}_n + \ddot{\lambda}_{n+1})
\end{align*}

The Lagrange parameter $\lambda_n$ enforces the constraint $G(q_n)=0$ but is not needed to
determine $q_{n+1}$ or $\dot{q}_{n+1}$.
The value $\lambda_{n+1}$ is solved implicitly as part of the DAE system [](eq:dae_sys)
and therefore $\lambda$ does not require an initial value to compute. Since that also implies that initial
values for $\dot{\lambda}$ and $\ddot{\lambda}$ are not required, we will ignore those in the
consideration of initial velocity and acceleration.

For the initial velocity we take a look at our constraint $G$. We know that
\begin{equation*}
  G(q) = 0.
\end{equation*}
Differentiation on both sides leads to
\begin{equation*}
  \nabla G(q)v = 0
\end{equation*}
and since $\nabla G(q)$ is the  normal vector, that means that $v$ has to be tangential.
{cite}`curv_formul{page 636f}`
We simply project the current velocity of the ball to the tangent vector and use the result
as the initial value $v_0$.

Lastly, to determine the starting acceleration, we use the following formula for the acceleration
along a curve:
```{math}
:label: eq:accel_start

  \mathbf{\tilde{a}} = a \tau + \kappa v^2 \nu,
```

where $a$ and $v$ are tangential acceleration and velocity, $\tau$ and $\nu$ are tangent and normal
vector and $\kappa$ is the curvature of the curve, and set $a_0 = \tilde{a}$.
{cite}`acceleration`
