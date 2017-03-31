import requests
import dateutil.parser
from models import DischargeRate

# Parameter codes
parameter_codes = {'00060': 'discharge', '00065': "gage_height"}

# Hard coded URL for Barton Springs, Austin TX
# url = 'https://waterservices.usgs.gov/nwis/iv/?format=json&indent=on&\
# sites=08155500&period=P365D&parameterCd=00060,00065&siteStatus=all'


def get_values(period, site, *params):
    """
    Get values from the USGS API. Returns {'paramcode': [(dateTime, value),],}
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


result = get_values(7, '08155500', '00060', '00065')

