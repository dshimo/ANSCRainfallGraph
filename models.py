from pony import orm
import datetime

db = orm.Database("sqlite",
                  "vals.sqlite",
                  create_db=True)


class DischargeRate(db.Entity):
    time_stamp = orm.Required(datetime.datetime)
    value = orm.Required(float)


class GageHeight(db.Entity):
    time_stamp = orm.Required(datetime.datetime)
    value = orm.Required(float)

db.generate_mapping(create_tables=True)