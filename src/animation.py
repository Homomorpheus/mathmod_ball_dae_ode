"""
Contains Animation, a helper class to make matplotlib animations
"""


import matplotlib.animation
import matplotlib.pyplot as plt

from curve_constraint import CurveConstraint


class DotAnimation:
    "Helper class to generate matplotlib animation"
    def __init__(self, curve: CurveConstraint):
        self._positions = []
        self._curve = curve

    def update(self, q):
        "registers position at a timestep"
        self._positions.append(q[:2])

    def render(self, interval, filename):
        "render and save to file"
        px = 1/plt.rcParams['figure.dpi']  # pixel in inches
        fig, ax = plt.subplots(figsize=(600*px, 600*px), frameon=False)
        ax.set_aspect("equal")
        ax.set(xlim=self._curve.xlim, ylim=self._curve.ylim_padded)
        
        self._curve.plot(ax)
        point, = ax.plot([], [], "bo")
        text = ax.text(0.05, 1.1, "", transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox={"boxstyle":'round', "facecolor":"white"})

        def feed_to_matplotlib(frame):
            point.set_xdata([self._positions[frame][0]])
            point.set_ydata([self._positions[frame][1]])
            text.set_text(F"time = {frame*interval:.2f}")
            return [point, text]

        ani = matplotlib.animation.FuncAnimation(fig, feed_to_matplotlib, frames=len(self._positions), interval=interval*1000, blit=True)
        ani.save(filename)

        plt.close()
