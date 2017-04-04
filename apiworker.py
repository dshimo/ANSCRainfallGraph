import requests
import dateutil.parser
import datetime
from models import DischargeRate, GageHeight, Rainfall
from pony import orm

# Parameter codes
DISCHARGE = '00060'
GAGE_HEIGHT = '00065'
RAINFALL = 'RAIN'


def get_values(period, site, *params):
    """
    Get values from the USGS API and WUNDERGROUND. Returns {'paramcode': [(dateTime, value),],}
    :int period: period for data in days
    :str site: site code
    :list params: list of param codes
    """
    url = 'https://waterservices.usgs.gov/nwis/iv/?format=json'
    url += '&sites=' + site
    url += '&period=P' + str(period) + 'D'
    url += '&parameterCd='
    for param in params:
        url += param + ","
    url = url[:-1] + '&siteStatus=all'
    response = requests.get(url)

    result = {}
    if response.status_code != 200:
        # TODO: handle errors better
        return result
    time_series = response.json()["value"]["timeSeries"]
    for x in range(len(time_series)):
        cur_param = time_series[x]["variable"]['variableCode'][0]['value']
        cur_values = []
        for value in time_series[x]["values"][0]["value"]:
            cur_date = dateutil.parser.parse(value["dateTime"])
            cur_value = value["value"]
            cur_values.append((cur_date, cur_value))
        result[cur_param] = cur_values
    url = "http://api.wunderground.com/api/"
    url += open('WUNDERGROUNDAPIKEY').readline().strip()
    url += '/conditions/q/TX/Austin.json'
    response = requests.get(url)
    cur_value = float(response.json()['current_observation']['precip_1hr_in'])
    cur_date = response.json()['current_observation']['observation_epoch']
    cur_date = datetime.datetime.fromtimestamp(int(cur_date))
    result[RAINFALL] = [(cur_date, cur_value)]
    return result


def update_db(period):
    with orm.db_session:
        result = get_values(period, '08155500', '00060', '00065')
        for key in result.keys():
            if key == DISCHARGE:
                for value in result[key]:
                    if not orm.exists(v for v in DischargeRate if v.time_stamp == value[0]):
                        DischargeRate(time_stamp=value[0], value=value[1])
            elif key == GAGE_HEIGHT:
                for value in result[key]:
                    if not orm.exists(v for v in GageHeight if v.time_stamp == value[0]):
                        GageHeight(time_stamp=value[0], value=value[1])
            elif key == RAINFALL:
                for value in result[key]:
                    if not orm.exists(v for v in Rainfall if v.time_stamp == value[0]):
                        Rainfall(time_stamp=value[0], value=value[1])


update_db(1)
# with orm.db_session:
#     orm.select(d for d in DischargeRate).show()