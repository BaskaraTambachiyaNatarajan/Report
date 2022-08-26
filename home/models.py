from django.db import models

# Create your models here.

class Port(models.Model):
    price=models.DecimalField(decimal_places=5,max_digits=15)
    description=models.JSONField()
    name=models.CharField(max_length=500)
    img=models.ImageField()
    sellerid=models.IntegerField(default=0)
    productid=models.IntegerField(default=0)
    identity=models.IntegerField()
    name=models.CharField(max_length=500)
    portcode=models.CharField(max_length=10)
