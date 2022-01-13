from tortoise import fields, models


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    full_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class Entries(models.Model):
    id = fields.IntField(pk=True)
    market = fields.CharField(max_length=10)
    direction = fields.CharField(max_length=5)
    setup = fields.CharField(max_length=25)
    order = fields.CharField(max_length=10)
    result = fields.FloatField(default=0.0)
    obs = fields.TextField(default="")
    author = fields.ForeignKeyField("models.Users", related_name="entry")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"Entry for {self.market}, created at {self.created_at}"


class Notes(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=225)
    content = fields.TextField()
    author = fields.ForeignKeyField("models.Users", related_name="note")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}, {self.author_id} on {self.created_at}"
