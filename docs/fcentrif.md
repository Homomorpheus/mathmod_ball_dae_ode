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

This can be simplified using the identity $a \times (b \times c) = b(a \cdot c) - c(a \cdot b)$:

$$
  \hat{F}_c = m \omega \times (q \times \omega) = m(q (\omega \cdot \omega) - \omega (\underbrace{\omega \cdot q}_{=0})) = m q \| \omega \|^2
$$

This vectorial force is normal to the curve. Since we are only interested in the normal part of the force, we define

$$
  F_c := \| \hat{F}_c \| = m r \| \omega \|^2,
$$

where $r$ is the radius of the circular curve $q$.
In addition, we know that $\dot{q} = \omega \times q$ {cite}`Holm{Equation 2.1.7, Remark 2.1.16}`.
Since only the


## On general curves

### Curvature

https://mathworld.wolfram.com/Curvature.html
https://mathworld.wolfram.com/OsculatingCircle.html
https://math.libretexts.org/Courses/Monroe_Community_College/MTH_212_Calculus_III/Chapter_12%3A_Vector-valued_Functions/12.4%3A_Arc_Length_and_Curvature
order https://www.worldscientific.com/worldscibooks/10.1142/p802#t=aboutBook ???

https://www.tuwien.at/tu-wien/organisation/zentrale-bereiche/archiv/universitaetssammlungen/privilegiensammlung

## Curvature
