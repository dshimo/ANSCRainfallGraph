import requests

'''Hard coded URL for Barton Springs, Austin TX'''
url = 'https://waterservices.usgs.gov/nwis/iv/?format=json&indent=on&\
sites=08155500&period=P4D&parameterCd=00060,00065&siteStatus=all'

class Discharge 
    def


response = requests.get(url)
print(response.json())
