from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.deletion import CASCADE

class Price(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    url = models.CharField(max_length=250)
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=20)
    priceArr = ArrayField(models.DecimalField(max_digits=6, decimal_places=2))
    dateArr = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return self.url