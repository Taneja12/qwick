from django.db import models
from django import forms
# Create your models here.

from django.db import models

class Product(models.Model):
    Title = models.CharField(max_length=30)
    Product_id = models.IntegerField(unique=True)
    Description = models.CharField(max_length=1000)
    price = models.FloatField(max_length=30)
    img = models.ImageField(upload_to='images/')
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.Title
    
class Contact(models.Model):
    email = models.CharField(max_length=30)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.subject
    



class Cart(models.Model):
    username = models.CharField(max_length=30)
    c_details = models.JSONField(default=dict)

    def __str__(self):
        return self.username

    def cart_contents(self):
        return self.c_details
     
class Wishlistt(models.Model):
    user = models.CharField(max_length=30)  # You might want to use a ForeignKey to the User model if you have a custom user model
    wl_details = models.ManyToManyField(Product, related_name='wishlist')

    def __str__(self):
        return self.user