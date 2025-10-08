from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Item(models.Model):
    pos  = models.IntegerField()
    image = models.ImageField(upload_to='product_images/')
    title = models.CharField(max_length=20)
    description = models.TextField()
    price = models.IntegerField()
    amount = models.IntegerField()
    special = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.title

class User(AbstractUser):
    # Django's AbstractUser already has email, password, username etc.
    # We are making email the username field and making it unique.
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # Still required for createsuperuser