# Equations of motion for constrained mechanical systems

Let $q(t) \in \mathbb{R}^2$ be the position of a mass point (ball) with mass $m$.
Assume that the mass point is subjected to a force $F$ and a constraint $G(q)$ with Lagrange parameter $\lambda$.
If we now define the mass matrix
\begin{equation*}
  M :=
  \begin{pmatrix}
    m & 0 \\
    0 & m
  \end{pmatrix},
\end{equation*}
its motion is described by
```{math}
:label: eq:motion

  M \ddot{q} &= F + \lambda \nabla G(q)\\
  0 &= G(q).
```
{cite}`theophys{page 171, Equation 5.28}`
In this case, the set of destination of $G$ is $\mathbb{R}$.

In our case, we will mainly subject it to the gravitational force
\begin{equation*}
  F_g = mg
\end{equation*}
where $g \in \mathbb{R}^2$ denotes a constant directional acceleration that serves to simulate gravity.
Throughout the project, other forces have also been added to this.

If we now define
\begin{equation*}
  \tilde{M} :=
  \begin{pmatrix}
    m & 0 & 0 \\
    0 & m & 0 \\
    0 & 0 & 0
  \end{pmatrix}
  ~~~\text{ and }~~~
  \tilde{F} :=
  \begin{pmatrix}
    F + \lambda \nabla G(q)\\
    G(q)
  \end{pmatrix},
\end{equation*}

Equation [](eq:motion) turns into
\begin{equation*}
\tilde{M} \begin{pmatrix} \ddot{q} \\ \ddot{\lambda} \end{pmatrix} = \tilde{F}.
\end{equation*}
