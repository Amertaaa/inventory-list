from django.db import models
from django.contrib.auth.models import User
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)
    price  = models.IntegerField()
    amount = models.IntegerField()
    description = models.TextField(max_length=255)
    
# Create your models here.
# class Employee(models.Model): 
#     name = models.CharField(max_length=255)
#     age  = models.IntegerField()
#     hobby = models.TextField(max_length=255)