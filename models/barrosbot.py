import peewee
import time

from settings import LENGTHS, BARROSBOT_DB
from playhouse.postgres_ext import ArrayField
from strings import barrosbot as strings

# db = peewee.SqliteDatabase(':memory:')
db = peewee.PostgresqlDatabase(BARROSBOT_DB["name"],
                               user=BARROSBOT_DB["user"],
                               password=BARROSBOT_DB["password"],
                               host=BARROSBOT_DB["host"],
                               port=BARROSBOT_DB["port"])


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Log(BaseModel):
    uid = peewee.IntegerField()
    username = peewee.CharField(max_length=LENGTHS["default"])
    update_id = peewee.IntegerField()
    text = peewee.CharField(max_length=LENGTHS["payload"])
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "logs"


class Game(BaseModel):
    owner_id = peewee.IntegerField()
    owner = peewee.CharField(max_length=LENGTHS["default"])
    roles = ArrayField(peewee.CharField, default=strings.DEFAULT_ROLE)
    days = peewee.IntegerField(null=True)
    hostages = peewee.CharField(max_length=LENGTHS["default"], null=True)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "games"


class Guest(BaseModel):
    game_id = peewee.IntegerField()
    player_id = peewee.IntegerField()
    player = peewee.CharField(max_length=LENGTHS["default"])
    role = peewee.CharField(max_length=LENGTHS["default"], null=True)
    room = peewee.BooleanField(null=True)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "guests"


class Share(BaseModel):
    game_id = peewee.IntegerField()
    from_id = peewee.IntegerField()
    to_id = peewee.IntegerField(null=True)
    role = peewee.BooleanField()
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "shares"


# db.drop_tables([Log], safe=True)
# db.drop_tables([Game], safe=True)
# db.drop_tables([Guest], safe=True)
# db.drop_tables([Share], safe=True)

db.create_tables([Log], safe=True)
db.create_tables([Game], safe=True)
db.create_tables([Guest], safe=True)
db.create_tables([Share], safe=True)
