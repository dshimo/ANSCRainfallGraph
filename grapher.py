import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from models import DischargeRate, GageHeight, Rainfall, TotalRainfall
from pony import orm
import datetime
import dateutil.parser as dparser
from scipy.interpolate import spline
import numpy as np
import threading

grapher_lock = threading.Lock()


EDGE_COLOR = "#FCE694"
RAINFALL_COLOR = "#C1DBE3"
GRAPH_COLOR = "#F6FEAA"
X_TICK_COLOR = "#FCE694"


def cumulative(x):
    for index in range(len(x)):
        if index != 0:
            x[index] += x[index-1]


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


def get_vals(Database, days):
    days_delta = datetime.timedelta(days=days)
    with orm.db_session:
        # Get the datetime of the latest value in the database
        latest = orm.max(v.time_stamp for v in Database)
        if not isinstance(latest, datetime.datetime):
            latest = dparser.parse(latest)
        datetime_cutoff = latest - days_delta
        values = orm.select(v for v in Database if v.time_stamp > datetime_cutoff)
        # x axis values to plot (datetime)
        x = []
        # y axis values to plot (value)
        y = []
        for value in values:
            cur_time_stamp = value.time_stamp
            # print(value, end=": ")
            # print(value.value)
            # same bug as above
            if not isinstance(cur_time_stamp, datetime.datetime):
                cur_time_stamp = dparser.parse(cur_time_stamp)
            x.append(cur_time_stamp.timestamp())
            y.append(value.value)
    return x, y


def store_rainfall(days, value):
    with orm.db_session:
        date = datetime.datetime.now()
        TotalRainfall(days=days, value=value, time_stamp=date)


def plot_vals(Database, days):
    """
    Display a plot for the given data
    :param Database: the Database (GageHeight, DischargeRate or Rainfall) to use
    :param days: number of days to plot (up to today)
    :return: nothing
    """
    x, y = get_vals(Database, days)
    rain_x, rain_y = get_vals(Rainfall, days)
    cumulative(rain_y)
    store_rainfall(days, rain_y[-1])
    x, y = smooth_vals(x, y, days, 12)
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
            y_label = 'Depth (ft)'
        axes.set_ylabel(y_label, color=GRAPH_COLOR, fontproperties=label_font)
        axes.tick_params('y', colors=GRAPH_COLOR)
        for label in (axes.get_xticklabels() + axes.get_yticklabels()):
            label.set_fontproperties(tick_font)

        # Plot the rainfall
        rain_axes = axes.twinx()
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
