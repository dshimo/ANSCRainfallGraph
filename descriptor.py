from random import uniform,randint

# "lawns"   : (lambda x: x*145.29*6048000, "That's enough to water @ lawns per week!"),
DISCHARGE = {"bottles" : (lambda x: x*56.6337,"That's like pouring @ bottles per second!"), 
             "spit"    : (lambda x: x, "That's the same as @ people spitting at the same time!"),
             "taps"    : (lambda x: x*448.8312, "That's roughly equivalent to @ sinks turned on at the same time!"),
             "bathtubs": (lambda x: x*314.18184, "That's enough water to fill @ bathtubs per second!"),
             "toilets" : (lambda x: x/0.0267361, "That's the same rate as @ toilets being flushed at the same time!"),
             "milk"    : (lambda x: x, "If Barton Springs was milk, you would need to eat @ boxes of cereal per second!"),
             "punch"   : (lambda x: x, "That's the same force as getting punched by @ average men!")}

GAGEHEIGHT = {"cars"    : (lambda x: x/5.0, "That's approximately @ cars stacked on top each other!"),  
              "buses"   : (lambda x: x/10.0, "That's approximately @ buses stacked on top each other!"),
              "Shaquille O'Neals": (lambda x: x/85.0, "That's @ Shaquille O'Neals stacked from head to toe!"),
              "whale"   : (lambda x: x > 20, "That's deep enough for a blue whale to swim in!"),
              "giraffe" : (lambda x: x > 16, "That's deep enough for a giraffe to swim in!"),
              "trex"    : (lambda x: x > 20, "That means a T-Rex could take a bath in Barton Springs!"),
              "house"   : (lambda x: x > 20, "That's enough to submerge a 2-story house!")}

def make_descriptions():
    discharge_rate = round(uniform(9, 140),2)
    gage_height    = round(uniform(18, 30),2)

    descriptions = {"discharge":[discharge_text(discharge_rate)], "gage":[gage_text(gage_height)],
                    "faq":["The temperature of Barton Springs is 68-70 degrees year round.",
                           "The outflow of Barton Springs measures between 30-50 million gallons a day",
                           "Barton Springs is home of the endangered Barton Springs Salamander",
                           "The depth of Barton Springs pool runs from 0' at the shallow end to 18' at the deep end",
                           "Barton Springs is named after William \"Billy\" Barton who settled his family here in 1837",
                           "Three of the four springs in Zilker Park are named after William Barton's daughters, Zenobia, Parthenia and Eliza",
                           "Before Europeans settled the area the indigenous peoples of Central Texas considered the springs to be sacred",
                           "Spanish explorers arrived here around 1730 and set up temporary missions along Barton Creek",
                           "Construction on the dams that created a permanent pool at Barton Springs began in 1920",
                           "Andrew Zilker deeded the parklands and Barton Springs to the City of Austin in 1918",
                           "Barton Springs pool is subject to flooding when there are heavy rains in the hill country",
                           "Barton Springs Salamanders are tailed amphibians that are uniquely adapted to thrive in a spring environment"]}


    print(descriptions)
    return descriptions

def discharge_text(discharge_rate):
    description = current("discharge rate", discharge_rate, "cubic feet per second")
    description += " " + convert(DISCHARGE, discharge_rate)
    return description

def gage_text(gage_height):
    description = current("gage height", gage_height, "feet")
    description += " " + convert(GAGEHEIGHT, gage_height)
    return description

def current(strVal, val, strValUnits):
    return "The " + strVal + " is currently " + str(val) + " " + strValUnits + "."

def convert(graph, val):
    word = list(graph)[randint(0,len(graph) - 1)]
    
    while not graph[word][0](val) and graph == GAGEHEIGHT:
        word = list(graph)[randint(0,len(graph) - 1)]

    conversion = round(graph[word][0](val), 2)
    conversion = int(conversion) if int(conversion) == conversion else conversion
    return graph[word][1].replace("@",str(conversion))

if __name__ == "__main__":
    make_descriptions()
