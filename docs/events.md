# Switching states

<img src="../_static/state_flowchart_2.svg">

To the determine whether the ball leaves the surface, causing a switch from the DAE to the ODE, 
or not, the total force acting on the ball in the direction of the surface normal has to be 
examined.

The two important forces to consider are the gravitational force $F_g$ and the centrifugal force 
$F_c$.
To receive the component of gravity in the normal direction we compute the scalar product
\begin{equation*}
  F_g = g \cdot N
\end{equation*}
where $g \in \mathbb{R}^{2}$ denotes the gravitational acceleration and $N \in \mathbb{R}^{2}$ 
the outwards normal vector.

The total outwards normal force is then given by
\begin{equation*}
  F_N = F_g + F_c,
\end{equation*}
and the ball lifts off as soon as $F_N \lt 0$, meaning the force pressing the ball towards the 
curve is smaller than the one pushing it away.

As soon as this happens we stop the Newmark solver for the DAE and turn to the ODE-setup to start 
solving for the flying phase.