# Calculation of the centrifugal force

The motion of an object on a surface/curve - and therefore its liftoff behavior -
is determined by the forces acting on it, including the centrifugal force
from the surface/curve. Using the centrifugal force and all other forces,
one can determine whether the object is pressed towards or away from the
surface/curve.

Note that the centrifugal force does not have to correspond to the constraint
force $\lambda \nabla G(q)$ {cite}`theophys{page 202}`.

## On a circle

Let $m, q(t)$ and $\omega(t)$ be the mass, position and angular velocity of a particle on a circular curve
around the origin of the reference frame.
Then the centrifugal force acting on the particle is

$$
  \hat{F}_c = m \omega \times (q \times \omega).
$$

{cite}`Demtröder{page 82}` This is the vector form of that force.

This can be simplified using the identity $a \times (b \times c) = b(a \cdot c) - c(a \cdot b)$ {cite}`Demtröder{page 409, Equation 13.9}`:

$$
  \hat{F}_c = m \omega \times (q \times \omega) = m(q (\omega \cdot \omega) - \omega (\underbrace{\omega \cdot q}_{=0})) = m q \| \omega \|^2
$$

This vectorial force is normal to the curve. Since we are only interested in the normal part of the force, we define

$$
  F_c := \| \hat{F}_c \| = m r \| \omega \|^2,
$$

where $r$ is the radius of the circular curve $q$.
In addition, we know that $\dot{q} = \omega \times q$ {cite}`Holm{Equation 2.1.7, Remark 2.1.16}`.
As (without loss of generality)
\begin{align*}
  \omega =
  \begin{pmatrix}
    0 \\
    0 \\
    \omega_3
  \end{pmatrix}
  ~~~~ \text{and} ~~~~
  q =
  \begin{pmatrix}
    q_1 \\
    q_2 \\
    0
  \end{pmatrix},
\end{align*}
we obtain that
\begin{equation*}
  \dot{q} = \omega \times q =
  \begin{pmatrix}
    -\omega_3 q_2 \\
    -\omega_3 q_1 \\
    0
  \end{pmatrix}.
\end{equation*}
As a result, \| \dot{q} \| = |\omega_3| \|q\| = \| \omega \| r and therefore
\begin{equation*}
  F_c = m \frac{ \| \dot{q} \|^2 }{r}
\end{equation*}
follows.

## On general curves

However, this is not applicable when the motion of the particle is not exactly circular;
after all, the formula above is depends on the radius of the circular motion.
This can be mitigated by assuming the motion to be asymptotically circular.

The osculating circle of a curve at a point is the circle that goes through that point
and has the same tangent and curvature $\kappa$ at that point. Its radius is

$$
r = \frac{1}{ | \kappa | }.
$$
{cite}`osc`

This turns the formula for the centrifugal force into
\begin{equation*}
  F_c = m \| \dot{q} \|^2 | \kappa |.
\end{equation*}

### Curvature

Given a parameterization $\varphi$ of a curve in $\mathbb{R}^2$, the curve's curvature at any point $\varphi(t)$ is given by
\begin{equation*}
  \kappa = \frac{\varphi_1'(t) \varphi_2''(t) - \varphi_2'(t) \varphi_1''(t)}{\| \varphi '(t) \|^3}.
\end{equation*}
{cite}`curvature`
The problem is: In the current setting, the curve is not given by a parameterization, but implicitly. (Via the equation $G(q)=0$.)

However, we can perform an affine transformation such that the point in question (any point on the curve) lies in the origin and the
normal and tangent vector at that point are the new basis. (See figure below.) Then the implicit function theorem states that in some neighborhood,
$G(q)=0$ is solved by the graph of a function (which makes for a valid parameterization). {cite}`ana{Satz 6.69}` It also gives us the derivative of that function {cite}`ana{Korollar 6.70}`, and therefore also its second derivative.

<img src="../_static/trafo.svg">

In the case of the curve describing the graph of a function $f$, we have $\varphi(t) = (t, f(t)$). Then the curvature formula simplifies to
\begin{equation*}
  \kappa = \frac{f''(t)}{(1 + f'(t)^2)^{3/2}}.
\end{equation*}
{cite}`curvature`

Take a point $x_0$ on our curve, with inward unit normal vector $\nu$ and a unit tangent vector $t$.
These can be easily calculated:
\begin{align*}
  \nu &= \frac{ \nabla G(x_0) }{ \| \nabla G(x_0) \| } \\
  t &= (-\nu_2, \nu_1)
\end{align*}
{cite}`curv_formul{page 636f}`

Neither translation nor rotation of space change the curvature of a curve.
Therefore (and because $t$ is normal to $\nu$), we can transform our space in the sense of
\begin{equation*}
  (x, y) = \alpha t + \beta \nu + x_0.
\end{equation*}

Let
\begin{equation*}
  T(\alpha, \beta) := \alpha t + \beta \nu + x_0;
\end{equation*}
then we look at $T^{-1}(\varphi)$.
Note that in our new affine space, $T^{-1}(\varphi)$ is defined by the equation $G(T(\alpha, \beta))=0$.

Now, the implicit function theorem gives us a locally defined function $f$ that describes a part of $T^{-1}(\varphi)$.
As $x_0$ lies on the curve, $f(0)=0$ holds.
Also, the implicit function theorem tells us that for small $\alpha$,
```{math}
:label: eq:f_diff
  f'(\alpha) = {\large - \frac{\frac{\partial G \circ T}{\partial \alpha}}{\frac{\partial G \circ T}{\partial \beta}} \Biggr\rvert_{\beta=f(\alpha)} }
             = \frac{\nabla G(\alpha t + \beta \nu + x_0) \cdot t}{\nabla G(\alpha t + \beta \nu + x_0) \cdot \nu} \Biggr\rvert_{\beta=f(\alpha)}
             = \frac{\nabla G(\alpha t + f(\alpha) \nu + x_0) \cdot t}{\nabla G(\alpha t + f(\alpha) \nu + x_0) \cdot \nu}
```
holds. {cite}`ana{Satz 6.69 and Korollar 6.70}`
Inserting $\alpha = 0$ yields
\begin{equation*}
  f'(0) = - \frac{\nabla G(x_0) \cdot t}{\nabla G(x_0) \cdot \nu}
\end{equation*}

However, {eq}`eq:f_diff` can also be used to obtain $f''$:
\begin{align*}
  f''(\alpha) = &- \frac{t^T H_G(\alpha t + f(\alpha) \nu + x_0)(t + f'(\alpha) \nu) \nabla G(\alpha t + f(\alpha) \nu + x_0) \cdot \nu
                        }{(\nabla G(\alpha t + f(\alpha) \nu + x_0) \cdot \nu)^2} \\
                &+ \frac{ \nabla G(\alpha t + f(\alpha) \nu + x_0) \cdot t \nu^T H_G(\alpha t + f(\alpha) \nu + x_0)(t + f'(\alpha) \nu)
                        }{(\nabla G(\alpha t + f(\alpha) \nu + x_0) \cdot \nu)^2}
\end{align*}
Here, $H_G$ denotes the hessian of $G$.

For $\alpha = 0$ and $c := t + f'(0) \nu$, this amounts to
\begin{equation*}
  f''(0) = - \frac{t^T H_G(x_0)c G(x_0) \cdot \nu - G(x_0) \cdot t \nu^T H_G(x_0)c}{(\nabla G(x_0) \cdot \nu)^2}.
\end{equation*}

Now, all building blocks for the computation of the centrifugal force are available.

<!--
order https://www.worldscientific.com/worldscibooks/10.1142/p802#t=aboutBook ??? \
https://www.tuwien.at/tu-wien/organisation/zentrale-bereiche/archiv/universitaetssammlungen/privilegiensammlung -->
