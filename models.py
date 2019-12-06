from datetime import datetime
from playhouse.postgres_ext import ArrayField

import peewee
import settings

db = peewee.PostgresqlDatabase(
    "gdg-devfest-19",
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class NewsletterTelegram(BaseModel):
    id = peewee.IntegerField(unique=True)

    class Meta:
        db_table = "newsletter_telegram"


class NewsletterEmail(BaseModel):
    email = peewee.CharField(max_length=128, unique=True)

    class Meta:
        db_table = "newsletter_email"


class Voter(BaseModel):
    nif = peewee.CharField(max_length=320, unique=True)
    wallet = peewee.CharField(max_length=16, unique=True)
    telegram_id = peewee.IntegerField(null=True)
    email = peewee.DateTimeField(max_length=320, null=True)

    class Meta:
        db_table = "voters"


class Proposals(BaseModel):
    id = peewee.FixedCharField(max_length=8, unique=True)
    deadline = peewee.IntegerField()
    description = peewee.CharField(max_length=320, index=True)

    class Meta:
        db_table = "proposals"


class Votes(BaseModel):
    wallet = peewee.CharField(max_length=42, unique=True)
    signature = peewee.CharField(max_length=66, unique=True)
    proposal_id = peewee.IntegerField()
    in_favor = peewee.BooleanField()
    txid = peewee.CharField(max_length=66, null=True)

    class Meta:
        db_table = "votes"


class Proofs(BaseModel):
    proposal_id = peewee.FixedCharField(max_length=8, unique=True)
    txid = peewee.FixedCharField(max_length=66, index=True)
    deadline = peewee.IntegerField()
    updated = peewee.DateTimeField(default=datetime.utcnow, index=True)

    class Meta:
        db_table = "proofs"


db.create_tables([NewsletterTelegram], safe=True)
db.create_tables([NewsletterEmail], safe=True)
db.create_tables([Voter], safe=True)
db.create_tables([Proposals], safe=True)
db.create_tables([Votes], safe=True)
db.create_tables([Proofs], safe=True)
