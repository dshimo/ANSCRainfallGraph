from pony import orm
from models import Rainfall
import datetime
import dateutil.parser as dparser


def cumulative(x):
    for index in range(len(x)):
        if index != 0:
            x[index] += x[index-1]


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


def get_cumulative_rainfall_vals(days):
    rain_x, rain_y = get_vals(Rainfall, days)
    cumulative(rain_y)
    return rain_x, rain_y


def get_total_rainfall(days):
    return get_cumulative_rainfall_vals(days)[1][-1]
