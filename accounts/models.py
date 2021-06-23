from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.files import ImageField
from django.utils import timezone
from cloudinary.models import CloudinaryField

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

class Group(models.Model):
    group_name = models.CharField(max_length=200, primary_key=True)
    description = models.TextField()
    contacts = ArrayField(models.PositiveIntegerField())
    members = ArrayField(models.CharField(max_length=100))
    scrnshot = CloudinaryField('image')
    tkg_number = models.CharField(max_length=25, default='')
    courier = models.CharField(max_length=25, default='')
    meeting_date = models.DateField(default=timezone.now)
    owner = models.CharField(max_length=50)
    address = models.CharField(max_length=255, default='')
    is_locked = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.group_name

class Shipping(models.Model):
    group = models.ForeignKey(Group, on_delete=CASCADE)
    group_name = models.CharField(max_length=200, primary_key=True)
    platform = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    base_shipping = models.DecimalField(max_digits=4, decimal_places=2)
    free_shipping_min = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    member_count = models.PositiveSmallIntegerField()
    def __str__(self) -> str:
        return self.group_name

class Data(models.Model):
    group_name = models.OneToOneField(Group, on_delete=CASCADE)
    users = ArrayField(models.CharField(max_length=50), default=list)
    items = ArrayField(models.CharField(max_length=200), default=list)
    prices = ArrayField(models.DecimalField(max_digits=6, decimal_places=2), default=list)
    urls = ArrayField(models.URLField(max_length=500), default=list)
    quantity = ArrayField(models.PositiveSmallIntegerField(), default=list)
    paid = ArrayField(models.BooleanField(), default=list)

    def total_price(self):
        total = 0
        for price in self.prices:
            total += price
        return total

    def __str__(self) -> str:
        return self.group_name.group_name