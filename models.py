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


class Ph(db.Entity):
    time_stamp = orm.PrimaryKey(datetime.datetime)
    value = orm.Required(float)


class Temperature(db.Entity):
    time_stamp = orm.PrimaryKey(datetime.datetime)
    value = orm.Required(float)


db.generate_mapping(create_tables=True)


# Drop all data and reset db
def reset_db():
    db.drop_all_tables(True)
    db.create_tables()
