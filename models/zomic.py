import peewee
from time import time

from settings import DB, LENGTHS, DEFAULTS

# db = peewee.SqliteDatabase(':memory:')
db = peewee.PostgresqlDatabase(
    DB["name"],
    user=DB["user"],
    password=DB["password"],
    host=DB["host"],
    port=DB["port"],
)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Community(BaseModel):
    id = peewee.CharField(max_length=LENGTHS["id"], unique=True, index=True)
    name = peewee.CharField(max_length=LENGTHS["default"], unique=True)
    secret = peewee.BooleanField(default=False)
    required_info = peewee.CharField(max_length=LENGTHS["json"], null=False)
    founder = peewee.CharField(max_length=LENGTHS["hash"], null=False)
    permissions = peewee.CharField(max_length=LENGTHS["json"],
                                   default=str(DEFAULTS["permissions"]))
    telegram_token = peewee.CharField(max_length=LENGTHS["telegram_token"], null=True)  # Private
    submission_rate = peewee.IntegerField(default=DEFAULTS["submission_rate"])
    timestamp = peewee.IntegerField()  # Signed
    wallet = peewee.CharField(max_length=LENGTHS["wallet"], null=False)
    signature = peewee.CharField(max_length=LENGTHS["signature"], unique=True)
    db_ts = peewee.IntegerField(default=time())

    class Meta:
        db_table = "communities"


class User(BaseModel):  # New Entry for each User Wallet - Immutable
    id = peewee.CharField(max_length=LENGTHS["hash"], null=False)
    community_id = peewee.CharField(max_length=LENGTHS["id"], null=False, index=True)
    wallet = peewee.CharField(max_length=LENGTHS["wallet"], unique=True)  # Private
    admin = peewee.BooleanField(default=False)
    active = peewee.BooleanField(default=True)
    db_ts = peewee.IntegerField(default=time())

    class Meta:
        db_table = "users"


class Proposal(BaseModel):  # New Entry for each Proposal - Immutable
    id = peewee.CharField(max_length=LENGTHS["id"], null=False, index=True)  # Random Generated
    community_id = peewee.CharField(max_length=LENGTHS["id"], null=False, index=True)  # Signed
    approval_rate = peewee.IntegerField(default=DEFAULTS["approval_rate"])  # Signed
    description = peewee.CharField(max_length=LENGTHS["description"])  # Signed
    title = peewee.CharField(max_length=LENGTHS["default"], unique=True)  # Signed
    type = peewee.CharField(max_length=LENGTHS["type"])  # Signed
    deadline = peewee.IntegerField(null=False)  # Signed
    status = peewee.CharField(max_length=LENGTHS["type"], default=DEFAULTS["status"])
    in_favor = peewee.IntegerField(null=True)
    against = peewee.IntegerField(null=True)
    timestamp = peewee.IntegerField()  # Signed
    wallet = peewee.CharField(max_length=LENGTHS["wallet"])
    signature = peewee.CharField(max_length=LENGTHS["signature"], unique=True)
    db_ts = peewee.IntegerField(default=time())

    class Meta:
        db_table = "proposals"


class Vote(BaseModel):  # New Entry for each Vote - Immutable
    community_id = peewee.CharField(max_length=LENGTHS["id"], null=False, index=True)  # Signed
    proposal_id = peewee.CharField(max_length=LENGTHS["id"], null=False, index=True)  # Signed
    user = peewee.CharField(max_length=LENGTHS["hash"], null=False, index=True)  # Private
    in_favor = peewee.BooleanField()  # Signed
    timestamp = peewee.IntegerField()  # Signed
    wallet = peewee.CharField(max_length=LENGTHS["wallet"])
    signature = peewee.CharField(max_length=LENGTHS["signature"], unique=True)
    db_ts = peewee.IntegerField(default=time())

    class Meta:
        db_table = "votes"


class Proof(BaseModel):
    community_id = peewee.CharField(max_length=LENGTHS["id"], null=False, index=True)
    type = peewee.CharField(max_length=LENGTHS["type"], null=False)
    user = peewee.CharField(max_length=LENGTHS["hash"], null=True)  # Only for add_user/remove_user
    wallet = peewee.CharField(max_length=LENGTHS["wallet"],  null=True)  # Only for add_user
    payload = peewee.CharField(max_length=LENGTHS["payload"], null=False)
    signature = peewee.CharField(max_length=LENGTHS["signature"], unique=True)
    ack = peewee.CharField(max_length=LENGTHS["signature"], unique=True)
    txid = peewee.CharField(max_length=LENGTHS["transaction"], null=True)
    db_ts = peewee.IntegerField(default=time())

    class Meta:
        db_table = "proofs"


class NewsletterTelegram(BaseModel):
    community_id = peewee.CharField(max_length=LENGTHS["id"], null=False)
    chat_id = peewee.IntegerField()

    class Meta:
        db_table = "newsletter_telegram"
        indexes = ((('community_id', 'chat_id'), True),)


class NewsletterEmail(BaseModel):
    community_id = peewee.CharField(max_length=LENGTHS["id"], null=False)
    email = peewee.CharField(max_length=LENGTHS["email"])

    class Meta:
        db_table = "newsletter_email"
        indexes = ((('community_id', 'email'), True),)


"""
Community.drop_table()
User.drop_table()
Proposal.drop_table()
Vote.drop_table()
Proof.drop_table()
NewsletterTelegram.drop_table()
NewsletterEmail.drop_table()
"""

db.create_tables([Community], safe=True)
db.create_tables([User], safe=True)
db.create_tables([Proposal], safe=True)
db.create_tables([Vote], safe=True)
db.create_tables([Proof], safe=True)
db.create_tables([NewsletterTelegram], safe=True)
db.create_tables([NewsletterEmail], safe=True)
