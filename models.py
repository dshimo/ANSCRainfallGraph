from pony import orm
import datetime

db = orm.Database("sqlite",
                  "vals.sqlite",
                  create_db=True)


class DischargeRate(db.Entity):
    time_stamp = orm.PrimaryKey(datetime.datetime)
    value = orm.Required(float)


class GageHeight(db.Entity):
    time_stamp = orm.PrimaryKey(datetime.datetime)
    value = orm.Required(float)


class Rainfall(db.Entity):
    time_stamp = orm.PrimaryKey(datetime.datetime)
    value = orm.Required(float)


class TotalRainfall(db.Entity):
    time_stamp = orm.PrimaryKey(datetime.datetime)
    value = orm.Required(float)
    days = orm.Required(int)
db.generate_mapping(create_tables=True)
