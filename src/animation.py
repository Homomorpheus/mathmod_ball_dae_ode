"""
Contains BallAnimation, a helper class to make matplotlib animations
"""


from typing import Literal

import matplotlib.animation
import matplotlib.pyplot as plt
try:
    import ipywidgets as widgets
    from IPython.display import display
except Exception:
    print("import failed in animation.py")

import geometry


class BallAnimation:
    "Helper class to generate matplotlib animation"

    colors = {"ball": "#ffa600",
              "curve": "#003f5c"
             }
    
    def __init__(self, curve: geometry.CurveConstraint, ball: geometry.Ball):
        self._positions = []
        self._velocities = []
        self._modes = []
        self._curve = curve
        self._ball = ball

    def update(self, q, v, mode: Literal["dae", "ode"]):
        "registers position and velocity at a timestep"
        self._positions.append(q[:2])
        self._velocities.append(v[:2])
        self._modes.append(mode)

    def render(self, interval, filename, jupyter_progress_bar=True):
        "render and save to file"
        fig, (ax, axtext) = plt.subplots(figsize=(8, 8), nrows=2, ncols=1, height_ratios=(6, 1))
        
        ax.set_aspect("equal")
        ax.set(xlim=self._curve.xlim, ylim=self._curve.ylim_padded)

        axtext.axis("off")
        
        self._curve.plot(ax, color=self.colors["curve"])
        point, = ax.plot([], [], "o", color=self.colors["ball"])
        text = axtext.text(0, 1, "", transform=axtext.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment="left")

        if jupyter_progress_bar:
            status = [widgets.HTML("-"), widgets.IntProgress(value=0, min=0, max=len(self._positions) - 1, description="")]
            display(widgets.HBox(status))
        

        def feed_to_matplotlib(frame):
            point.set_xdata([self._positions[frame][0]])
            point.set_ydata([self._positions[frame][1]])

            mode = self._modes[frame]

            if jupyter_progress_bar:
                status[0].value = F"<b>frame {frame + 1} of {len(self._positions)}</b>"
                status[1].value = frame

            if mode == "dae":
                # if not self._curve.fulfills_constraint(self._positions[frame]):
                #     q = self._positions[frame]
                #     print(self._curve._expression.evalf(subs={self._curve._x: q[0], self._curve._y: q[1]}), frame)
                text.set_text(F"frame: {frame + 1} \nmode: DAE\n"
                              + "$F_{cf} = " + F"{self._curve.centrifugal_force(self._ball._mass, self._positions[frame], self._velocities[frame]) : .2f}$\n"
                              + "$F_{tot} = " + F"{self._ball.total_physical_normal_force(self._positions[frame], self._velocities[frame]) : .2f}$"
                             )
                
            elif mode == "ode":
                text.set_text(F"frame: {frame + 1} \nmode: ODE\n"
                              + F"pos = {self._positions[frame]}"
                             )
                
            else:
                raise ValueError(F'unknown mode specification "{self._modes[frame]}"')
                
            return [point, text]

        ani = matplotlib.animation.FuncAnimation(fig, feed_to_matplotlib, frames=len(self._positions), interval=interval*1000, blit=True)
        ani.save(filename)
        # https://stackoverflow.com/a/55174144
        # with open(filename, "w") as file:
        #     print(ani.to_jshtml(), file=file)

        plt.close()
