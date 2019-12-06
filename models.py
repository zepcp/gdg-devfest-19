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
    id = peewee.IntegerField(unique=True, required=True)

    class Meta:
        db_table = "newsletter_telegram"


class NewsletterEmail(BaseModel):
    email = peewee.CharField(max_length=320, unique=True, required=True)

    class Meta:
        db_table = "newsletter_email"


class Voter(BaseModel):
    nif = peewee.CharField(max_length=320, unique=True, index=True)
    keypass = peewee.CharField(max_length=16, index=True)
    sha1 = peewee.CharField(max_length=64, null=True)
    updated = peewee.DateTimeField(default=datetime.utcnow, index=True)

    class Meta:
        db_table = "developers"


class Apk(BaseModel):
    original_md5sum = peewee.FixedCharField(max_length=32, index=True)
    compiler = peewee.CharField(max_length=10, index=True)
    icon_data = ArrayField(peewee.CharField, null=True)
    updated = peewee.DateTimeField(default=datetime.utcnow, index=True)

    class Meta:
        db_table = "apks"


class Sku(BaseModel):
    package = peewee.CharField(max_length=320, index=True)
    sku = peewee.CharField(max_length=3000)
    details = peewee.CharField(max_length=20000)
    updated = peewee.DateTimeField(default=datetime.utcnow, index=True)

    class Meta:
        db_table = "skus"


class Rule(BaseModel):
    original_md5sum = peewee.FixedCharField(max_length=32, index=True)
    FileReplacement = peewee.BooleanField(default=False, null=True)
    IconReplacement = peewee.BooleanField(default=False, null=True)
    PoAInjection = peewee.BooleanField(default=False, null=True)
    WalletInjection = peewee.BooleanField(default=False, null=True)
    ManifestPermissions = peewee.BooleanField(default=False, null=True)
    ManifestPoA = peewee.BooleanField(default=False, null=True)
    ManifestYML = peewee.BooleanField(default=False, null=True)
    GoogleLicenseCheckRemover = peewee.BooleanField(default=False, null=True)
    SmaliReplacementsBilling = peewee.BooleanField(default=False, null=True)
    XMLStringsPoA = peewee.BooleanField(default=False, null=True)
    updated = peewee.DateTimeField(default=datetime.utcnow, index=True)

    class Meta:
        db_table = "rules"


class Plugins(BaseModel):
    updated = peewee.DateTimeField(default=datetime.utcnow, index=True)
    package_name = peewee.CharField(index=True)
    plugin_ids = ArrayField(peewee.CharField, index=False)
    arguments = ArrayField(peewee.CharField, index=False)

    class Meta:
        db_table = "plugins"
        primary_key = peewee.CompositeKey("package_name")


class PluginsReport(BaseModel):
    updated = peewee.DateTimeField(default=datetime.utcnow, index=True)
    package_name = peewee.CharField(index=True)
    version_code = peewee.IntegerField(index=True)
    plugin_ids = ArrayField(peewee.CharField, index=False)
    arguments = ArrayField(peewee.CharField, index=False)
    plugin_result = ArrayField(peewee.IntegerField, index=False, null=True)
    plugin_result_message = ArrayField(peewee.CharField, index=False, null=True)

    class Meta:
        db_table = "plugin_reports"


class Splits(BaseModel):
    issue = peewee.CharField(max_length=10, index=True)
    name = peewee.CharField(max_length=64, index=True)
    original_md5sum = peewee.CharField(max_length=32)
    repackaged_md5sum = peewee.CharField(max_length=32, null=True)

    class Meta:
        indexes = (
            (('issue', 'name'), True),  # unique keys
        )
        db_table = "splits"


class UnityIL2CPP(BaseModel):
    result = peewee.BooleanField(null=True)
    message = peewee.CharField(default=None, null=True)
    package_name = peewee.CharField(max_length=320, index=True)
    rule_flag = peewee.CharField(default=None, null=True)
    rule_key = peewee.CharField(default=None, null=True)
    rule_order = peewee.CharField(default=None, null=True)
    rule_data = peewee.CharField(default=None, null=True)
    updated = peewee.DateTimeField(default=datetime.utcnow)

    class Meta:
        db_table = "unity_il2cpp"


class UnityMono(BaseModel):
    original_md5sum = peewee.FixedCharField(max_length=32, index=True)
    package_name = peewee.CharField(max_length=320, index=True)
    result = peewee.BooleanField(null=True)
    message = peewee.CharField(default=None, null=True)
    updated = peewee.DateTimeField(default=datetime.utcnow)

    class Meta:
        db_table = "unity_mono"


class TestCases(BaseModel):
    md5sum = peewee.FixedCharField(max_length=32, index=True)
    package = peewee.CharField(max_length=320, index=True)
    vercode = peewee.IntegerField(index=True)
    android = peewee.CharField(max_length=16, index=True)
    model = peewee.CharField(max_length=32, index=True)
    resolution = peewee.CharField(max_length=16, index=True)
    test_case = peewee.CharField(max_length=16, index=True)
    updated = peewee.DateTimeField(default=datetime.utcnow, index=True)

    class Meta:
        db_table = "test_cases"


class AWS(BaseModel):
    md5sum = peewee.FixedCharField(max_length=32, unique=True, index=True)
    arn = peewee.FixedCharField(max_length=37, index=True)
    updated = peewee.DateTimeField(default=datetime.utcnow, index=True)

    class Meta:
        db_table = "aws"


db.create_tables([Migration], safe=True)
db.create_tables([Dev], safe=True)
db.create_tables([Apk], safe=True)
db.create_tables([Sku], safe=True)
db.create_tables([Rule], safe=True)
db.create_tables([Plugins], safe=True)
db.create_tables([PluginsReport], safe=True)
db.create_tables([Splits], safe=True)
db.create_tables([UnityIL2CPP], safe=True)
db.create_tables([UnityMono], safe=True)
db.create_tables([TestCases], safe=True)
db.create_tables([AWS], safe=True)

