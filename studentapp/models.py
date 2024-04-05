from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class student(models.Model):
    #no need to add id, it will be by default
    name = models.CharField(max_length=40)
    branch = models.CharField(max_length=20)
    percent = models.FloatField()
    pimage=models.ImageField(upload_to='image')

class Cart(models.Model):
    sid = models.ForeignKey(student,on_delete=models.CASCADE,db_column='sid')
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    quantity = models.IntegerField(default=1)

class orders(models.Model):
    order_id=models.IntegerField()
    sid = models.ForeignKey(student,on_delete=models.CASCADE,db_column='sid')
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    quantity = models.IntegerField(default=1)