"""
Contains BallAnimation, a helper class to make matplotlib animations
"""


from typing import Literal

import matplotlib.animation
import matplotlib.pyplot as plt
import numpy as np
try:
    import ipywidgets as widgets
    from IPython.display import display
except Exception:
    print("import failed in animation.py")

import geometry


class BallAnimation:
    "Helper class to generate matplotlib animation"

    # https://coolors.co/palette/001219-005f73-0a9396-94d2bd-e9d8a6-ee9b00-ca6702-bb3e03-ae2012-9b2226
    colors = {"ball": ['#CA6702', '#0A9396', '#E9D8A6', '#9B2226', '#BB3E03', '#94D2BD', '#005F73', '#EE9B00', '#AE2012'],
              "curve": "#001219"
             }
    
    def __init__(self, curve: geometry.CurveConstraint, balls: list[geometry.Ball], length: int):
        self._positions = np.zeros((length, len(balls), 2)) # [frame, ball, space-component]
        self._velocities = np.zeros((length, len(balls), 2))
        self._modes = np.empty((length, len(balls)), dtype=np.dtypes.StringDType()) # [frame, ball]
        self._curve = curve
        self._balls = balls
        self._length = length
        self._amount_balls = len(balls)

        # check if there are enough colors
        if self._amount_balls > len(self.colors["ball"]):
            raise ValueError('please specify more colors (set array BallAnimation.colors["ball"] = ...)')

    def update(self, q, v, ball_index: int, frame, mode: Literal["dae", "ode"]):
        "registers position and velocity at a timestep"
        self._positions[frame, ball_index, : ] = q[:2]
        self._velocities[frame, ball_index, : ] = v[:2]
        self._modes[frame, ball_index] = mode

    def render(self, interval, filename=None, show_trace=False, trace_alpha=0.5, jupyter_progress_bar=True):
        "render and save to file"
        fig, (ax, axtext) = plt.subplots(nrows=1, ncols=2, width_ratios=(7, 1)) #figsize=(8, 8), 
        fig.set_figwidth(8)
        
        ax.set_aspect("equal")
        ax.set(xlim=self._curve.xlim, ylim=self._curve.ylim_padded)

        axtext.axis("off")

        # initialize empty plot elements
        self._curve.plot(ax, color=self.colors["curve"])
        points = [ax.plot([], [], "o", color=self.colors["ball"][i])[0] for i in range(self._amount_balls)]
        framenum_text = ax.text(0, 1.05, "frame 1", transform=ax.transAxes, fontsize=12,
                                    verticalalignment="bottom", horizontalalignment="left"
                                   )
        texts = [axtext.text(0, 0.9 - i/self._amount_balls, "", transform=axtext.transAxes, fontsize=11,
                             verticalalignment='top', horizontalalignment="left",
                             bbox={"boxstyle": "round", "edgecolor": self.colors["ball"][i], "facecolor": "white", "pad": 0.5}
                            ) for i in range(self._amount_balls)]

        if show_trace:
            traces = [ax.plot([], [], color=self.colors["ball"][i], alpha=trace_alpha)[0] for i in range(self._amount_balls)]

        # initialize progress bar within notebook
        if jupyter_progress_bar:
            status = widgets.HTML("-")
            display(status)
        

        def feed_to_matplotlib(frame):
            "callback for matplotlib"

            # update progress bar within notebook
            if jupyter_progress_bar:
                    status.value = F'<b>frame {frame + 1} of {self._length}</b> <progress value="{frame + 1}" max="{self._length}"></progress>'

            framenum_text.set_text(F"frame {frame + 1}")

            # for every ball
            for i, (ball, point, text) in enumerate(zip(self._balls, points, texts)):
                point.set_xdata([self._positions[frame, i, 0]])
                point.set_ydata([self._positions[frame, i, 1]])

                if show_trace:
                    traces[i].set_xdata([self._positions[:frame, i, 0]])
                    traces[i].set_ydata([self._positions[:frame, i, 1]])

                mode = self._modes[frame, i]
    
                if mode == "dae":
                    text.set_text((ball.name + "\n" if ball.name != "" else "")
                                  + F"mode: DAE\n"
                                  + "$F_{cf} = " + F"{self._curve.centrifugal_force(ball._mass, self._positions[frame, i, : ], self._velocities[frame, i, : ]) : .2f}$\n"
                                  + "$F_{tot} = " + F"{ball.total_physical_normal_force(self._positions[frame, i, :], self._velocities[frame, i, : ]) : .2f}$"
                                 )
                    
                elif mode == "ode":
                    text.set_text((ball.name + "\n" if ball.name != "" else "")
                                  + F"mode: ODE\n"
                                  + r"pos = $\binom{" + F"{self._positions[frame, i, 0] : .2f}" + "}{" + F"{self._positions[frame, i, 1] : .2f}" + "}$"
                                 )
                    
                else:
                    raise ValueError(F'unknown mode specification "{mode}"')
                
            return points + [framenum_text] + texts

        self.ani = matplotlib.animation.FuncAnimation(fig, feed_to_matplotlib, frames=len(self._positions), interval=interval*1000, blit=True)

        if filename == None:
            ani_str = self.ani.to_html5_video(1e5)
            
            plt.close()
            return ani_str
        else:
            self.ani.save(filename)        

        plt.close()
