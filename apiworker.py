import requests
import dateutil.parser
from models import DischargeRate, GageHeight, Rainfall
from pony import orm

# Parameter codes
DISCHARGE = '00060'
GAGE_HEIGHT = '00065'
RAINFALL = '00045'

# Site codes
BARTON = '08155500'
ONION_CREEK = '08158700'


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
    return result


def update_db(period):
    with orm.db_session:
        barton = get_values(period, BARTON, DISCHARGE, GAGE_HEIGHT)
        rainfall = get_values(period, ONION_CREEK, RAINFALL)
        result = {**barton, **rainfall}
        for key in result.keys():
            if key == DISCHARGE:
                for value in result[key]:
                    if not orm.exists(v for v in DischargeRate if v.time_stamp == value[0]):
                        # Convert to gallons per second
                        gallons = float(value[1]) * 7.48051948
                        DischargeRate(time_stamp=value[0], value=gallons)
            elif key == GAGE_HEIGHT:
                for value in result[key]:
                    if not orm.exists(v for v in GageHeight if v.time_stamp == value[0]):
                        GageHeight(time_stamp=value[0], value=value[1])
            elif key == RAINFALL:
                for value in result[key]:
                    if not orm.exists(v for v in Rainfall if v.time_stamp == value[0]):
                        Rainfall(time_stamp=value[0], value=value[1])

if __name__ == "__main__":
    update_db(365)