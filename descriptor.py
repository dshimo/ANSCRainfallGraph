from random import uniform,randint
from models import DischargeRate,GageHeight,Rainfall,TotalRainfall, Temperature, Ph
from pony import orm
import datetime
import dateutil.parser as dparser

# "lawns"   : (lambda x: x*145.29*6048000, "That's enough to water @ lawns per week!"),
# "punch"   : (lambda x: x, "That's the same force as getting punched by @ average men!")}
DISCHARGE = {"bottles": (lambda x: x*7.5708,"That's like pouring out @ water bottles per second!"),
             "taps": (lambda x: x/0.036667, "That's roughly equivalent to @ kitchen sinks turned on at the same time!"),
             "milk": (lambda x: x*10.666666667, "If Barton Springs was milk, you could eat @ bowls of cereal per second!"),
             "bathtubs": (lambda x: x/80, "That's enough water to fill @ bathtubs per second!"),
             "toilets": (lambda x: x/0.35, "That's the same rate as @ toilets being flushed at the same time!")}

GAGEHEIGHT = {"cars": (lambda x: x//5, "That's like @ cars stacked on top of each other!"),
              "buses": (lambda x: x//10, "That's more than @ buses stacked on top of each other!"),
              "Shaquille O'Neals": (lambda x: x/7.08333, "That's @ Shaquille O'Neals stacked from head to toe!"),
              "whale": (lambda x: x > 20, "That's deep enough for a blue whale to swim in!"),
              "giraffe": (lambda x: x > 16, "That's deep enough for a giraffe to swim in!"),
              "trex": (lambda x: x > 20, "That means a T-rex could take a bath in Barton Springs!"),
              "house": (lambda x: x > 20, "That's enough to submerge a 2-story house!")}


def make_descriptions():
    descriptions = {"discharge": discharge_text(), "gage": gage_text(),
                    "faq": ["The temperature of Barton Springs is 68-70 degrees year round.",
                            "The outflow of Barton Springs measures between 30-50 million gallons a day.",
                            "Barton Springs is home to the endangered Barton Springs Salamander.",
                            "The depth of Barton Springs Pool runs from 0 ft at the shallow end to 18 ft at the deep end.",
                            'Barton Springs is named after William "Billy" Barton who settled his family here in 1837.',
                            "Three of the four springs in Zilker Park are named after William Barton's daughters, Zenobia, Parthenia and Eliza.",
                            "Before Europeans settled the area the indigenous peoples of Central Texas considered the springs to be sacred.",
                            "Spanish explorers arrived here around 1730 and set up temporary missions along Barton Creek.",
                            "Construction on the dams that created a permanent pool at Barton Springs began in 1920.",
                            "Andrew Zilker deeded the parklands and Barton Springs to the City of Austin in 1918.",
                            "Barton Springs Pool is subject to flooding when there are heavy rains in the hill country.",
                            "Barton Springs Salamanders are tailed amphibians that are uniquely adapted to thrive in a spring environment.",
                            temperature_text(),
                            ph_text()],
                    "rainfall": rain_text()}

    return descriptions


def current(strVal, Database, strValUnits):
    with orm.db_session:
        # fetch most current datetime for val
        latest = orm.max(v.time_stamp for v in Database)
        if not isinstance(latest, datetime.datetime):
            latest = dparser.parse(latest)
        val = orm.select(v for v in Database if v.time_stamp == latest)
        # should only obtain single element with latest timestamp
        for v in val:
            val = int(v.value)

    return ["The " + strVal + " is currently " + str(val) + " " + strValUnits + ".", val]


def discharge_text():
    listDescriptions = []

    data = current("flow speed", DischargeRate, "gallons per second")
    description = data[0]
    for word in DISCHARGE:
        val = round(DISCHARGE[word][0](data[1]), 2)
        listDescriptions.append(description + " " + DISCHARGE[word][1].replace("@", "{:,}".format(int(val))))

    return listDescriptions


def gage_text():
    listDescriptions = []

    data = current("depth", GageHeight, "feet")
    description = data[0]
    for word in GAGEHEIGHT:
        val = GAGEHEIGHT[word][0](data[1])
        add = val if isinstance(val, bool) else True
        val = round(val, 2)
        if add:
            listDescriptions.append(description + " " + GAGEHEIGHT[word][1].replace("@", str(val)))
    
    return listDescriptions 


def rain_text():
    with orm.db_session:
        # fetch most current datetime for val and days
        latest = orm.max(v.time_stamp for v in TotalRainfall)
        if not isinstance(latest, datetime.datetime):
            latest = dparser.parse(latest)
        val = orm.select(v for v in TotalRainfall if v.time_stamp == latest)
        # should only obtain single element with latest timestamp
        for v in val:
            days = int(v.days)
            value = v.value

    listDescriptions = ["The total rainfall has been " + str(round(value, 2)) + " inches over the past " + str(days) + " days."]

    return listDescriptions


def ph_text():
    with orm.db_session:
        latest = orm.max(v.time_stamp for v in Ph)
        if not isinstance(latest, datetime.datetime):
            latest = dparser.parse(latest)
        val = orm.select(v for v in Ph if v.time_stamp == latest)
        for v in val:
            value = v.value

    description = "The pH of Barton Springs is currently " + str(value) + "."

    return description


def temperature_text():
    with orm.db_session:
        latest = orm.max(v.time_stamp for v in Temperature)
        if not isinstance(latest, datetime.datetime):
            latest = dparser.parse(latest)
        val = orm.select(v for v in Temperature if v.time_stamp == latest)
        for v in val:
            value = 9.0/5.0 * v.value + 32

    description = "The water temperature of Barton Springs is currently " + str(value) + "°F."

    return description

if __name__ == "__main__":
    print(make_descriptions())
