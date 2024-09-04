from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    building_no = models.CharField(max_length=255, default="", null=True, blank=True)
    street_address_1 = models.CharField(max_length=255)
    street_address_2 = models.CharField(max_length=255)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pin = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.city + " " + self.pin 