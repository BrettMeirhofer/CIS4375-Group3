from django.db import models

class Choice(models.Model):
    Product_Name = models.CharField(max_length=200)