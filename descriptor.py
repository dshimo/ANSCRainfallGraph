from random import randint
from math import floor

# DISCHARGE  = ['bottles','lawns','spit','taps','bathtubs','toilets','milk','punch']
DISCHARGE = {'bottles': lambda x: x*56.6337}
# GAGEHEIGHT = ['cars','bus','shaqs','whale','giraffe','trex','house']
GAGEHEIGHT = {'cars'   : lambda x: x*4/12.0, \
              'buses'  : lambda x: x*10/12.0, \
              'Shaquille O\'Neals': lambda x: x/85.0}

ADJECTIVE = [' approximately', ' roughly'      , ' more or less', ' almost'      , ' practically']
EQUALITY  = [' the same as'  , ' equivalent to', ' identical to', ' analogous to', ' parallel to']
    
def make_descriptions():
    discharge_rate = randint(95, 105)
    gage_height    = randint(23, 25)

    discharge_text(discharge_rate)
    gage_text(gage_height)

def discharge_text(discharge_rate):
    description = "The discharge rate is currently " + str(discharge_rate) + " cubic feet per second."
    description += convert(DISCHARGE, discharge_rate)
    print(description)


def gage_text(gage_height):
    description = "The gage height is currently " + str(gage_height) + " inches."
    description += convert(GAGEHEIGHT, gage_height)
    print(description)

def convert(graph, val):
    word = (graph.keys())[randint(0,len(graph) - 1)]
    conversion = int(round(graph[word](val), 0))
    return " That's" + ADJECTIVE[randint(0,4)] + EQUALITY[randint(0,4)] + " " + str(conversion) + " " + word + "!"

if __name__ == "__main__":
    make_descriptions()
