from django.db import models
import datetime
from django.contrib.auth.models import User
# from .models import forms
import os

class Image(models.Model):
    caption=models.CharField(max_length=50)
    image1=models.ImageField(upload_to="img/%y")
    def __str__(self):
        return self.caption
    
class AImage(models.Model):
    caption1=models.CharField(max_length=50)
    image2=models.ImageField(upload_to="img/%y")
    def __str__(self):
        return self.caption1
    
class shop(models.Model):
    title=models.CharField(max_length=150,null=False,blank=False)
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to="img/%y")
    status=models.BooleanField(default=False,help_text="0-show , 1-Hidden")
    time_create=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class subcategories(models.Model):
    subcategory=models.ForeignKey(shop,on_delete=models.CASCADE)
    titlecat=models.CharField(max_length=150,null=False,blank=False)
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to="img/%y")
    status=models.BooleanField(default=False,help_text="0-show , 1-Hidden")
    time_create=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
      
class products(models.Model):
    category=models.ForeignKey(subcategories,on_delete=models.CASCADE)
    titlepd=models.CharField(max_length=150,null=False,blank=False)
    name=models.CharField(max_length=150)
    vendor=models.CharField(max_length=100)
    prod_image=models.ImageField(upload_to="img/%y")
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.IntegerField(null=False,blank=False)
    off_price=models.IntegerField(null=False,blank=False)
    description=models.TextField(max_length=450)
    trending=models.BooleanField(default=False,help_text="0-show , 1-Hidden")
    wishlist = models.BooleanField(default=False, help_text="0-show , 1-Hidden")
    status=models.BooleanField(default=False,help_text="0-show , 1-Hidden")
    time_create=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class regdata(models.Model):
    Firstname=models.CharField(max_length=25,null=False,blank=False)
    Lastname=models.CharField(max_length=25,null=False,blank=False)
    Email=models.CharField(max_length=50,null=False,blank=False)
    Password=models.CharField(max_length=20,null=False,blank=False)
    def __str__(self):
        return self.Firstname

class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    prod_qty=models.IntegerField(null=False,blank=False)
    time_create=models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.prod_qty*self.product.off_price

class wishlists(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    time_create=models.DateTimeField(auto_now_add=True)
