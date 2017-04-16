from random import uniform,randint
from models import DischargeRate,GageHeight
from pony import orm
import datetime
import dateutil.parser as dparser

# "lawns"   : (lambda x: x*145.29*6048000, "That's enough to water @ lawns per week!"),
# milk to cereal was too variable. made it into glasses of milk instead. used 8oz cups
# spits are also variable
# "punch"   : (lambda x: x, "That's the same force as getting punched by @ average men!")}
DISCHARGE = {"bottles": (lambda x: x*56.6337,"That's like pouring out @ bottles per second!"),
             "taps": (lambda x: x*448.8312, "That's roughly equivalent to @ sinks turned on at the same time!"),
             "milk": (lambda x: x*119.68825, "If Barton Springs was milk, you would need @ glasses every second to catch it all!"),
             "bathtubs": (lambda x: x*314.18184, "That's enough water to fill @ bathtubs per second!"),
             "toilets": (lambda x: x/0.0267361, "That's the same rate as @ toilets being flushed at the same time!")}

GAGEHEIGHT = {"cars": (lambda x: x/5.0, "That's approximately @ cars stacked on top each other!"),
              "buses": (lambda x: x/10.0, "That's approximately @ buses stacked on top each other!"),
              "Shaquille O'Neals": (lambda x: x/7.08333, "That's @ Shaquille O'Neals stacked from head to toe!"),
              "whale": (lambda x: x > 20, "That's deep enough for a blue whale to swim in!"),
              "giraffe": (lambda x: x > 16, "That's deep enough for a giraffe to swim in!"),
              "trex": (lambda x: x > 20, "That means a T-Rex could take a bath in Barton Springs!"),
              "house": (lambda x: x > 20, "That's enough to submerge a 2-story house!")}


def make_descriptions():
    descriptions = {"discharge": discharge_text(), "gage": gage_text(),
                    "faq": ["The temperature of Barton Springs is 68-70 degrees year round.",
                            "The outflow of Barton Springs measures between 30-50 million gallons a day.",
                            "Barton Springs is home of the endangered Barton Springs Salamander.",
                            "The depth of Barton Springs pool runs from 0' at the shallow end to 18' at the deep end.",
                            "Barton Springs is named after William \"Billy\" Barton who settled his family here in 1837.",
                            "Three of the four springs in Zilker Park are named after William Barton's daughters, Zenobia, Parthenia and Eliza.",
                            "Before Europeans settled the area the indigenous peoples of Central Texas considered the springs to be sacred.",
                            "Spanish explorers arrived here around 1730 and set up temporary missions along Barton Creek.",
                            "Construction on the dams that created a permanent pool at Barton Springs began in 1920.",
                            "Andrew Zilker deeded the parklands and Barton Springs to the City of Austin in 1918.",
                            "Barton Springs pool is subject to flooding when there are heavy rains in the hill country.",
                            "Barton Springs Salamanders are tailed amphibians that are uniquely adapted to thrive in a spring environment."]}

    return descriptions


def discharge_text():
    listDescriptions = []

    data = current("discharge rate", DischargeRate, "ft\u003csup\u003e3\u003c\u002Fsup\u003e per second")
    description = data[0]
    for word in DISCHARGE:
        val = round(DISCHARGE[word][0](data[1]),2)
        listDescriptions.append(description + " " + DISCHARGE[word][1].replace("@",str(val)))

    return listDescriptions


def gage_text():
    listDescriptions = []

    data = current("gage height", GageHeight, "feet")
    description = data[0]
    for word in GAGEHEIGHT:
        val = GAGEHEIGHT[word][0](data[1])
        add = val if isinstance(val, bool) else True
        val = round(val, 2)
        if add:
            listDescriptions.append(description + " " + GAGEHEIGHT[word][1].replace("@",str(val)))
    
    return listDescriptions 


def current(strVal, Database, strValUnits):
    with orm.db_session:
        # fetch most current datetime for val
        latest = orm.max(v.time_stamp for v in Database)
        if not isinstance(latest, datetime.datetime):
            latest = dparser.parse(latest)
        val = orm.select(v for v in Database if v.time_stamp == latest)
        # should only obtain single element with latest timestamp
        for v in val:
            val = v.value

    return ["The " + strVal + " is currently " + str(val) + " " + strValUnits + ".", val]

if __name__ == "__main__":
    make_descriptions()
