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
As a result, $\| \dot{q} \| = |\omega_3| \|q\| = \| \omega \| r$ and therefore
\begin{equation*}
  F_c = m \frac{ \| \dot{q} \|^2 }{r}
\end{equation*}
follows.

## On general curves

However, this is not applicable when the motion of the particle is not exactly circular;
after all, the formula above depends on the radius of the circular motion.
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


<!--
order https://www.worldscientific.com/worldscibooks/10.1142/p802#t=aboutBook ??? \
https://www.tuwien.at/tu-wien/organisation/zentrale-bereiche/archiv/universitaetssammlungen/privilegiensammlung -->
