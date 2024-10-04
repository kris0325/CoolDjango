from django.db import models

# Create your models here.
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    salary = models.IntegerField()

    class Meta:
        db_table = 'users'  # 指定数据库中的表名为 'users'

    def __str__(self):
        return self.name
