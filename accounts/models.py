from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    item = models.CharField(max_length=255)
    date = models.CharField(max_length=15)
    company = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self) -> str:
        return self.item