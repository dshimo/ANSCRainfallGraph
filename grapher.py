import matplotlib.pyplot as plt
from models import DischargeRate, GageHeight, Rainfall
from pony import orm
import datetime
import dateutil.parser as dparser
from scipy.interpolate import spline
import numpy as np


def smooth_vals(x, y, days, points_per_day):
    """
    Apply smoothing to the values for a prettier graph
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


def plot_vals(Database, days, color='white', dimensions=(640, 480)):
    """
    Display a plot for the given data
    :param dimensions: dimensions of the image rendered
    :param color: color of the graph
    :param Database: the Database (GageHeight, DischargeRate or Rainfall) to use
    :param days: number of days to plot (up to today)
    :return: nothing
    """
    days_delta = datetime.timedelta(days=days)
    with orm.db_session:
        # Get the datetime of the latest value in the database
        latest = dparser.parse(orm.max(v.time_stamp for v in Database))
        datetime_cutoff = latest - days_delta
        values = orm.select(v for v in Database if v.time_stamp > datetime_cutoff)
        # x axis values to plot (datetime)
        x = []
        # y axis values to plot (value)
        y = []
        for value in values:
            # print(value, end=": ")
            # print(value.value)
            x.append(dparser.parse(value.time_stamp).timestamp())
            y.append(value.value)

        x, y = smooth_vals(x, y, days, 2)
        with plt.rc_context({'axes.edgecolor': color, 'xtick.color': color, 'ytick.color': color}):
            fig, axes = plt.subplots()
            axes.plot(x, y, 'w-')
            axes.set_facecolor((1, 1, 1, 0))

            # Convert the x axis labels to days of the week
            labels = axes.get_xticks().tolist()
            labels = [datetime.datetime.fromtimestamp(date).strftime('%A') for date in labels]
            print(labels)
            axes.set_xticklabels(labels)
            fig.savefig('res/gen/gageheight.png', facecolor=(1, 1, 1, 0), bbox_inches='tight', dpi=120)


plot_vals(GageHeight, 5)