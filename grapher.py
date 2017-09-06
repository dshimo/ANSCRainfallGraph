import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from models import DischargeRate, GageHeight
from getvals import get_vals, get_cumulative_rainfall_vals
import datetime
from scipy.interpolate import spline
import numpy as np
import threading

grapher_lock = threading.Lock()


EDGE_COLOR = "#FCE694"
RAINFALL_COLOR = "#C1DBE3"
GRAPH_COLOR = "#F6FEAA"
X_TICK_COLOR = "#FCE694"


def smooth_vals(x, y, days, points_per_day):
    """
    Apply smoothing to the values for a prettier graph
    :param days: number of days we're plotting
    :param points_per_day: number of points we want per day 
    :param x: x axis values (datetime)
    :param y: y axis values
    :return: smoothed x and y
    """
    x = np.array(x)
    y = np.array(y)
    # Figure out how many values we want on the graph, based on how many days we're plotting
    points = points_per_day * days
    # Create interpolated values of x
    interpolated_x = np.linspace(x.min(), x.max(), points)
    # Smooth y values
    smoothed_y = spline(x, y, interpolated_x)
    # Convert from epoch time back to datetime
    # interpolated_x = [datetime.datetime.fromtimestamp(date) for date in interpolated_x]
    return interpolated_x, smoothed_y


def plot_vals(Database, days):
    """
    Display a plot for the given data
    :param Database: the Database (GageHeight, DischargeRate or Rainfall) to use
    :param days: number of days to plot (up to today)
    :return: nothing
    """
    x, y = get_vals(Database, days)
    rain_x, rain_y = get_cumulative_rainfall_vals(days)
    x, y = smooth_vals(x, y, days, 3)
    label_font = font_manager.FontProperties(fname='./fonts/Oswald-Bold.ttf', size=18)
    tick_font = font_manager.FontProperties(fname='./fonts/Oswald-Regular.ttf', size=12)
    with plt.rc_context({'axes.edgecolor': EDGE_COLOR, 'xtick.color': X_TICK_COLOR}):
        fig, axes = plt.subplots()
        line = axes.plot(x, y, 'w-')
        axes.set_facecolor((1, 1, 1, 0))
        # Set line width
        plt.setp(line, linewidth=5, color=GRAPH_COLOR)
        if Database == DischargeRate:
            y_label = 'Flow Speed (gallons/s)'
        else:
            y_label = 'Gage Height (ft)'
        axes.set_ylabel(y_label, color=GRAPH_COLOR, fontproperties=label_font)
        axes.tick_params('y', colors=GRAPH_COLOR)
        for label in (axes.get_xticklabels() + axes.get_yticklabels()):
            label.set_fontproperties(tick_font)

        # Plot the rainfall
        rain_axes = axes.twinx()
        rain_axes.set_xmargin(0)
        rain_line = rain_axes.plot(rain_x, rain_y)
        plt.setp(rain_line, linewidth=5, color=RAINFALL_COLOR)
        rain_axes.set_ylabel('Total Rainfall (inches)', color=RAINFALL_COLOR, fontproperties=label_font)
        rain_axes.tick_params('y', colors=RAINFALL_COLOR)
        for label in rain_axes.get_yticklabels():
            label.set_fontproperties(tick_font)

        # Convert the x axis labels to days of the week
        labels = axes.get_xticks().tolist()
        labels = [datetime.datetime.fromtimestamp(date) for date in labels]
        labels = [date.strftime('%a\n(%m/%d)') for date in labels]
        axes.set_xticklabels(labels)
        with grapher_lock:
            fig.savefig('./gen/' + Database.__name__ + '.png', facecolor=(1, 1, 1, 0), bbox_inches='tight', dpi=230)


if __name__ == "__main__":
    plot_vals(GageHeight, 10)
    plot_vals(DischargeRate, 10)
