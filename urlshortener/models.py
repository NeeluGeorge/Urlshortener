from django.db import models
import datetime


class Register(models.Model):
    username=models.CharField(max_length=10,primary_key=True)
    pwd=models.CharField(max_length=15)
    class Meta:
        db_table='user'

class Shortner(models.Model):
    userid=models.ForeignKey(Register,to_field='username',on_delete=models.CASCADE)
    urlshort=models.CharField(max_length=500,unique=True)
    url=models.CharField(max_length=200)
    date =models.DateField(("Date"),default=datetime.date.today)

    class Meta:
        db_table='urldata'

