from datetime import datetime

import peewee
import settings

EMAIL_LENGTH = 128
TRANSACTION_LENGTH = 66
WALLET_LENGTH = 42
DESCRIPTION_LENGTH = 320
PROPOSAL_ID_LENGTH = 8
NIF_LENGTH = 9

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
    email = peewee.CharField(max_length=EMAIL_LENGTH, unique=True)

    class Meta:
        db_table = "newsletter_email"


class Voter(BaseModel):
    nif = peewee.CharField(max_length=NIF_LENGTH, unique=True)
    wallet = peewee.CharField(max_length=WALLET_LENGTH, unique=True)
    telegram_id = peewee.IntegerField(null=True)
    email = peewee.CharField(max_length=EMAIL_LENGTH, null=True)

    class Meta:
        db_table = "voters"


class Proposals(BaseModel):
    id = peewee.FixedCharField(max_length=PROPOSAL_ID_LENGTH, unique=True)
    deadline = peewee.IntegerField()
    description = peewee.CharField(max_length=DESCRIPTION_LENGTH, index=True)

    class Meta:
        db_table = "proposals"


class Votes(BaseModel):
    wallet = peewee.CharField(max_length=WALLET_LENGTH, unique=True)
    signature = peewee.CharField(max_length=TRANSACTION_LENGTH, unique=True)
    proposal_id = peewee.IntegerField()
    in_favor = peewee.BooleanField()
    txid = peewee.CharField(max_length=TRANSACTION_LENGTH, null=True)

    class Meta:
        db_table = "votes"


class Proofs(BaseModel):
    proposal_id = peewee.FixedCharField(max_length=PROPOSAL_ID_LENGTH, unique=True)
    txid = peewee.FixedCharField(max_length=TRANSACTION_LENGTH, index=True)
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
