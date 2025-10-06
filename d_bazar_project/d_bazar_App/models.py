from django.db import models

# Create your models here.

class Item(models.Model):
    pos  = models.IntegerField()
    image = models.ImageField()
    title = models.CharField(max_length=20)
    description = models.TextField()
    price = models.FloatField()
    amount = models.FloatField()
    special = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.title