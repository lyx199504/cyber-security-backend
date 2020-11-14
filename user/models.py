from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    userId = models.AutoField(db_column='user_id', primary_key=True)
    openId = models.CharField(db_column='open_id', max_length=100)
    nickname = models.CharField(db_column='nickname', max_length=255)
    gender = models.IntegerField(db_column='gender', default=0)
    image = models.CharField(db_column='image', max_length=255)
    score = models.IntegerField(db_column='score', default=0)
    createTime = models.DateTimeField(db_column='create_time', auto_now=True)
    loginTime = models.DateTimeField(db_column='login_time', auto_now=True)

    class Meta:
        managed = False
        db_table = 'user'

    @staticmethod
    def allowFields():
        fields = list(map(lambda field: field.name, User._meta.fields))
        return fields