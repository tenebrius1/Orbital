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

class Deliveries(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=200)
    tkg_number = models.CharField(max_length=25)
    courier_code = models.CharField(max_length=25)
    courier_name = models.CharField(max_length=25)
    class Meta:
        verbose_name = "Deliveries"
        verbose_name_plural = "Deliveries"
    def __str__(self) -> str:
        return self.tkg_number