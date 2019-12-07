from datetime import datetime

import peewee
import settings

EMAIL_LENGTH = 128
SIG_LENGTH = 132
TRANSACTION_LENGTH = 66
WALLET_LENGTH = 42
DESCRIPTION_LENGTH = 320
PROPOSAL_ID_LENGTH = 8
TITLE_LENGTH = 45

# db = peewee.SqliteDatabase(':memory:')
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


class Proposals(BaseModel):
    deadline = peewee.DateTimeField()
    title = peewee.CharField(max_length=TITLE_LENGTH, unique=True)
    topic = peewee.CharField(max_length=TITLE_LENGTH)
    description = peewee.CharField(max_length=DESCRIPTION_LENGTH, unique=True)
    status = peewee.CharField(max_length=TITLE_LENGTH)
    wallet = peewee.CharField(max_length=WALLET_LENGTH, null=True)

    class Meta:
        db_table = "proposals"


class Voters(BaseModel):
    user_hash = peewee.CharField(max_length=TRANSACTION_LENGTH, unique=True)
    wallet = peewee.CharField(max_length=WALLET_LENGTH, unique=True)
    telegram_id = peewee.IntegerField(null=True)
    email = peewee.CharField(max_length=EMAIL_LENGTH, null=True)

    class Meta:
        db_table = "voters"


class Votes(BaseModel):
    user_hash = peewee.CharField(max_length=TRANSACTION_LENGTH)
    wallet = peewee.CharField(max_length=WALLET_LENGTH)
    signature = peewee.CharField(max_length=SIG_LENGTH, unique=True)
    proposal_id = peewee.IntegerField()
    in_favor = peewee.BooleanField()
    timestamp = peewee.IntegerField()
    txid = peewee.CharField(max_length=TRANSACTION_LENGTH, null=True)

    class Meta:
        db_table = "votes"


class Proofs(BaseModel):
    proposal_id = peewee.IntegerField()
    txid = peewee.FixedCharField(max_length=TRANSACTION_LENGTH, index=True)
    updated = peewee.DateTimeField(default=datetime.utcnow, index=True)

    class Meta:
        db_table = "proofs"


db.create_tables([NewsletterTelegram], safe=True)
db.create_tables([NewsletterEmail], safe=True)
db.create_tables([Proposals], safe=True)
db.create_tables([Votes], safe=True)
db.create_tables([Voters], safe=True)
db.create_tables([Proofs], safe=True)
