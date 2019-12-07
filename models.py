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
    status = peewee.CharField(max_length=TITLE_LENGTH, default=settings.OPEN)
    wallet = peewee.CharField(max_length=WALLET_LENGTH, null=True)
    in_favor = peewee.IntegerField(null=True)
    against = peewee.IntegerField(null=True)
    txid = peewee.CharField(max_length=TRANSACTION_LENGTH, null=True)

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

    class Meta:
        db_table = "votes"


NewsletterTelegram.drop_table()
NewsletterEmail.drop_table()
Proposals.drop_table()
Votes.drop_table()
Voters.drop_table()

db.create_tables([NewsletterTelegram], safe=True)
db.create_tables([NewsletterEmail], safe=True)
db.create_tables([Proposals], safe=True)
db.create_tables([Votes], safe=True)
db.create_tables([Voters], safe=True)


Proposals.create(deadline="2020-01-01",
                 title="Combater Fake News",
                 topic=settings.TOPICS[0],
                 description="Descrição detalhada o Combate às Fake News",
                 wallet="0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46")
Proposals.create(deadline="2020-01-01",
                 title="Combater a Info Exclusão",
                 topic=settings.TOPICS[1],
                 description="Descrição detalhada sobre o Combate à Info Exclusão",
                 wallet="0x8fa6967433b76a50e0653910798b0c3d7e96f4b4")
Proposals.create(deadline="2020-01-01",
                 title="Apoio à Cidadania",
                 topic=settings.TOPICS[2],
                 description="Descrição detalhada sobre o Apoio à Cidadania",
                 wallet="0xe8Cc03Dd6b3260caca81638F70Ba2D0f7B4BD49A")
Proposals.create(deadline="2020-01-01",
                 title="Promover Mais Transparência Política",
                 topic=settings.TOPICS[3],
                 description="Descrição detalhada sobre a Promoção de Mais Transparência Política",
                 wallet="0x0aa704E5c55792698c8f72418d35Af2C6f521caa")

Voters.create(user_hash="0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46",
              wallet="0x64767925a6df9e1ac8718ade7b347ea0eb9f9d46")
Voters.create(user_hash="0x8fa6967433b76a50e0653910798b0c3d7e96f4b4",
              wallet="0x8fa6967433b76a50e0653910798b0c3d7e96f4b4")
Voters.create(user_hash="0xe8Cc03Dd6b3260caca81638F70Ba2D0f7B4BD49A",
              wallet="0xe8Cc03Dd6b3260caca81638F70Ba2D0f7B4BD49A")
Voters.create(user_hash="0x0aa704E5c55792698c8f72418d35Af2C6f521caa",
              wallet="0x0aa704E5c55792698c8f72418d35Af2C6f521caa")

NewsletterEmail.create(email="zepcp@hotmail.com")
NewsletterTelegram.create(id=546114127)
