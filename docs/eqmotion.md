# Equations of motion for constrained mechanical systems

## From the principle of least action

Let $q(t) \in \mathbb{R}^2$ be the position of a mass point (ball) with mass $m$ and Lagrangian function $L$.
Assume that the mass point is subjected to a force $F$ and a constraint $G(q) \in C^2(\mathbb{R}^2, \mathbb{R})$ with Lagrange parameter $\lambda$.
Then the action of the object is given by
\begin{equation*}
  \tilde{S} = \int_0^T L(q, \dot{q}) + \lambda G(q) \ dt,
\end{equation*}
for $q(0), q(T)$ fixed. {cite}`leastaction{Equation 4}`
The stationary condition $0 = \delta \tilde{S}$ under $\delta q(0) = \delta q(T) = 0$ yields
\begin{align*}
  0 = \delta \tilde{S}
  & = \frac{\partial}{\partial \varepsilon } \int_0^T L(q + \varepsilon \delta q, \dot{q} + \varepsilon \dot{\delta q})
            + \lambda \cdot G(q + \varepsilon \delta q) \ dt \Biggr\rvert_{\varepsilon = 0} \\
  & = \int_0^T \frac{\partial L}{\partial q} (q, \dot{q}) \cdot \delta q + \frac{\partial L}{\partial \dot{q}} (q, \dot{q}) \cdot \delta \dot{q}
            + \lambda \cdot G(q) \cdot \delta q \ dt \\
  & = \frac{\partial L}{\partial \dot{q}} (q, \dot{q}) \cdot \delta q \Biggr\rvert_{t=0}^{t=T}
            + \int_0^T \left( \frac{\partial L}{\partial q} (q, \dot{q}) - \frac{\partial}{\partial t} \frac{\partial L}{\partial \dot{q}} (q, \dot{q})
            + \lambda \cdot G(q) \right) \cdot \delta q \ dt
\end{align*}
and
\begin{equation*}
  0 = G(q).
\end{equation*}

The resulting DAE is
```{math}
:label: eq:EL

  \frac{\partial L}{\partial q} (q, \dot{q}) - \frac{\partial}{\partial t} \frac{\partial L}{\partial \dot{q}} (q, \dot{q})
              + \lambda \cdot G(q) &= 0 \\
  G(q) &= 0.
```

For a mass point, we know that
\begin{align*}
  T(\dot{q}) &= \frac{1}{2} \dot{q} \cdot m \dot{q} ~~~~ \text{(kinetic energy)} \\
  \nabla U(q) &= F ~~~~ \text{(potential energy)} \\
  L &= T(\dot{q}) - U(q).
\end{align*}
{cite}`theophys{page 178}`

Thus, {eq}`eq:EL` reduces to
\begin{align*}
  F - m \ddot{q} + \lambda \cdot G(q) &= 0 \\
  G(q) &= 0.
\end{align*}

If we now define the mass matrix
\begin{equation*}
  M :=
  \begin{pmatrix}
    m & 0 \\
    0 & m
  \end{pmatrix},
\end{equation*}
the motion of our ball is described by
```{math}
:label: eq:motion

  M \ddot{q} &= F + \lambda \nabla G(q)\\
  0 &= G(q).
```

In our case, we will mainly subject it to the gravitational force
\begin{equation*}
  mg
\end{equation*}
where $g \in \mathbb{R}^2$ denotes a constant directional acceleration that serves to simulate gravity.
Throughout the project, other forces have also been added to this.

If we now define

```{math}
:label: eq:dae_eq
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
```


Equation [](eq:motion) turns into
\begin{equation*}
\tilde{M} \begin{pmatrix} \ddot{q} \\ \ddot{\lambda} \end{pmatrix} = \tilde{F}.
\end{equation*}
