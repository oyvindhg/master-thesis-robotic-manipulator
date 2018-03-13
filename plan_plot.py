
import matplotlib.pyplot as plt
from IKPy.src.ikpy import plot_utils


def set_aspect_equal_3d(ax):
    """Fix equal aspect bug for 3D plots."""

    xlim = ax.get_xlim3d()
    ylim = ax.get_ylim3d()
    zlim = ax.get_zlim3d()

    from numpy import mean
    xmean = mean(xlim)
    ymean = mean(ylim)
    zmean = mean(zlim)

    plot_radius = max([abs(lim - mean_)
                       for lims, mean_ in ((xlim, xmean),
                                           (ylim, ymean),
                                           (zlim, zmean))
                       for lim in lims])

    ax.set_xlim3d([xmean - plot_radius, xmean + plot_radius])
    ax.set_ylim3d([ymean - plot_radius, ymean + plot_radius])
    ax.set_zlim3d([zmean - plot_radius, zmean + plot_radius])


def plot_plan(chain, model_rad, target_vector, equal_aspect = False):

    ax = plot_utils.init_3d_figure()
    chain.plot(model_rad, ax, target=target_vector)
    plt.xlim(-40, 40)
    plt.ylim(-40, 40)
    ax.set_zlim(-5, 30)

    if equal_aspect:
        set_aspect_equal_3d(ax)

    plt.show()